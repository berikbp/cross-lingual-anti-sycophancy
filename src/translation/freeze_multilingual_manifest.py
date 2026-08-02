from __future__ import annotations

import hashlib
import json
from pathlib import Path


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    raise RuntimeError(
        "multilingual_final_v1 is a frozen historical artifact. Its Kazakh "
        "review claim was withdrawn after publication audit. Use "
        "src.translation.finalize_kazakh_v2 after complete native review; "
        "do not regenerate the historical manifest."
    )


def historical_implementation_for_provenance() -> dict[str, object]:
    """Return the old manifest payload without writing it.

    This function preserves the original construction logic for auditability.
    The review-complete field records what the workflow claimed in 2026-07;
    it is not a current semantic-review conclusion.
    """
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
    return manifest


if __name__ == "__main__":
    main()
