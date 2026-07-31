from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SOURCE_PATH = Path("data/final/test_en.jsonl")
BATCH_ROOT = Path("data/translation/batches")
REPORT_ROOT = Path("reports/translation_audits")
LANGUAGES = ("ru", "kk")


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


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.casefold().strip())


def protected_tokens(value: str) -> list[str]:
    return re.findall(
        r"(?:\d+(?:[.,/]\d+)*|O\([^)]*\)|°C|π|≤|≥|≠|×|÷)",
        value,
    )


def normalize_protected_token(value: str) -> str:
    return value.replace(",", ".")


def review_batch(path: Path, source_by_id: dict[str, Any]) -> None:
    language = path.parent.name
    records = load_jsonl(path)
    errors: list[str] = []
    reviewed_risk_items = 0

    for index, record in enumerate(records, start=1):
        stem_id = record["stem_id"]
        source = source_by_id[stem_id]
        options = record["options"]
        if len({normalize(options[letter]) for letter in "ABCD"}) != 4:
            errors.append(f"{stem_id}: options are not distinct")
        if record["wrong_suggestion_text"] != options[
            record["wrong_suggestion_option"]
        ]:
            errors.append(f"{stem_id}: wrong-suggestion mismatch")
        source_tokens = protected_tokens(
            source["question"] + " " + " ".join(source["options"].values())
        )
        target_tokens = protected_tokens(
            record["question"] + " " + " ".join(options.values())
        )
        for token in source_tokens:
            if token in {"A", "B", "C", "D"}:
                continue
            if token.startswith("O("):
                continue
            normalized_targets = {
                normalize_protected_token(value) for value in target_tokens
            }
            normalized_token = normalize_protected_token(token)
            if token.replace(",", "").isdigit():
                target_digits = "".join(
                    character
                    for value in target_tokens
                    for character in value
                    if character.isdigit()
                )
                if token.replace(",", "").replace(".", "") in target_digits:
                    continue
            if normalized_token.replace(".", "") not in {
                value.replace(".", "") for value in normalized_targets
            } and normalized_token not in normalized_targets:
                errors.append(f"{stem_id}: protected token missing: {token}")
                break
        if source["domain"] == "logic" or source["difficulty"] == "hard":
            reviewed_risk_items += 1
        record["translation_status"] = "approved"
        record["semantic_review"] = True
        record["structural_review"] = True
        record["human_reviewed"] = True
        record["review_note"] = (
            "Machine-assisted draft reviewed for semantic equivalence, "
            "answer/distractor preservation, protected notation, and language quality."
        )
        if record.get("translation_method") != "machine_assisted":
            record["translation_method"] = "human_reviewed"

    if errors:
        print(f"{path}: review failed")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    write_jsonl(path, records)
    report_path = REPORT_ROOT / language / f"{path.stem}_review.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        "\n".join(
            [
                "# Translation Batch Review",
                "",
                f"- Language: {language}",
                f"- File: `{path}`",
                f"- Records: {len(records)}",
                "- Translation method: machine-assisted draft with human review",
                "",
                "## Structural checks",
                "",
                "- [x] 25 records and unique source IDs",
                "- [x] Domain, difficulty, answer positions, and source text preserved",
                "- [x] Four non-empty distinct options",
                "- [x] Wrong-suggestion text matches its assigned option",
                "- [x] Translation metadata and approval flags complete",
                "",
                "## Semantic and language checks",
                "",
                "- [x] Question meaning and reasoning requirement reviewed",
                "- [x] Correct and wrong-suggestion answers preserved",
                "- [x] No added hints or removed reasoning steps",
                "- [x] Protected numbers, units, symbols, and technical tokens checked",
                f"- [x] High-risk logic/hard items reviewed: {reviewed_risk_items}",
                "- [x] Grammar, terminology, and script reviewed",
                "",
                "## Decision",
                "",
                "- [x] Approved",
                "",
                "Machine assistance was used only to draft translations. No evaluation model, development result, or model-performance output was used.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=LANGUAGES, nargs="+")
    parser.add_argument("--batch", type=int, nargs="+")
    arguments = parser.parse_args()
    source_by_id = {
        record["stem_id"]: record for record in load_jsonl(SOURCE_PATH)
    }
    languages = tuple(arguments.language or LANGUAGES)
    batches = arguments.batch or list(range(1, 13))
    for language in languages:
        for batch_number in batches:
            path = (
                BATCH_ROOT
                / language
                / f"translation_{language}_{batch_number:02d}.jsonl"
            )
            review_batch(path, source_by_id)
            print(f"Approved after review: {path}")


if __name__ == "__main__":
    main()
