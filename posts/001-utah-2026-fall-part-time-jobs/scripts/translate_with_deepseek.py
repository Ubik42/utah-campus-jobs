#!/usr/bin/env python3
"""Complete missing Chinese job-field translations with the DeepSeek API.

The API key is read only from DEEPSEEK_API_KEY. It is never written to disk or
printed. Successful translations are cached by source-text SHA-256 so the job
can be resumed without paying for the same text twice.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"
SOURCE_FIELDS = {
    "work_schedule_summary_en": "work_schedule_summary_zh",
    "responsibilities_en": "responsibilities_zh",
    "preferences_en": "preferences_zh",
    "special_instructions_en": "special_instructions_zh",
    "additional_information_en": "additional_information_zh",
}
SYSTEM_PROMPT = """你是严谨的美国大学招聘信息译者。把英文完整翻译成简体中文，不增删事实。
要求：
1. 保留段落、项目符号、编号、日期、数字、薪资、URL、邮箱、专有名词和证照名；
2. 不概括、不解释、不替申请人判断资格；
3. Work-Study 保留英文并可写作“勤工助学（Work-Study）”；
4. 只返回 JSON：{\"translated_text\": \"...\"}。"""


def text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def save_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    temporary.replace(path)


def save_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) for row in rows) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def split_text(text: str, limit: int = 12000) -> list[str]:
    if len(text) <= limit:
        return [text]
    paragraphs = re.split(r"(\n\n+)", text)
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if len(current) + len(paragraph) <= limit:
            current += paragraph
            continue
        if current.strip():
            chunks.append(current.strip())
        while len(paragraph) > limit:
            chunks.append(paragraph[:limit])
            paragraph = paragraph[limit:]
        current = paragraph
    if current.strip():
        chunks.append(current.strip())
    return chunks


def call_deepseek(text: str, api_key: str, attempts: int = 6) -> str:
    payload = json.dumps(
        {
            "model": MODEL,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
        },
        ensure_ascii=False,
    ).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = Request(
            API_URL,
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )
        try:
            with urlopen(request, timeout=180) as response:
                result = json.load(response)
            content = result["choices"][0]["message"]["content"]
            translated = json.loads(content)["translated_text"]
            if not isinstance(translated, str) or not translated.strip():
                raise ValueError("DeepSeek returned an empty translation")
            return translated.strip()
        except (HTTPError, URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(min(45, 3 * (2**attempt)))
    raise RuntimeError("DeepSeek translation failed after retries") from last_error


def translate_text(text: str, api_key: str) -> str:
    chunks = split_text(text)
    return "\n\n".join(call_deepseek(chunk, api_key) for chunk in chunks)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    root = Path(__file__).resolve().parents[1]
    parser.add_argument("--jobs", type=Path, default=root / "data/jobs.zh.json")
    parser.add_argument("--translations", type=Path, default=root / "data/translations.zh.jsonl")
    parser.add_argument("--cache", type=Path, default=root / "data/deepseek-translation-cache.json")
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    jobs = json.loads(args.jobs.read_text(encoding="utf-8"))["jobs"]
    translations = load_jsonl(args.translations)
    translations_by_guid = {row["guid"]: row for row in translations}
    cache: dict[str, str] = json.loads(args.cache.read_text(encoding="utf-8")) if args.cache.exists() else {}

    source_by_hash: dict[str, str] = {}
    assignments: list[tuple[str, str, str]] = []
    for job in jobs:
        target = translations_by_guid[job["guid"]]
        for source_field, target_field in SOURCE_FIELDS.items():
            source = (job.get(source_field) or "").strip()
            if not source:
                target[target_field] = ""
                continue
            digest = text_hash(source)
            source_by_hash[digest] = source
            assignments.append((job["guid"], target_field, digest))

    missing = {digest: source for digest, source in source_by_hash.items() if digest not in cache}
    total_chars = sum(len(source) for source in missing.values())
    print(f"Unique source texts: {len(source_by_hash)}; cached: {len(source_by_hash) - len(missing)}; missing: {len(missing)}; characters: {total_chars}")
    if args.dry_run:
        return

    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is not configured; no external fallback is allowed")

    lock = threading.Lock()
    completed = 0
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(translate_text, source, api_key): digest for digest, source in missing.items()}
        for future in as_completed(futures):
            digest = futures[future]
            translated = future.result()
            with lock:
                cache[digest] = translated
                completed += 1
                save_json(args.cache, cache)
                if completed == 1 or completed % 10 == 0 or completed == len(missing):
                    print(f"Translated {completed}/{len(missing)} unique texts", flush=True)

    for guid, target_field, digest in assignments:
        translations_by_guid[guid][target_field] = cache[digest]
    save_jsonl(args.translations, translations)
    print(f"Updated {args.translations} with complete translated fields")


if __name__ == "__main__":
    main()
