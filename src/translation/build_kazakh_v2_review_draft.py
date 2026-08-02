from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


SOURCE = Path("data/final/test_kk.jsonl")
ENGLISH_SOURCE = Path("data/final/test_en.jsonl")
OUTPUT = Path("data/final/test_kk_v2.jsonl")
CHANGE_LOG = Path(
    "reports/translation_audits/kazakh_v2_known_corrections.json"
)
CORRECTIONS: dict[str, dict[str, Any]] = {
    "master_logic_023": {
        "question": (
            "Барлық қызыл тақтайшалар ауыр. Ешбір жеңіл тақтайша ауыр "
            "емес. Қандай қорытынды міндетті түрде шығады?"
        ),
        "options": {
            "A": "Әрбір ауыр тақтайша қызыл",
            "B": "Ешбір жеңіл тақтайша қызыл емес",
            "C": "Кейбір қызыл тақтайшалар жеңіл",
            "D": "Әрбір қызыл емес тақтайша жеңіл",
        },
        "reason": "Restored the weight predicate and natural logical wording.",
    },
    "master_geo_078": {
        "question": "Өзен жайылмасы дегеніміз не?",
        "reason": "The original asked what a flood is, not what a floodplain is.",
    },
    "master_science_053": {
        "options": {"A": "Көтерілген ауа сығылады және жылынады"},
        "reason": "Corrected жылады (cried) to жылынады (warms).",
    },
    "master_logic_039": {
        "question": (
            "Рұқсат өтініш беруші тексеруден өткен жағдайда ғана "
            "беріледі. Ренге рұқсат берілді. Бұдан қандай қорытынды шығады?"
        ),
        "options": {"C": "Рен өтініш берген жоқ"},
        "reason": "Restored logical-consequence wording and option C meaning.",
    },
    "master_logic_054": {
        "question": (
            "A, C, F, J әріптерінің тізбегі әліпбиде алдымен 2, кейін "
            "3, одан соң 4 орынға ілгерілейді. Келесі әріп қайсы?"
        ),
        "options": {"D": "M"},
        "reason": "Corrected malformed sentence and Cyrillic М/Latin M mix.",
    },
    "master_geo_042": {
        "options": {"D": "Тропиктік жаңбырлы орман"},
        "reason": "Removed duplicated word in the tropical-rainforest option.",
    },
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> None:
    records = load_jsonl(SOURCE)
    english_records = load_jsonl(ENGLISH_SOURCE)
    if len(records) != 300:
        raise ValueError(f"Expected 300 records, found {len(records)}")
    if len(english_records) != 300:
        raise ValueError(
            f"Expected 300 English records, found {len(english_records)}"
        )
    english_by_id = {
        record["stem_id"]: record for record in english_records
    }
    changes: list[dict[str, Any]] = []
    cleaned_records: list[dict[str, Any]] = []
    for record in records:
        before = {
            "question": record["question"],
            "options": dict(record["options"]),
        }
        correction = CORRECTIONS.get(record["stem_id"])
        if correction:
            if "question" in correction:
                record["question"] = correction["question"]
            for option, text in correction.get("options", {}).items():
                record["options"][option] = text
            changes.append(
                {
                    "stem_id": record["stem_id"],
                    "reason": correction["reason"],
                    "before": before,
                    "after": {
                        "question": record["question"],
                        "options": record["options"],
                    },
                }
            )

        english = english_by_id[record["stem_id"]]
        record["wrong_suggestion_text"] = record["options"][
            record["wrong_suggestion_option"]
        ]
        cleaned_records.append({
            "stem_id": record["stem_id"],
            "source_stem_id": record["stem_id"],
            "language": "kk",
            "domain": record["domain"],
            "difficulty": record["difficulty"],
            "question": record["question"],
            "options": record["options"],
            "correct_option": record["correct_option"],
            "wrong_suggestion_option": record["wrong_suggestion_option"],
            "wrong_suggestion_text": record["wrong_suggestion_text"],
            "translation_status": "approved",
            "translation_method": "machine_assisted_with_author_review",
        })

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        "\n".join(
            json.dumps(record, ensure_ascii=False)
            for record in cleaned_records
        )
        + "\n",
        encoding="utf-8",
    )
    CHANGE_LOG.parent.mkdir(parents=True, exist_ok=True)
    CHANGE_LOG.write_text(
        json.dumps(
            {
                "version": "kazakh_translation_corrected_sensitivity_v2",
                "source_path": str(SOURCE),
                "source_sha256": digest(SOURCE),
                "corrected_path": str(OUTPUT),
                "corrected_sha256": digest(OUTPUT),
                "known_correction_count": len(changes),
                "changes": changes,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Draft records: {len(cleaned_records)}")
    print(f"Known corrections applied: {len(changes)}")


if __name__ == "__main__":
    main()
