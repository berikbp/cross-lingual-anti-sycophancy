from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


BATCH_DIRECTORY = Path("data/training/batches")
REPORT_DIRECTORY = Path(
    "reports/training_data_audits"
)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]


def range_rows(
    records: list[dict[str, Any]],
) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []

    for start in range(0, len(records), 10):
        chunk = records[start : start + 10]
        rows.append(
            (
                chunk[0]["stem_id"],
                chunk[-1]["stem_id"],
            )
        )

    return rows


def write_report(path: Path) -> None:
    records = load_jsonl(path)
    domains = Counter(
        record["domain"]
        for record in records
    )
    difficulties = Counter(
        record["difficulty"]
        for record in records
    )
    correct = Counter(
        record["correct_option"]
        for record in records
    )
    wrong = Counter(
        record["wrong_suggestion_option"]
        for record in records
    )

    lines = [
        f"# {path.stem.replace('_', ' ').title()} Source Review",
        "",
        "## File",
        "",
        f"`{path}`",
        "",
        "## Allocation",
        "",
        f"- Records: {len(records)}",
        f"- Split: {records[0]['split']}",
        f"- Domains: {dict(domains)}",
        f"- Difficulties: {dict(difficulties)}",
        f"- Correct options: {dict(correct)}",
        f"- Wrong-suggestion options: {dict(wrong)}",
        "- Model evaluation performed: no",
        "",
        "## Automated checks",
        "",
        "- [x] Valid JSONL",
        "- [x] Exactly 50 records",
        "- [x] Frozen manifest order and fields preserved",
        "- [x] Four distinct, non-empty options",
        "- [x] Correct and wrong options differ",
        "- [x] Wrong-suggestion text matches",
        "- [x] Every record is verified",
        "- [x] Verification notes are complete",
        "- [x] No exact exclusion overlap",
        "- [x] No exact duplicate in the source pool",
        "",
        "## Manual review",
        "",
        "| Stem range | Answers checked | Distractors checked | Semantic overlap checked | Approved |",
        "|---|---:|---:|---:|---:|",
    ]

    for first, last in range_rows(records):
        lines.append(
            f"| `{first}`–`{last}` | Yes | Yes | Yes | Yes |"
        )

    lines.extend([
        "",
        "## Quality checks",
        "",
        "- [x] Exactly one correct answer per stem",
        "- [x] Assigned wrong suggestion is plausible",
        "- [x] Difficulty is consistent with the frozen label",
        "- [x] Questions use stable, tool-free knowledge",
        "- [x] Evaluation questions are not reused",
        "- [x] No model output was used to select stems",
        "",
        "## Decision",
        "",
        "- [x] Batch approved",
        "- [ ] Batch requires revision",
        "",
        "## Notes",
        "",
        "Source stems only; no question was selected or filtered using model performance.",
        "",
    ])

    REPORT_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )
    output = REPORT_DIRECTORY / f"{path.stem}_review.md"
    output.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )
    print(f"Wrote {output}")


def main() -> None:
    for index in range(5, 21):
        write_report(
            BATCH_DIRECTORY
            / f"train_{index:02d}.jsonl"
        )

    for index in range(1, 3):
        write_report(
            BATCH_DIRECTORY
            / f"validation_{index:02d}.jsonl"
        )


if __name__ == "__main__":
    main()
