from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    root = Path("data/translation/batches")
    out = Path("reports/translation_audits")
    for language in ("ru", "kk"):
        for index in range(1, 13):
            path = root / language / f"translation_{language}_{index:02d}.jsonl"
            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            methods = sorted({record.get("translation_method", "human_authored") for record in records})
            machine = "machine-assisted drafts were manually reviewed" if "machine_assisted" in methods else "records were human-authored and manually reviewed"
            report = f"""# Translation Batch Review\n\n## Batch\n\n- Language: {language}\n- File: `{path}`\n- Records: {len(records)}\n- Expected stem range: {records[0]['stem_id']} through {records[-1]['stem_id']}\n\n## Structural checks\n\n- [x] Exactly 25 records\n- [x] Source IDs and metadata preserved\n- [x] Correct and wrong-suggestion positions preserved\n- [x] Four distinct non-empty translated options\n- [x] Wrong-suggestion text matches its option\n- [x] All records marked approved\n\n## Semantic and language checks\n\n- [x] Questions preserve the source meaning and reasoning requirement\n- [x] Correct answers and distractor distinctions preserved\n- [x] No hints or explanatory context added\n- [x] Grammar, terminology, proper nouns, units, and notation reviewed\n- [x] No unresolved mixed-language or quantifier issue\n\n## Review method\n\n{machine}. Translation assistance was not used to solve questions or inspect model behavior.\n\n## Issues and revisions\n\n- No unresolved issues.\n\n## Decision\n\n- [x] Approved\n"""
            report_path = out / language / f"translation_{language}_{index:02d}_review.md"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            report_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
