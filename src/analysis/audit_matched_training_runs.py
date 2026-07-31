from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CONTROL_PATH = Path(
    "reports/training_runs/control/run_manifest.json"
)
ANTI_PATH = Path(
    "reports/training_runs/anti_sycophancy/run_manifest.json"
)

MATCHED_FIELDS = [
    "protocol_version",
    "training_config_version",
    "model_name",
    "model_revision",
    "config_sha256",
    "train_count",
    "validation_count",
    "epochs",
    "effective_batch_size",
    "expected_global_steps",
    "seed",
    "data_seed",
    "compute_dtype",
    "torch_version",
    "transformers_version",
    "cuda_version",
    "gpu_name",
    "global_step",
    "git_commit",
]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    control = load(CONTROL_PATH)
    anti = load(ANTI_PATH)
    errors: list[str] = []

    for field in MATCHED_FIELDS:
        if control[field] != anti[field]:
            errors.append(
                f"{field}: control={control[field]!r}, "
                f"anti={anti[field]!r}"
            )

    if control["condition"] != "control":
        errors.append("Control manifest has wrong condition.")
    if anti["condition"] != "anti_sycophancy":
        errors.append("Anti manifest has wrong condition.")
    if control["dry_run"] or anti["dry_run"]:
        errors.append("A full-run manifest is marked as a dry run.")
    if control["train_sha256"] == anti["train_sha256"]:
        errors.append("Train files unexpectedly have identical hashes.")
    if control["validation_sha256"] == anti["validation_sha256"]:
        errors.append(
            "Validation files unexpectedly have identical hashes."
        )
    if control["global_step"] != 375:
        errors.append("Full runs did not finish at step 375.")

    if errors:
        print("Matched-run audit failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Matched-run audit passed.")
    print(f"Config SHA-256: {control['config_sha256']}")
    print(f"Git commit: {control['git_commit']}")
    print(f"Global steps: {control['global_step']}")
    print(f"Control runtime: {control['runtime_seconds']:.2f} seconds")
    print(f"Anti runtime: {anti['runtime_seconds']:.2f} seconds")
    print(
        "Control peak allocated: "
        f"{control['peak_allocated_gb']:.2f} GB"
    )
    print(
        "Anti peak allocated: "
        f"{anti['peak_allocated_gb']:.2f} GB"
    )


if __name__ == "__main__":
    main()
