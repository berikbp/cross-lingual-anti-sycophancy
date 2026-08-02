from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import yaml

from src.analysis.analyze_final_multilingual import bootstrap, group, metrics


CONFIG = Path("configs/analysis/final_analysis_v1.yaml")
ROOT = Path("results/corrected_kazakh_v2")
OUT_JSON = Path("reports/corrected_kazakh_v2_metrics.json")
OUT_REPORT = Path("reports/corrected_kazakh_v2_analysis.md")
CONDITIONS = ("base", "control_v2", "selective_correction_v2")


def load(path: Path) -> list[dict]:
    records = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    for record in records:
        record["language"] = "kk"
    return records


def main() -> None:
    configuration = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    seed = configuration["analysis"]["bootstrap_seed"]
    samples = configuration["analysis"]["bootstrap_samples"]
    confidence_level = configuration["analysis"]["confidence_level"]
    records = {
        condition: load(ROOT / f"{condition}_kk.jsonl")
        for condition in CONDITIONS
    }
    output = {condition: metrics(rows) for condition, rows in records.items()}
    control = group(records["control_v2"])
    selective = group(records["selective_correction_v2"])
    ids = sorted(control)
    effects = np.array(
        [
            (
                int(control[item]["B0"]["branch_correct"])
                - int(control[item]["B2"]["branch_correct"])
            )
            - (
                int(selective[item]["B0"]["branch_correct"])
                - int(selective[item]["B2"]["branch_correct"])
            )
            for item in ids
        ],
        dtype=float,
    )
    paired = bootstrap(
        effects,
        seed,
        samples,
        confidence_level,
    )
    payload = {
        "analysis_name": "corrected_kazakh_v2_sensitivity",
        "historical_results_replaced": False,
        "models": output,
        "paired_control_minus_selective": paired,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    control_loss = 100 * output["control_v2"]["pressure_loss"]
    selective_loss = 100 * output["selective_correction_v2"]["pressure_loss"]
    lines = [
        "# Corrected Kazakh v2 sensitivity analysis",
        "",
        "This post-audit analysis uses the author-reviewed corrected Kazakh translation and the frozen language-revised Kazakh prompts. It does not replace the historical Stage 19 Kazakh evaluation.",
        "",
        "| Condition | B0 accuracy | B2 accuracy | Pressure loss |",
        "|---|---:|---:|---:|",
    ]
    for condition in CONDITIONS:
        result = output[condition]
        b0 = result["branches"]["B0"]["accuracy_all_records"]
        b2 = result["branches"]["B2"]["accuracy_all_records"]
        lines.append(
            f"| {condition} | {b0['count']}/{b0['denominator']} ({100*b0['rate']:.1f}%) | {b2['count']}/{b2['denominator']} ({100*b2['rate']:.1f}%) | {100*result['pressure_loss']:.1f} pp |"
        )
    lines += [
        "",
        f"Paired Control-v2 minus Selective-v2 effect: {100*paired['mean']:.1f} pp (95% bootstrap CI {100*paired['ci_95'][0]:.1f} to {100*paired['ci_95'][1]:.1f} pp).",
        "",
        f"Historical original-translation losses were 17.7 pp (Control-v2) and 19.3 pp (Selective-v2). Corrected losses are {control_loss:.1f} and {selective_loss:.1f} pp.",
        "",
        "Interpret the difference as sensitivity to the combined translation-and-prompt language correction, not as a preregistered replacement of the locked result or as the isolated effect of either change.",
    ]
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Corrected Kazakh v2 sensitivity analysis complete.")


if __name__ == "__main__":
    main()
