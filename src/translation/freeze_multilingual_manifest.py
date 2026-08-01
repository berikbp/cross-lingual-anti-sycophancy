from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    files = {key: Path(value) for key, value in {
        "english": "data/final/test_en.jsonl",
        "russian": "data/final/test_ru.jsonl",
        "kazakh": "data/final/test_kk.jsonl",
        "split_manifest": "data/final/split_manifest.json",
    }.items()}
    manifest = {
        "version": "multilingual_final_v1",
        "protocol_version": "2.0",
        "stem_count": 300,
        "languages": ["en", "ru", "kk"],
        "english_path": str(files["english"]),
        "russian_path": str(files["russian"]),
        "kazakh_path": str(files["kazakh"]),
        "english_sha256": sha(files["english"]),
        "russian_sha256": sha(files["russian"]),
        "kazakh_sha256": sha(files["kazakh"]),
        "split_manifest_sha256": sha(files["split_manifest"]),
        "replacement_count": 0,
        "replacement_log_path": "reports/translation_audits/replacement_log.md",
        "translation_assistance": {"method": "machine-assisted translation with human semantic verification", "system": "Google Translate web endpoint (GTX)", "access_date": "2026-07-31"},
        "translation_review_complete": True,
        "model_inference_performed": False,
    }
    out = Path("data/final/multilingual_manifest.json")
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)


if __name__ == "__main__":
    main()
