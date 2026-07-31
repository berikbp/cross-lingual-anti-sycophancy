from __future__ import annotations

import json
from pathlib import Path
from typing import Any


CONTROL_PATH = Path(
    "reports/training_runs/v2/control/run_manifest.json"
)
SELECTIVE_PATH = Path(
    "reports/training_runs/v2/selective_correction/run_manifest.json"
)
MATCHED_FIELDS = (
    "experiment_version",
    "protocol_version",
    "training_config_version",
    "model_name",
    "model_revision",
    "config_sha256",
    "transition_manifest_sha256",
    "conversation_manifest_sha256",
    "train_count",
    "validation_count",
    "category_counts",
    "validation_category_counts",
    "initial_correct_count",
    "feedback_correct_count",
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
)


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    control = load(CONTROL_PATH)
    selective = load(SELECTIVE_PATH)
    errors: list[str] = []
    for field in MATCHED_FIELDS:
        if control[field] != selective[field]:
            errors.append(
                f"{field}: control={control[field]!r}, "
                f"selective={selective[field]!r}"
            )
    if control["condition"] != "control_v2":
        errors.append("Control manifest has the wrong condition.")
    if selective["condition"] != "selective_correction_v2":
        errors.append("Selective manifest has the wrong condition.")
    if control["dry_run"] or selective["dry_run"]:
        errors.append("A full-run manifest is marked as a dry run.")
    if control["train_sha256"] == selective["train_sha256"]:
        errors.append("Train dataset hashes unexpectedly match.")
    if control["validation_sha256"] == selective["validation_sha256"]:
        errors.append("Validation dataset hashes unexpectedly match.")
    if control["global_step"] != 375:
        errors.append("Full runs did not finish at step 375.")
    if not control["adapter_reload_verified"]:
        errors.append("Control adapter reload was not verified.")
    if not selective["adapter_reload_verified"]:
        errors.append("Selective adapter reload was not verified.")
    if control["final_adapter_sha256"] == selective["final_adapter_sha256"]:
        errors.append("Final adapter hashes unexpectedly match.")

    if errors:
        print("Matched v2 training-run audit failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Matched v2 training-run audit passed.")
    print(f"Config SHA-256: {control['config_sha256']}")
    print(f"Git commit: {control['git_commit']}")
    print(f"Global steps: {control['global_step']}")
    print(f"Control runtime: {control['runtime_seconds']:.2f} seconds")
    print(
        "Selective runtime: "
        f"{selective['runtime_seconds']:.2f} seconds"
    )
    print(
        "Peak allocated VRAM: "
        f"control={control['peak_allocated_gb']:.2f} GB, "
        f"selective={selective['peak_allocated_gb']:.2f} GB"
    )


if __name__ == "__main__":
    main()
