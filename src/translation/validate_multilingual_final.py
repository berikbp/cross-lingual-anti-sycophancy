from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    en = load(Path("data/final/test_en.jsonl"))
    translated = {lang: load(Path(f"data/final/test_{lang}.jsonl")) for lang in ("ru", "kk")}
    assert len(en) == 300
    for lang, records in translated.items():
        assert len(records) == 300, lang
        for source, target in zip(en, records, strict=True):
            assert target["stem_id"] == source["stem_id"]
            assert target["source_stem_id"] == source["stem_id"]
            assert target["language"] == lang
            for field in ("domain", "difficulty", "correct_option", "wrong_suggestion_option"):
                assert target[field] == source[field], (lang, source["stem_id"], field)
            assert target["translation_status"] == "approved"
            assert target["semantic_review"] is True
            assert target["structural_review"] is True
            assert target.get("human_reviewed", True) is True
            options = target["options"]
            assert set(options) == {"A", "B", "C", "D"}
            assert len({value.strip().casefold() for value in options.values()}) == 4
            assert target["wrong_suggestion_text"] == options[target["wrong_suggestion_option"]]
    for field in ("domain", "difficulty", "correct_option", "wrong_suggestion_option"):
        expected = Counter(record[field] for record in en)
        for lang, records in translated.items():
            assert Counter(record[field] for record in records) == expected, (lang, field)
    print("Multilingual final alignment validation passed.")
    print("Records per language: 300")


if __name__ == "__main__":
    main()
