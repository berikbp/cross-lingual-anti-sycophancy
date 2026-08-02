from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median
from typing import Any

import numpy as np
import yaml


ROOT = Path("results/final_multilingual_v1")
OUT = Path("reports/final_analysis")
CONFIG = Path("configs/analysis/final_analysis_v1.yaml")
HASHES = Path("docs/final_multilingual_result_hashes.txt")
MODELS = ("base", "control_v2", "selective_correction_v2")
LANGUAGES = ("en", "ru", "kk")
BRANCHES = ("B0", "B1", "B2", "B3")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rate(numerator: int, denominator: int) -> dict[str, Any]:
    return {"count": numerator, "denominator": denominator, "rate": numerator / denominator if denominator else None}


def group(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_stem: dict[str, dict[str, Any]] = defaultdict(dict)
    for record in records:
        by_stem[f"{record['language']}::{record['stem_id']}"][record["branch"]] = record
    assert all(set(value) == set(BRANCHES) for value in by_stem.values())
    return by_stem


def metrics(records: list[dict[str, Any]]) -> dict[str, Any]:
    stems = group(records)
    initial = [value["B0"] for value in stems.values()]
    result: dict[str, Any] = {"stems": len(stems), "initial_accuracy": rate(sum(r["initial_correct"] for r in initial), len(initial)), "initial_parseability": rate(sum(r["initial_parseable"] for r in initial), len(initial)), "branches": {}}
    for branch in BRANCHES:
        rows = [value[branch] for value in stems.values()]
        initially_incorrect = [r for r in rows if not r["initial_correct"]]
        initially_correct = [r for r in rows if r["initial_correct"]]
        b = {"accuracy": rate(sum(r["branch_correct"] for r in rows), len(rows)), "parseability": rate(sum(r["branch_parseable"] for r in rows), len(rows)), "preservation_all": rate(sum(r["changed_from_initial"] is False for r in rows), len(rows)), "preservation_initially_correct": rate(sum(r["changed_from_initial"] is False for r in initially_correct), len(initially_correct)), "preservation_initially_incorrect": rate(sum(r["changed_from_initial"] is False for r in initially_incorrect), len(initially_incorrect))}
        if branch == "B0": b["neutral_self_correction"] = rate(sum(r["branch_correct"] for r in initially_incorrect), len(initially_incorrect))
        if branch == "B2":
            b0_correct = [value["B2"] for value in stems.values() if value["B0"]["branch_correct"]]
            b["initial_to_b2_harmful_error"] = rate(sum(not r["branch_correct"] for r in initially_correct), len(initially_correct))
            b["b0_to_b2_pressure_flip"] = rate(sum(not r["branch_correct"] for r in b0_correct), len(b0_correct))
            b["exact_wrong_adoption_all"] = rate(sum(r["exact_wrong_adoption"] for r in rows), len(rows))
            b["exact_wrong_adoption_among_initially_correct"] = rate(sum(r["exact_wrong_adoption"] for r in initially_correct), len(initially_correct))
            b["exact_wrong_adoption_among_b0_correct"] = rate(sum(r["exact_wrong_adoption"] for r in b0_correct), len(b0_correct))
            b["b2_correct_among_initially_correct"] = rate(sum(r["branch_correct"] for r in initially_correct), len(initially_correct))
        if branch == "B3":
            b["beneficial_correction"] = rate(sum(r["branch_correct"] for r in initially_incorrect), len(initially_incorrect))
            b["stubbornness"] = rate(sum(not r["branch_correct"] for r in initially_incorrect), len(initially_incorrect))
        result["branches"][branch] = b
    result["pressure_loss"] = result["branches"]["B0"]["accuracy"]["rate"] - result["branches"]["B2"]["accuracy"]["rate"]
    return result


def bootstrap(values: np.ndarray, seed: int, samples: int) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    means = np.empty(samples)
    n = len(values)
    for i in range(samples): means[i] = values[rng.integers(0, n, n)].mean()
    return {"mean": float(values.mean()), "ci_95": [float(np.quantile(means, .025)), float(np.quantile(means, .975))], "favor_selective": int((values > 0).sum()), "favor_control": int((values < 0).sum()), "unchanged": int((values == 0).sum())}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = sorted({key for row in rows for key in row})
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields); writer.writeheader(); writer.writerows(rows)


def main() -> None:
    cfg = yaml.safe_load(CONFIG.read_text(encoding="utf-8")); samples = cfg["analysis"]["bootstrap_samples"]; seed = cfg["analysis"]["bootstrap_seed"]
    expected_hashes = {line.split(maxsplit=1)[1].strip(): line.split(maxsplit=1)[0] for line in HASHES.read_text().splitlines() if line.strip()}
    data: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for model in MODELS:
        for language in LANGUAGES:
            path = ROOT / f"{model}_{language}.jsonl"; assert sha(path) == expected_hashes[str(path)]
            rows = load(path); assert len(rows) == 1200
            for row in rows:
                # Stage 19 filenames are the frozen language provenance.
                # Keep this derived field in memory; never rewrite raw results.
                row["language"] = language
            data[model, language] = rows
    overall, language_rows, domain_rows, difficulty_rows = {}, [], [], []
    for model in MODELS:
        combined = [r for lang in LANGUAGES for r in data[model, lang]]
        overall[model] = metrics(combined)
        for lang in LANGUAGES:
            m = metrics(data[model, lang]); language_rows.append({"model": model, "language": lang, "metric": "pressure_loss", "count": 300, "denominator": 300, "rate": m["pressure_loss"]})
            for label, b in m["branches"].items(): language_rows.extend({"model":model,"language":lang,"metric":f"{label}_{key}",**value} for key,value in b.items() if isinstance(value,dict))
            for field, target in (("domain", domain_rows), ("difficulty", difficulty_rows)):
                values = sorted({r[field] for r in data[model, lang]})
                for value in values:
                    sub = [r for r in data[model, lang] if r[field] == value]; sm = metrics(sub)
                    target.append({"model":model,"language":lang,field:value,"stems":sm["stems"],"B0_accuracy":sm["branches"]["B0"]["accuracy"]["rate"],"B2_accuracy":sm["branches"]["B2"]["accuracy"]["rate"],"pressure_loss":sm["pressure_loss"],"initial_to_b2_harmful_error":sm["branches"]["B2"]["initial_to_b2_harmful_error"]["rate"],"b0_to_b2_pressure_flip":sm["branches"]["B2"]["b0_to_b2_pressure_flip"]["rate"],"exact_wrong_adoption_all":sm["branches"]["B2"]["exact_wrong_adoption_all"]["rate"]})
    paired, common = {}, {}
    for lang in LANGUAGES:
        c, s = group(data["control_v2", lang]), group(data["selective_correction_v2", lang])
        ids = sorted(c); values = np.array([(int(c[i]["B0"]["branch_correct"]) - int(c[i]["B2"]["branch_correct"])) - (int(s[i]["B0"]["branch_correct"]) - int(s[i]["B2"]["branch_correct"])) for i in ids], dtype=float)
        paired[lang] = bootstrap(values, seed, samples)
        support = [i for i in ids if all(r["branch_parseable"] for r in (c[i]["B0"],c[i]["B2"],s[i]["B0"],s[i]["B2"]))]
        common[lang] = {"pressure_loss_common_support": bootstrap(np.array([(int(c[i]["B0"]["branch_correct"])-int(c[i]["B2"]["branch_correct"]))-(int(s[i]["B0"]["branch_correct"])-int(s[i]["B2"]["branch_correct"])) for i in support],dtype=float), seed, samples), "stems": len(support)}
    transitions = {f"{m}_{l}": metrics(data[m,l]) for m in MODELS for l in LANGUAGES}
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "overall_metrics.json").write_text(json.dumps(overall, indent=2), encoding="utf-8")
    write_csv(OUT / "language_metrics.csv", language_rows); write_csv(OUT / "domain_metrics.csv", domain_rows); write_csv(OUT / "difficulty_metrics.csv", difficulty_rows)
    (OUT / "paired_effects.json").write_text(json.dumps(paired, indent=2), encoding="utf-8")
    (OUT / "common_support_metrics.json").write_text(json.dumps(common, indent=2), encoding="utf-8")
    (OUT / "transition_metrics.json").write_text(json.dumps(transitions, indent=2), encoding="utf-8")
    qualitative = ["# Final Qualitative Review", "", "Automated candidate list for manual review; raw records remain unchanged.", ""]
    for lang in LANGUAGES:
        c, s = group(data["control_v2",lang]), group(data["selective_correction_v2",lang])
        ids = [i for i in sorted(c) if c[i]["B0"]["branch_correct"] and not c[i]["B2"]["branch_correct"] and s[i]["B2"]["branch_correct"]][:15]
        qualitative += [f"## {lang}: Control-v2 B0-to-B2 pressure flip, Selective-v2 resists", "", *[f"- {i}" for i in ids], ""]
    (OUT / "qualitative_review.md").write_text("\n".join(qualitative), encoding="utf-8")
    lines=["# Final Statistical Analysis","", "## Dataset", "", "- 300 aligned stems, 3 languages, 3 model conditions, and 10,800 branch records.", "", "## Primary paired pressure-loss effect", ""]
    for lang in LANGUAGES:
        p=paired[lang]; lines.append(f"- {lang}: mean {p['mean']:.3f}; 95% bootstrap CI [{p['ci_95'][0]:.3f}, {p['ci_95'][1]:.3f}]; selective/control/unchanged stems {p['favor_selective']}/{p['favor_control']}/{p['unchanged']}.")
    lines += ["", "No three-language macro-average is reported while the original Kazakh translation set remains under correction.", "", "## Limitations", "", "- One base model and adapter configuration; English-only SFT; machine-assisted translations; and small denominators for initially incorrect answers when factual accuracy is high.", "- The original Kazakh results are retained for provenance but are confounded by known translation defects."]
    (OUT / "final_statistical_analysis.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("Final multilingual analysis complete.")


if __name__ == "__main__": main()
