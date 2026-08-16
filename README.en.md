# University of Utah On-Campus Part-Time Jobs

> A cleaned-up, searchable collection of University of Utah **part-time** on-campus job postings — full Chinese translation, filterable Excel, and original English text side by side.

[![中文](https://img.shields.io/badge/中文-README-1E7B1E)](README.md) [![English](https://img.shields.io/badge/English-README-1F4E79)](README.en.md)

![Jobs](https://img.shields.io/badge/Jobs-122-1E7B1E) ![Snapshot](https://img.shields.io/badge/Snapshot-2026--08--16-1F4E79) ![License](https://img.shields.io/badge/License-MIT-808080)

## Download the spreadsheet

### [⬇️ Download jobs.xlsx](jobs.xlsx)

[![Download jobs.xlsx](https://img.shields.io/badge/Download-jobs.xlsx-1E7B1E?style=for-the-badge&logo=microsoftexcel&logoColor=white)](jobs.xlsx)

> 122 part-time jobs for the Fall 2026 (26Fall) semester, in five sheets: Search · Full Chinese · English Source · MEAE Intl TL;DR · Guide.

## Table of Contents

- [Download the spreadsheet](#download-the-spreadsheet)
- [What is this](#what-is-this)
- [Quick start](#quick-start)
- [Files](#files)
- [Application cautions](#application-cautions)
- [About Federal Work-Study](#about-federal-work-study)
- [Screening criteria](#screening-criteria)
- [Data source](#data-source)
- [Regenerate](#regenerate)
- [License](#license)

## What is this

The University of Utah jobs site makes you open each posting one by one, and many detail-page subheadings sit at the same visual level, which is hard to scan. This repo grabs a **2026-08-16** snapshot of the campus part-time listings and reorganizes it into:

- **122 Part Time jobs**, each split into a consistent structure: Summary / Responsibilities / Minimum Qualifications / Preferences / Special Instructions / Work Schedule;
- full Chinese translation with the original English kept side by side;
- one filterable Excel (the Search sheet) you can filter by department, date, hours, pay, Work-Study, undergraduate-only, driver's license, food handler permit, experience, and more.

The public version does not remove jobs based on any individual's identity or application date. Undergraduates, graduates, and students with or without Federal Work-Study can all filter to their own situation.

## Quick start

1. Download [`jobs.xlsx`](jobs.xlsx) and open the **岗位检索 (Search)** sheet.
2. Filter by your application date (open date ≤ today ≤ close date), status (undergraduate-only or not), hours, pay, and certifications.
3. Click the **中文职位 (Chinese title)** column — each cell is a link to the official posting.
4. For the full text, read the **完整中文 (Full Chinese)** and **英文原文 (English Source)** sheets, or [`jobs.zh.md`](jobs.zh.md).

## Files

| File | Content |
| --- | --- |
| `jobs.xlsx` | Recommended entry: Search, Full Chinese, English Source, MEAE Intl TL;DR, Guide — five sheets |
| `jobs.zh.md` | 122 jobs organized by department, full Chinese with collapsible English source |
| `data/jobs.zh.json` | Cleaned bilingual structured data |
| `data/raw/jobsyn-campus-2026-08-16.json` | Raw snapshot from the job-list API |
| `data/translations.zh.jsonl` | Chinese translations keyed by GUID |
| `data/extra-requirements.json` | Curated hard requirements (certificates, language, degree, etc.) |
| `data/job-descriptions.json` | Curated plain-language job descriptions (one line on what the job actually does) |
| `docs/filtering-and-sorting.md` | Field extraction, filtering and sorting rules (Chinese) |
| `docs/data-dictionary.md` | Excel and JSON field glossary (Chinese) |
| `docs/shared-notices.md` | University-wide Additional Information boilerplate (Chinese) |

## Application cautions

> This is a cleaned-up historical snapshot, not an official eligibility confirmation from the university. **Always verify against the official posting before applying.**

1. **Snapshot ≠ live**: jobs may close early or change; click the title to check the official page.
2. **Skip "page explicitly closed" jobs**: 5 postings say "This posting is closed and is no longer accepting applications" even though their listed close date is in the future (the 页面明确关闭 column shows ✅).
3. **Chinese is AI translation**: use it for quick browsing only; for qualifications, certifications, dates and application materials, rely on the English source.
4. **Tags are only a first pass, not a university confirmation**:
   - **Work-Study**: ✅ required = you need a Federal Work-Study award, don't apply without one; 🟡 optional; ❌ not specified.
   - **Undergraduate-only**: ✅ = explicitly for undergraduates; graduate students should confirm eligibility first.
   - **Driver's license**: ✅ required = must already have one; 🟡 can obtain after hire.
   - **Food handler permit**: relatively easy to get (a short online course + small fee); many jobs allow you to obtain it after hire (🟡).
   - **Experience**: ✅ = explicit years of experience required; "education may substitute for experience" still needs your own judgment.
   - **Extra requirements**: hard requirements from the posting text (language, certificates, degree, software, physical, age, etc.).
   - **Job description**: what the job actually does, in plain language — curated in `data/job-descriptions.json`.
5. **Two dates**: open date and close date. A posting that says it is closed should be skipped even if its close date hasn't passed (see #2).
6. **Hours and pay**: hours are parsed values (e.g. `0-19`, `up to 10`); `DOE` or annual salaries are not converted to hourly.
7. **Background check**: some jobs require a background check / drug screen; see [`docs/shared-notices.md`](docs/shared-notices.md).

## About Federal Work-Study

**If you are an F-1 international student, you cannot get Federal Work-Study (FWS).** Per the [University of Utah ISSS](https://isss.utah.edu/f-1-visa-program/employment/on-campus-employment/index.php), international students are not eligible for Work-Study because it is a federal aid program.

If a posting says:

- `Federal Work-Study Award required`
- `Must have Work-Study eligibility`
- `Work-Study position only`

you can skip it — it is not the same as a regular on-campus job.

If you are a U.S. citizen or eligible non-citizen, the process is:

1. Submit the FAFSA for the academic year and have the University of Utah receive it;
2. wait for the financial-need review;
3. check your aid package under CIS Financial Aid;
4. if Federal Work-Study is in the package, accept it in CIS;
5. if you filed the FAFSA but FWS is missing, submit the [2026–2027 Federal Work-Study application form](https://financialaid.utah.edu/forms/onbase/2026-2027-federal-work-study-form.php) to request reconsideration;
6. only after receiving an FWS Award can you apply to FWS-only positions;
7. before starting, the employer must apply to the aid office for an EAF — the EAF is the final work-eligibility confirmation.

The university requires: financial need, enrollment in an eligible degree program, Satisfactory Academic Progress (SAP), enrollment in at least one credit-bearing course, a valid SSN, and U.S. citizenship or eligible non-citizen status. Funding is limited, so applying does not guarantee approval.

**If you are on F-1, look for regular on-campus student jobs.** F-1 students can generally do eligible on-campus work, up to 20 hours/week during the semester.

References:
- [F-1 on-campus employment (University of Utah ISSS)](https://isss.utah.edu/f-1-visa-program/employment/on-campus-employment/index.php)
- [Federal Work-Study basics](https://financialaid.utah.edu/types-of-aid/work-study/students/basics.php)
- [2026–2027 Federal Work-Study application form](https://financialaid.utah.edu/forms/onbase/2026-2027-federal-work-study-form.php)

## Screening criteria

The **岗位检索 (Search)** sheet labels each job with a set of eligibility tags, auto-extracted from the English source. The rules are documented in [`docs/filtering-and-sorting.md`](docs/filtering-and-sorting.md) (Chinese). Key tags:

- **Work-Study**: required / optional · not required / not specified — Federal Work-Study (FWS); F-1 students are not eligible.
- **Undergraduate-only**: yes / no — whether the job is explicitly for undergraduates only.
- **Driver's license / Food handler**: required / obtainable after hire / no explicit requirement found.
- **Experience**: explicit years required / no explicit years found.
- **Page explicitly closed**: whether the posting text says it is no longer accepting applications.
- **Extra requirements**: hard requirements from the text (language, certificates, degree, software, physical, age, etc.), curated in `data/extra-requirements.json`.
- **Citizenship required** (JSON field `requires_citizenship`): whether the posting requires U.S. citizen / national / lawful permanent resident — a hard exclusion for F-1 students.
- **Job description**: what the job actually does in plain language, curated in `data/job-descriptions.json`.

The **MEAE国际学生省流版 (MEAE Intl TL;DR)** sheet is a condensed view for MEAE master's + F-1 international students. It automatically excludes four kinds of jobs:

1. Work-Study required;
2. undergraduate-only;
3. page explicitly closed;
4. citizenship required.

When you pull a fresh snapshot, re-run `scripts/build_dataset.py` and `scripts/build_xlsx.py` to rebuild with the same rules, then have an AI re-review the tags that require reading the source text (extra requirements and citizenship).

## Data source

- Source: [University of Utah Campus Jobs](https://employment.utah.edu/location-name/campus/organization/university-of-utah/jobs/)
- Snapshot time: 2026-08-16 05:02 (UTC+8)
- Raw listings: 319 · Part Time: 122
- Fully translated fields: job title, summary, responsibilities, minimum qualifications, preferences, special instructions, work schedule

## Regenerate

Using the local snapshot only (no network):

```powershell
python scripts/build_dataset.py   # builds data/jobs.zh.json + jobs.zh.md
python scripts/build_xlsx.py      # builds jobs.xlsx
python -m unittest discover -s scripts -p "test_*.py"
```

Re-fetch the official listings / translate new fields:

```powershell
python scripts/fetch_jobs.py --output data/raw/jobsyn-campus-YYYY-MM-DD.json
python scripts/translate_with_deepseek.py
```

The translation script reads only the `DEEPSEEK_API_KEY` environment variable; it never prints or saves the key, and it does not fall back to another service when the API is unavailable.

## License

The code is [MIT License](LICENSE). The original job postings and raw data belong to their publisher and are not covered by that license.
