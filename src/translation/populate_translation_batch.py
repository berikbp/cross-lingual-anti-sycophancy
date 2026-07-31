from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("batch_path", type=Path)
    parser.add_argument("translations_path", type=Path)
    return parser.parse_args()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    arguments = parse_arguments()
    batch = load_jsonl(arguments.batch_path)
    translations = json.loads(
        arguments.translations_path.read_text(encoding="utf-8")
    )
    if not isinstance(translations, list):
        raise ValueError("Translation input must be a JSON list")
    if len(batch) != 25 or len(translations) != 25:
        raise ValueError("Batch and translation input must contain 25 items")

    for record, translated in zip(batch, translations, strict=True):
        if translated.get("stem_id") != record["stem_id"]:
            raise ValueError(
                f"Stem order mismatch: {translated.get('stem_id')} "
                f"!= {record['stem_id']}"
            )
        question = translated.get("question")
        options = translated.get("options")
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"{record['stem_id']}: empty question")
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError(
                f"{record['stem_id']}: options must be a four-item list"
            )

        record["question"] = question
        record["options"] = dict(zip("ABCD", options, strict=True))
        record["wrong_suggestion_text"] = record["options"][
            record["wrong_suggestion_option"]
        ]
        record["translation_status"] = "approved"
        record["translator_note"] = translated.get("translator_note", "")
        record["semantic_review"] = True
        record["structural_review"] = True
        record["review_note"] = translated.get("review_note", "")

    with arguments.batch_path.open("w", encoding="utf-8") as file:
        for record in batch:
            file.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"Populated and approved {len(batch)} records: {arguments.batch_path}")


if __name__ == "__main__":
    main()
