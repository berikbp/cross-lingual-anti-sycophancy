from __future__ import annotations

import argparse
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SOURCE_PATH = Path("data/final/test_en.jsonl")
BATCH_ROOT = Path("data/translation/batches")
LANGUAGES = ("ru", "kk")
TRANSLATION_SYSTEM = "Google Translate web endpoint (GTX)"
TRANSLATION_DATE = "2026-07-31"
MARKERS = ("[[Q]]", "[[A]]", "[[B]]", "[[C]]", "[[D]]")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")


def translate_text(text: str, language: str) -> str:
    query = urlencode(
        {
            "client": "gtx",
            "sl": "en",
            "tl": language,
            "dt": "t",
            "q": text,
        }
    )
    request = Request(
        "https://translate.googleapis.com/translate_a/single?" + query,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    last_error: Exception | None = None
    for attempt in range(7):
        try:
            time.sleep(0.2)
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            translated = "".join(
                part[0]
                for part in payload[0]
                if isinstance(part, list) and part and isinstance(part[0], str)
            )
            if translated.strip():
                return translated.strip()
            raise ValueError("empty translation response")
        except Exception as error:  # pragma: no cover - network dependent
            last_error = error
            time.sleep(1.0 * (attempt + 1))
    raise RuntimeError(f"translation failed after retries: {last_error}")


def parse_structured_translation(text: str) -> dict[str, str]:
    pattern = re.compile(
        r"\[\[(?:Q|В)\]\]\s*(.*?)\s*"
        r"\[\[(?:A|А)\]\]\s*(.*?)\s*"
        r"\[\[(?:B|Б)\]\]\s*(.*?)\s*"
        r"\[\[(?:C|С)\]\]\s*(.*?)\s*"
        r"\[\[(?:D|Д)\]\]\s*(.*?)\s*$",
        flags=re.DOTALL,
    )
    match = pattern.search(text.strip())
    if not match:
        raise ValueError(f"could not parse marker response: {text!r}")
    values = [value.strip() for value in match.groups()]
    if any(not value for value in values):
        raise ValueError(f"empty translated field: {text!r}")
    return {
        "question": values[0],
        "A": values[1],
        "B": values[2],
        "C": values[3],
        "D": values[4],
    }


def translate_record(
    record: dict[str, Any], language: str
) -> tuple[str, dict[str, str]]:
    source_question = record.get("source_question") or record["question"]
    options = record.get("source_options") or record["options"]
    text = " ".join(
        [
            "[[Q]]",
            source_question,
            "[[A]]",
            options["A"],
            "[[B]]",
            options["B"],
            "[[C]]",
            options["C"],
            "[[D]]",
            options["D"],
        ]
    )
    try:
        value = parse_structured_translation(translate_text(text, language))
    except ValueError:
        value = {
            "question": translate_text(source_question, language),
            **{
                letter: translate_text(options[letter], language)
                for letter in "ABCD"
            },
        }
    return record["stem_id"], value


def draft_batch(path: Path, language: str) -> None:
    records = load_jsonl(path)
    translated: dict[str, dict[str, str]] = {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(translate_record, record, language)
            for record in records
        ]
        for future in as_completed(futures):
            stem_id, value = future.result()
            translated[stem_id] = value

    output: list[dict[str, Any]] = []
    for record in records:
        value = translated[record["stem_id"]]
        updated = dict(record)
        updated["question"] = value["question"]
        updated["options"] = {
            letter: value[letter] for letter in "ABCD"
        }
        updated["wrong_suggestion_text"] = updated["options"][
            updated["wrong_suggestion_option"]
        ]
        updated["translation_status"] = "draft"
        updated["translator_note"] = "Machine-assisted draft; human review pending."
        updated["semantic_review"] = False
        updated["structural_review"] = False
        updated["review_note"] = ""
        updated["translation_method"] = "machine_assisted"
        updated["translation_system"] = TRANSLATION_SYSTEM
        updated["translation_date"] = TRANSLATION_DATE
        updated["human_reviewed"] = False
        output.append(updated)
    write_jsonl(path, output)
    print(f"Drafted {len(output)} records: {path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=LANGUAGES, nargs="+")
    parser.add_argument("--batch", type=int, nargs="+")
    arguments = parser.parse_args()
    languages = tuple(arguments.language or LANGUAGES)
    batches = arguments.batch or list(range(1, 13))
    for language in languages:
        for batch_number in batches:
            path = (
                BATCH_ROOT
                / language
                / f"translation_{language}_{batch_number:02d}.jsonl"
            )
            draft_batch(path, language)


if __name__ == "__main__":
    main()
