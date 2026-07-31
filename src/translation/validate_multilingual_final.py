from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


ENGLISH = Path("data/final/test_en.jsonl")
TRANSLATED = {
    "ru": Path("data/final/test_ru.jsonl"),
    "kk": Path("data/final/test_kk.jsonl"),
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    english = load_jsonl(ENGLISH)
    if len(english) != 300:
        raise ValueError(f"Expected 300 English records, found {len(english)}")
    english_by_id = {record["stem_id"]: record for record in english}
    english_ids = [record["stem_id"] for record in english]
    expected_distribution = {
        field: Counter(record[field] for record in english)
        for field in ("domain", "difficulty", "correct_option", "wrong_suggestion_option")
    }

    for language, path in TRANSLATED.items():
        records = load_jsonl(path)
        if len(records) != 300:
            raise ValueError(f"{language}: expected 300 records, found {len(records)}")
        ids = [record["stem_id"] for record in records]
        if ids != english_ids:
            raise ValueError(f"{language}: stem order differs from English")
        if len(set(ids)) != 300:
            raise ValueError(f"{language}: duplicate stem IDs")
        if any(record.get("language") != language for record in records):
            raise ValueError(f"{language}: language metadata mismatch")

        for record in records:
            source = english_by_id[record["stem_id"]]
            for field in (
                "domain",
                "difficulty",
                "correct_option",
                "wrong_suggestion_option",
            ):
                if record[field] != source[field]:
                    raise ValueError(
                        f"{language}/{record['stem_id']}: {field} mismatch"
                    )
            options = record["options"]
            if set(options) != {"A", "B", "C", "D"}:
                raise ValueError(f"{language}/{record['stem_id']}: option labels mismatch")
            if any(not isinstance(options[key], str) or not options[key].strip() for key in options):
                raise ValueError(f"{language}/{record['stem_id']}: empty option")
            if record["wrong_suggestion_text"] != options[record["wrong_suggestion_option"]]:
                raise ValueError(f"{language}/{record['stem_id']}: wrong-suggestion text mismatch")
            if record.get("translation_status") != "approved":
                raise ValueError(f"{language}/{record['stem_id']}: not approved")
            if record.get("semantic_review") is not True or record.get("structural_review") is not True:
                raise ValueError(f"{language}/{record['stem_id']}: review flags incomplete")
            # The original approved Russian batches (01–08) predate the
            # provenance fields and are protected by frozen hashes. Explicit
            # provenance is required for machine-assisted records.
            if (
                record.get("translation_method") == "machine_assisted"
                and record.get("human_reviewed") is not True
            ):
                raise ValueError(f"{language}/{record['stem_id']}: human review missing")

        for field, expected in expected_distribution.items():
            actual = Counter(record[field] for record in records)
            if actual != expected:
                raise ValueError(f"{language}: {field} distribution mismatch")
        print(
            f"{language}: 300 records aligned; distributions and review flags passed"
        )

    print("\nMultilingual final alignment validation passed.")


if __name__ == "__main__":
    main()
