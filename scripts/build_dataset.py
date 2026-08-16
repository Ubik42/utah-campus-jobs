#!/usr/bin/env python3
"""Build the public Utah campus part-time job dataset from a saved Jobsyn snapshot."""

from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any


FIELD_LABELS = (
    "Open Date",
    "Requisition Number",
    "Job Title",
    "Working Title",
    "Career Progression Track",
    "Track Level",
    "FLSA Code",
    "Patient Sensitive Job Code?",
    "Type",
    "Temporary?",
    "Standard Hours per Week",
    "Full Time or Part Time?",
    "Shift",
    "Work Schedule Summary",
    "Is this a work study job?",
    "VP Area",
    "Department",
    "Location",
    "City",
    "Type of Recruitment",
    "Pay Rate Range",
    "Close Date",
    "Priority Review Date (Note - Posting may close at any time)",
    "Job Summary",
    "Responsibilities",
    "Minimum Qualifications",
    "Preferences",
    "Special Instructions Summary",
    "Additional Information",
)

def clean_text(value: str | None) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"[\t ]+", " ", value)
    value = re.sub(r" *\n *", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def clean_markdown_value(value: str) -> str:
    value = re.sub(r"(?<=\w)\*\*(?=\w)", " ", value)
    value = value.replace("**", "")
    value = re.sub(r"(?m)^\s*[+*]\s+", "- ", value)
    return clean_text(value)


EN_ADDITIONAL_ANCHOR = "the university is a participating employer with utah retirement systems"

# Positions that require U.S. citizenship / national / lawful-permanent-resident
# status — a hard disqualifier for F-1 international students.
CITIZENSHIP_RE = re.compile(
    r"united states (citizen|national)|u\.?s\.? (citizen|national)|american (citizen|national)|"
    r"lawful permanent resident|permanent resident of the united states|"
    r"citizenship (is )?required|must be a (citizen|national)",
    re.I,
)


def strip_shared_additional_information(text: str) -> str:
    """Remove the university-wide Additional Information notice (URS boilerplate)
    when its heading was not bold in the source and the notice leaked into an
    adjacent field. The notice itself lives once in docs/shared-notices.md."""
    if not text:
        return text
    index = text.casefold().find(EN_ADDITIONAL_ANCHOR)
    if index == -1:
        return text
    head = text[:index]
    head = re.sub(r"\s*\*{0,2}Additional Information\*{0,2}\s*:?\s*$", "", head, flags=re.IGNORECASE)
    return head.strip()


def strip_shared_additional_information_zh(text: str) -> str:
    """Chinese counterpart of strip_shared_additional_information."""
    if not text:
        return text
    match = re.search(r"(?:大学|犹他大学)是犹他州退休系统", text)
    if not match:
        return text
    head = text[: match.start()]
    head = re.sub(r"\s*补充信息\s*:?\s*$", "", head)
    return head.strip()


def parse_fields(description: str) -> dict[str, str]:
    """Use only known template labels as boundaries; keep bold text in body copy."""
    recognized: list[tuple[str, int, int]] = []
    allowed = set(FIELD_LABELS)
    for match in re.finditer(r"\*\*(.+?)\*\*", description, flags=re.DOTALL):
        label = clean_text(match.group(1)).rstrip(":")
        if label in allowed:
            recognized.append((label, match.start(), match.end()))

    fields: dict[str, str] = {}
    for index, (label, _start, end) in enumerate(recognized):
        next_start = recognized[index + 1][1] if index + 1 < len(recognized) else len(description)
        fields[label] = clean_markdown_value(description[end:next_start])
    return fields


def parse_us_date(value: str | None) -> date | None:
    value = clean_text(value)
    if not value:
        return None
    try:
        return datetime.strptime(value, "%m/%d/%Y").date()
    except ValueError:
        return None


def iso(value: date | None) -> str | None:
    return value.isoformat() if value else None


def first_numbers(value: str) -> list[float]:
    return [float(item.replace(",", "")) for item in re.findall(r"\d[\d,]*(?:\.\d+)?", value)]


def parse_hours(value: str) -> tuple[float | None, float | None]:
    numbers = first_numbers(value)
    if not numbers:
        return None, None
    normalized = value.casefold()
    if "or less" in normalized or "or fewer" in normalized:
        return 0.0, numbers[0]
    if "up to" in normalized or "maximum" in normalized or re.search(r"\bmax\.?\b", normalized):
        if len(numbers) >= 2:
            return numbers[0], numbers[1]
        return 0.0, numbers[0]
    if len(numbers) == 1:
        return numbers[0], numbers[0]
    return numbers[0], numbers[1]


def parse_pay(value: str) -> tuple[float | None, float | None]:
    numbers = first_numbers(value)
    if not numbers:
        return None, None
    # Annual salaries occasionally appear in part-time postings. Do not compare them
    # with hourly rates in the public sort.
    if any(number > 500 for number in numbers) and not re.search(r"/\s*(?:hr|hour)|hourly", value, re.I):
        return None, None
    if len(numbers) == 1:
        return numbers[0], numbers[0]
    return numbers[0], numbers[1]


def available_on(open_date: date | None, close_date: date | None, target: date) -> bool:
    return not ((open_date and target < open_date) or (close_date and target > close_date))


def work_study_status(title: str, fields: dict[str, str]) -> tuple[str, str]:
    evidence = "\n".join(
        [
            title,
            fields.get("Is this a work study job?", ""),
            fields.get("Job Summary", ""),
            fields.get("Minimum Qualifications", ""),
            fields.get("Special Instructions Summary", ""),
        ]
    )
    normalized = re.sub(r"\s+", " ", evidence).casefold()
    optional = re.search(
        r"work[ -]?study(?: participation)? (?:is )?not required|work[ -]?study is optional|does not require (?:federal )?work[ -]?study",
        normalized,
    )
    if optional:
        return "可选/非必需", optional.group(0)
    required = re.search(
        r"(?:only (?:available|open)|available only) to.{0,100}work[ -]?study|must.{0,100}(?:work[ -]?study|\bfws\b)|(?:work[ -]?study|\bfws\b).{0,100}(?:required|requirement)|if you have not received.{0,100}work[ -]?study|employment is contingent.{0,100}work[ -]?study|seeking (?:a )?work[ -]?study student",
        normalized,
    )
    title_mark = re.search(r"\bwork[ -]?study\b|(?:^|[\s(-])ws(?:$|[\s)-])", title.casefold())
    field_yes = fields.get("Is this a work study job?", "").strip().casefold() == "yes"
    if required or title_mark or field_yes:
        evidence_text = required.group(0) if required else (title_mark.group(0) if title_mark else fields.get("Is this a work study job?", "Yes"))
        return "必需", clean_text(evidence_text)
    return "未明确要求", ""


def requirement_status(text: str, kind: str) -> tuple[str, str]:
    normalized = re.sub(r"\s+", " ", text).casefold()
    patterns = {
        "driver": r"(?:valid |current )?(?:utah |u\.s\. |us )?(?:driver.{0,3}s|driving) (?:license|licence)|valid driver license",
        "food": r"food[- ]handler(?:.{0,3}s)? (?:permit|card|certification)|food handler permit",
        "alcohol": r"alcohol (?:server |service )?(?:certification|license)|servsafe alcohol|tips certification",
    }
    match = re.search(patterns[kind], normalized)
    if not match:
        return "未发现明确要求", ""
    window = normalized[max(0, match.start() - 100): min(len(normalized), match.end() + 130)]
    if re.search(r"within \d+ days|after (?:hire|hiring)|upon hire|must obtain|ability to obtain|obtain.*within", window):
        return "入职后可取得", clean_text(window)
    return "明确要求/需核验", clean_text(window)


def experience_status(minimum: str) -> tuple[str, str]:
    normalized = re.sub(r"\s+", " ", minimum).casefold()
    matches = list(re.finditer(r"(?:one|two|three|four|five|six|\d+) years?.{0,90}(?:experience|employment)", normalized))
    if not matches:
        return "未发现明确年限", ""
    evidence = clean_text("; ".join(match.group(0) for match in matches[:3]))
    return "明确要求经验年限", evidence


def job_url(job: dict[str, Any]) -> str:
    return f"https://employment.utah.edu/salt-lake-city-ut/{job['title_slug']}/{job['guid']}/job/"


def load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        item = json.loads(line)
        guid = item["guid"]
        if guid in result:
            raise ValueError(f"Duplicate GUID in {path.name}:{line_number}: {guid}")
        result[guid] = item
    return result


def build_records(raw_path: Path, translations_path: Path, departments_path: Path, extra_requirements_path: Path, job_descriptions_path: Path) -> tuple[list[dict[str, Any]], str]:
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    translations = load_jsonl(translations_path)
    departments = json.loads(departments_path.read_text(encoding="utf-8"))
    extra_requirements = json.loads(extra_requirements_path.read_text(encoding="utf-8"))
    job_descriptions = json.loads(job_descriptions_path.read_text(encoding="utf-8"))
    jobs = {job["guid"]: job for response in raw["responses"] for job in response.get("jobs", [])}
    part_time = [job for job in jobs.values() if job.get("job_type") == "Part Time"]
    records: list[dict[str, Any]] = []

    for job in part_time:
        guid = job["guid"]
        translation = translations.get(guid)
        if translation is None:
            raise ValueError(f"Missing translation: {job.get('title_exact')} ({guid})")
        fields = parse_fields(job.get("description", ""))
        fields = {key: strip_shared_additional_information(value) for key, value in fields.items()}
        department_raw = clean_text(fields.get("Department"))
        department = departments.get(department_raw, {"zh": department_raw or "未提供", "en": department_raw or "Not provided"})
        open_date = parse_us_date(fields.get("Open Date"))
        if open_date is None:
            try:
                open_date = datetime.fromisoformat(str(job.get("date_new", "")).replace("Z", "+00:00")).date()
            except ValueError:
                pass
        close_date = parse_us_date(fields.get("Close Date"))
        hours_text = clean_text(fields.get("Standard Hours per Week")) or "未提供"
        pay_text = clean_text(fields.get("Pay Rate Range")) or "未提供"
        hours_min, hours_max = parse_hours(hours_text)
        pay_min, pay_max = parse_pay(pay_text)
        title_en = clean_text(job.get("title_exact"))
        minimum_en = clean_text(fields.get("Minimum Qualifications"))
        translated_pairs = (
            ("Work Schedule Summary", "work_schedule_summary_zh"),
            ("Responsibilities", "responsibilities_zh"),
            ("Preferences", "preferences_zh"),
            ("Special Instructions Summary", "special_instructions_zh"),
        )
        for source_label, translated_key in translated_pairs:
            if clean_text(fields.get(source_label)) and not clean_text(translation.get(translated_key)):
                raise ValueError(f"Missing {translated_key}: {title_en} ({guid})")
        all_requirement_text = "\n".join(
            [minimum_en, fields.get("Responsibilities", ""), fields.get("Preferences", ""), fields.get("Special Instructions Summary", "")]
        )
        ws_status, ws_evidence = work_study_status(title_en, fields)
        driver_status, driver_evidence = requirement_status(all_requirement_text, "driver")
        food_status, food_evidence = requirement_status(all_requirement_text, "food")
        alcohol_status, alcohol_evidence = requirement_status(all_requirement_text, "alcohol")
        exp_status, exp_evidence = experience_status(minimum_en)
        undergrad_only = bool(translation.get("requires_undergraduate"))
        requires_citizenship = bool(
            CITIZENSHIP_RE.search("\n".join([title_en, minimum_en, fields.get("Preferences", "")]))
        )
        posting_text = "\n".join(fields.values())
        explicitly_closed = bool(
            re.search(r"this posting is closed and is no longer accepting applications", posting_text, re.I)
        )

        record = {
            "guid": guid,
            "requisition_number": clean_text(fields.get("Requisition Number")) or job.get("reqid"),
            "url": job_url(job),
            "title_zh": translation["title_zh"],
            "title_en": title_en,
            "department_zh": department["zh"],
            "department_en": department["en"],
            "department_raw": department_raw,
            "open_date": iso(open_date),
            "close_date": iso(close_date),
            "priority_review_date": iso(parse_us_date(fields.get("Priority Review Date (Note - Posting may close at any time)"))),
            "explicitly_closed_in_posting_text": explicitly_closed,
            "standard_hours_text": hours_text,
            "minimum_weekly_hours": hours_min,
            "maximum_weekly_hours": hours_max,
            "hours_group": "最低工时 > 10 小时" if hours_min is not None and hours_min > 10 else "最低工时 ≤ 10 小时或未提供",
            "pay_rate_text": pay_text,
            "minimum_hourly_pay": pay_min,
            "maximum_hourly_pay": pay_max,
            "work_study_status": ws_status,
            "work_study_evidence": ws_evidence,
            "undergraduate_only": undergrad_only,
            "undergraduate_evidence_zh": translation.get("undergraduate_filter_reason", ""),
            "requires_citizenship": requires_citizenship,
            "driver_license_status": driver_status,
            "driver_license_evidence": driver_evidence,
            "food_handler_status": food_status,
            "food_handler_evidence": food_evidence,
            "alcohol_certificate_status": alcohol_status,
            "alcohol_certificate_evidence": alcohol_evidence,
            "experience_status": exp_status,
            "experience_evidence": exp_evidence,
            "shift": clean_text(fields.get("Shift")),
            "work_schedule_summary_en": clean_text(fields.get("Work Schedule Summary")),
            "work_schedule_summary_zh": strip_shared_additional_information_zh(translation.get("work_schedule_summary_zh", "")),
            "job_summary_zh": strip_shared_additional_information_zh(translation["summary_zh"]),
            "job_summary_en": clean_text(fields.get("Job Summary")),
            "minimum_qualifications_zh": strip_shared_additional_information_zh(translation["minimum_qualifications_zh"]),
            "minimum_qualifications_en": minimum_en,
            "responsibilities_zh": strip_shared_additional_information_zh(translation.get("responsibilities_zh", "")),
            "responsibilities_en": clean_text(fields.get("Responsibilities")),
            "preferences_zh": strip_shared_additional_information_zh(translation.get("preferences_zh", "")),
            "preferences_en": clean_text(fields.get("Preferences")),
            "special_instructions_zh": strip_shared_additional_information_zh(translation.get("special_instructions_zh", "")),
            "special_instructions_en": clean_text(fields.get("Special Instructions Summary")),
            "type_of_recruitment": clean_text(fields.get("Type of Recruitment")),
            "extra_requirements": extra_requirements.get(guid, ""),
            "job_description": job_descriptions.get(guid, ""),
            "source_updated_at": job.get("date_updated"),
        }
        records.append(record)

    def sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
        return (item["department_zh"], item["title_zh"], item["guid"])

    records.sort(key=sort_key)
    return records, raw["fetched_at"]


def md_value(value: Any) -> str:
    if value is None or value == "":
        return "未提供"
    return str(value)


def render_markdown(records: list[dict[str, Any]], fetched_at: str) -> str:
    lines = [
        "# 犹他大学 2026 Fall 校内兼职完整中文索引",
        "",
        f"> 共 {len(records)} 个 Part Time 岗位；官网快照抓取时间：{fetched_at}。中文翻译用于快速浏览，申请前请点击职位链接核对英文原文。",
        "",
        "默认按部门和中文职位名排列。开放日期、截止日期、工时、薪资和资格标签均保留在 Excel，读者可按自己的条件筛选。",
        "",
    ]
    current_department = None
    for record in records:
        if record["department_zh"] != current_department:
            current_department = record["department_zh"]
            lines.extend([f"## {record['department_zh']}", "", f"*{record['department_en']}*", ""])
        lines.extend(
            [
                f"### [{record['title_zh']}]({record['url']})",
                "",
                f"*{record['title_en']}*",
                "",
                "#### 岗位概览",
                "",
                f"- 开放日期：{md_value(record['open_date'])}",
                f"- 截止日期：{md_value(record['close_date'])}",
                f"- 每周标准工时：{record['standard_hours_text']}",
                f"- 薪资：{record['pay_rate_text']}",
                f"- Work-Study：{record['work_study_status']}",
                f"- 本科生限定：{'是' if record['undergraduate_only'] else '未发现明确限定'}",
                f"- 驾照：{record['driver_license_status']}；食品处理员许可证：{record['food_handler_status']}；酒类服务证书：{record['alcohol_certificate_status']}",
                f"- 页面明确关闭：{'是' if record['explicitly_closed_in_posting_text'] else '否'}",
                "",
                "#### 职位摘要",
                "",
                record["job_summary_zh"] or "未提供职位摘要。",
                "",
                "#### 工作职责",
                "",
                record["responsibilities_zh"] or "未提供。",
                "",
                "#### 最低资格",
                "",
                record["minimum_qualifications_zh"] or "未提供。",
                "",
                "#### 优先条件",
                "",
                record["preferences_zh"] or "未提供。",
                "",
                "#### 申请说明",
                "",
                record["special_instructions_zh"] or "未提供。",
                "",
                "#### 排班安排",
                "",
                record["work_schedule_summary_zh"] or "未提供。",
                "",
                "<details>",
                "<summary>查看英文原文</summary>",
                "",
                f"**Job Summary**\n\n{record['job_summary_en'] or 'Not provided.'}",
                "",
                f"**Responsibilities**\n\n{record['responsibilities_en'] or 'Not provided.'}",
                "",
                f"**Minimum Qualifications**\n\n{record['minimum_qualifications_en'] or 'Not provided.'}",
                "",
                f"**Preferences**\n\n{record['preferences_en'] or 'Not provided.'}",
                "",
                f"**Special Instructions**\n\n{record['special_instructions_en'] or 'Not provided.'}",
                "",
                f"**Work Schedule**\n\n{record['work_schedule_summary_en'] or 'Not provided.'}",
                "",
                "</details>",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--raw", type=Path, default=root / "data/raw/jobsyn-campus-2026-08-16.json")
    parser.add_argument("--translations", type=Path, default=root / "data/translations.zh.jsonl")
    parser.add_argument("--departments", type=Path, default=root / "data/department-names.zh.json")
    parser.add_argument("--extra-requirements", type=Path, default=root / "data/extra-requirements.json")
    parser.add_argument("--job-descriptions", type=Path, default=root / "data/job-descriptions.json")
    parser.add_argument("--json-output", type=Path, default=root / "data/jobs.zh.json")
    parser.add_argument("--markdown-output", type=Path, default=root / "jobs.zh.md")
    args = parser.parse_args()

    records, fetched_at = build_records(args.raw, args.translations, args.departments, args.extra_requirements, args.job_descriptions)
    args.json_output.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "snapshot_fetched_at": fetched_at,
                "job_count": len(records),
                "jobs": records,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
        newline="\n",
    )
    args.markdown_output.write_text(render_markdown(records, fetched_at), encoding="utf-8", newline="\n")
    print(f"Built {len(records)} jobs -> {args.json_output.name}, {args.markdown_output.name}")


if __name__ == "__main__":
    main()
