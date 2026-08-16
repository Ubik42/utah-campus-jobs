#!/usr/bin/env python3
"""Download all University of Utah Campus job-list API pages into one JSON snapshot."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SEARCH_API = "https://prod-search-api.jobsyn.org/api/v1/solr/search"
HEADERS = {
    "Accept": "application/json",
    "Origin": "https://employment.utah.edu",
    "Referer": "https://employment.utah.edu/",
    "User-Agent": "rednote-sharing-utah-job-index/1.0",
    "x-origin": "employment.utah.edu",
}


def request_json(url: str, attempts: int = 5) -> Any:
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urlopen(Request(url, headers=HEADERS), timeout=30) as response:
                return json.load(response)
        except HTTPError as error:
            last_error = error
            delay = int(error.headers.get("Retry-After", 0) or 0) if error.code == 429 else 0
            delay = delay or 2 * (attempt + 1)
        except (URLError, TimeoutError) as error:
            last_error = error
            delay = 2 * (attempt + 1)
        if attempt + 1 < attempts:
            print(f"Request failed; retrying in {delay}s ({attempt + 2}/{attempts})", flush=True)
            time.sleep(delay)
    raise RuntimeError(f"Request failed after {attempts} attempts: {url}") from last_error


def fetch_pages() -> list[dict[str, Any]]:
    pages: list[dict[str, Any]] = []
    page = 1
    while True:
        query = urlencode(
            {
                "page": page,
                "organizations": "university-of-utah",
                "locationnames": "campus",
                "num_items": 40,
            }
        )
        payload = request_json(f"{SEARCH_API}?{query}")
        pages.append(payload)
        pagination = payload["pagination"]
        print(f"Fetched page {page}/{pagination['total_pages']}", flush=True)
        if not pagination["has_more_pages"]:
            return pages
        page += 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="Path for the timestamped raw JSON snapshot")
    args = parser.parse_args()
    pages = fetch_pages()
    fetched_at = datetime.now().astimezone()
    payload = {
        "schema_version": 1,
        "fetched_at": fetched_at.isoformat(),
        "source": SEARCH_API,
        "query": {
            "organizations": "university-of-utah",
            "locationnames": "campus",
            "num_items": 40,
        },
        "responses": pages,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
    temporary.replace(args.output)
    unique_jobs = {job["guid"] for page in pages for job in page.get("jobs", [])}
    print(f"Saved {len(unique_jobs)} unique jobs to {args.output}")


if __name__ == "__main__":
    main()
