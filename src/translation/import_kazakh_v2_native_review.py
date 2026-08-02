from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


DRAFT = Path("data/translation/review/kazakh_v2_review_draft.jsonl")
DEFAULT_WORKSHEET = Path(
    "reports/translation_audits/kazakh_v2_native_review.csv"
)
DEFAULT_OUTPUT = Path(
    "data/translation/review/kazakh_v2_native_reviewed.jsonl"
)
LETTERS = ("A", "B", "C", "D")
APPROVAL_FIELDS = (
    "semantic_equivalence",
    "answer_preserved",
    "distractors_preserved",
    "language_quality",
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def load_worksheet(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def import_review(
    draft: list[dict[str, Any]],
    worksheet: list[dict[str, str]],
) -> list[dict[str, Any]]:
    if len(draft) != 300 or len(worksheet) != 300:
        raise ValueError("Expected 300 draft and worksheet records.")
    if len({row["stem_id"] for row in worksheet}) != 300:
        raise ValueError("Worksheet stem IDs are not unique.")
    worksheet_by_id = {row["stem_id"]: row for row in worksheet}
    reviewed: list[dict[str, Any]] = []

    for original in draft:
        stem_id = original["stem_id"]
        if stem_id not in worksheet_by_id:
            raise ValueError(f"{stem_id}: missing from worksheet")
        row = worksheet_by_id[stem_id]
        for field in APPROVAL_FIELDS:
            if row.get(field, "").strip().casefold() != "yes":
                raise ValueError(f"{stem_id}: {field} is not yes")
        if row.get("decision", "").strip().casefold() != "approved":
            raise ValueError(f"{stem_id}: decision is not approved")
        reviewer = row.get("reviewer", "").strip()
        review_date = row.get("review_date", "").strip()
        review_note = row.get("review_note", "").strip()
        if not reviewer or not review_date or not review_note:
            raise ValueError(
                f"{stem_id}: reviewer, review_date, and review_note are required"
            )

        record = dict(original)
        record["options"] = dict(original["options"])
        record["question"] = row.get("kazakh_question", "").strip()
        if not record["question"]:
            raise ValueError(f"{stem_id}: Kazakh question is empty")
        for letter in LETTERS:
            value = row.get(f"kazakh_{letter}", "").strip()
            if not value:
                raise ValueError(f"{stem_id}: Kazakh option {letter} is empty")
            record["options"][letter] = value
        if len(
            {value.casefold() for value in record["options"].values()}
        ) != 4:
            raise ValueError(f"{stem_id}: Kazakh options are not distinct")

        record["wrong_suggestion_text"] = record["options"][
            record["wrong_suggestion_option"]
        ]
        record["translation_status"] = "approved"
        record["semantic_review"] = True
        record["structural_review"] = True
        record["human_reviewed"] = True
        record["human_reviewer"] = reviewer
        record["human_review_date"] = review_date
        record["review_note"] = review_note
        record["translator_note"] = (
            "Machine-assisted draft with independent native-Kazakh review."
        )
        reviewed.append(record)

    return reviewed


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import an explicitly approved native-Kazakh worksheet."
    )
    parser.add_argument("--worksheet", type=Path, default=DEFAULT_WORKSHEET)
    parser.add_argument("--draft", type=Path, default=DRAFT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    arguments = parser.parse_args()

    reviewed = import_review(
        load_jsonl(arguments.draft),
        load_worksheet(arguments.worksheet),
    )
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        "\n".join(
            json.dumps(record, ensure_ascii=False) for record in reviewed
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Imported native-reviewed Kazakh records: {len(reviewed)}")


if __name__ == "__main__":
    main()
