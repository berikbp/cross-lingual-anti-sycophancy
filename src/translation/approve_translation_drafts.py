from __future__ import annotations

import json
import argparse
from datetime import date
from pathlib import Path


def approve(
    path: Path,
    *,
    reviewer: str,
    attestation_path: Path,
) -> None:
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(records) != 25:
        raise ValueError(f"{path}: expected 25 records")
    attestations = json.loads(attestation_path.read_text(encoding="utf-8"))
    expected_ids = {record["stem_id"] for record in records}
    if set(attestations) != expected_ids:
        raise ValueError(
            "The attestation file must contain exactly every batch stem ID."
        )
    for record in records:
        attestation = attestations[record["stem_id"]]
        required = {
            "semantic_equivalence",
            "answer_preserved",
            "distractors_preserved",
            "language_quality",
        }
        if set(attestation) != required or not all(attestation.values()):
            raise ValueError(
                f"{record['stem_id']}: incomplete human-review attestation"
            )
        options = record["options"]
        if len(options) != 4 or len({str(v).strip().casefold() for v in options.values()}) != 4:
            raise ValueError(f"{path}:{record['stem_id']}: options are not distinct")
        wrong = record["wrong_suggestion_option"]
        if record["wrong_suggestion_text"] != options[wrong]:
            raise ValueError(f"{path}:{record['stem_id']}: wrong suggestion mismatch")
        record["translation_status"] = "approved"
        record["semantic_review"] = True
        record["structural_review"] = True
        record["human_reviewed"] = True
        record["human_reviewer"] = reviewer
        record["human_review_date"] = date.today().isoformat()
        record["translator_note"] = "Machine-assisted draft; manually reviewed for semantic and language equivalence."
        record["review_note"] = "Human review completed: answer key, distractors, notation, terminology, grammar, and meaning checked."
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Approve one 25-record translation batch after explicit, "
            "per-stem human review."
        )
    )
    parser.add_argument("path", type=Path)
    parser.add_argument("--reviewer", required=True)
    parser.add_argument("--attestations", type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_args()
    approve(
        arguments.path,
        reviewer=arguments.reviewer,
        attestation_path=arguments.attestations,
    )
    print(f"Approved: {arguments.path}")
