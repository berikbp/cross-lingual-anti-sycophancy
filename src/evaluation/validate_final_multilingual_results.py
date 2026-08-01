from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

CONDITIONS = ("base", "control_v2", "selective_correction_v2")
LANGUAGES = ("en", "ru", "kk")
BRANCHES = {"B0", "B1", "B2", "B3"}


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> None:
    expected = {r["stem_id"] for r in load(Path("data/final/test_en.jsonl"))}
    total = 0
    for condition in CONDITIONS:
        for language in LANGUAGES:
            path = Path("results/final_multilingual_v1") / f"{condition}_{language}.jsonl"
            records = load(path)
            assert len(records) == 1200, path
            assert {r["stem_id"] for r in records} == expected
            pairs = {(r["stem_id"], r["branch"]) for r in records}
            assert len(pairs) == 1200
            assert Counter(r["branch"] for r in records) == {b: 300 for b in BRANCHES}
            for stem in expected:
                subset = [r for r in records if r["stem_id"] == stem]
                assert len({r["initial_raw_response"] for r in subset}) == 1
            total += len(records)
    assert total == 10800
    print("Final multilingual result validation passed.")


if __name__ == "__main__":
    main()
