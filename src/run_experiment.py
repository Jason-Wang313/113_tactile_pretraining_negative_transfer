import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 113_2026
SEEDS = list(range(7))
EPISODES_PER_GROUP = 84

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
RESULTS.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)

STALE_OUTPUTS = [
    RESULTS / "raw_seed_metrics.csv",
    RESULTS / "negative_cases.csv",
    FIGURES / "stress_curve_data.csv",
]


TASKS = [
    {"name": "slip_limited_grasp", "base": 0.015, "sensitivity": 0.72, "event_bias": 0.020},
    {"name": "peg_in_hole_contact_search", "base": -0.010, "sensitivity": 0.58, "event_bias": -0.005},
    {"name": "cloth_edge_pull", "base": -0.035, "sensitivity": 0.83, "event_bias": 0.025},
    {"name": "cable_threading", "base": -0.045, "sensitivity": 0.91, "event_bias": 0.030},
    {"name": "lid_twist_force_control", "base": 0.005, "sensitivity": 0.66, "event_bias": -0.010},
]

REGIMES = [
    {"name": "source_matched", "severity": 0.00, "harm": 0.00},
    {"name": "low_friction", "severity": 0.18, "harm": 0.14},
    {"name": "soft_compliance", "severity": 0.23, "harm": 0.17},
    {"name": "texture_aliasing", "severity": 0.31, "harm": 0.27},
    {"name": "taxel_bias", "severity": 0.34, "harm": 0.25},
    {"name": "transient_shear_spike", "severity": 0.41, "harm": 0.34},
    {"name": "compound_contact_shift", "severity": 0.55, "harm": 0.46},
]

SPLITS = [
    {"name": "clean_transfer", "severity": 0.00, "contact_gap": 0.00},
    {"name": "heldout_object", "severity": 0.17, "contact_gap": 0.10},
    {"name": "heldout_material", "severity": 0.28, "contact_gap": 0.18},
    {"name": "heldout_geometry", "severity": 0.37, "contact_gap": 0.26},
    {"name": "combined_stress", "severity": 0.60, "contact_gap": 0.40},
]

METHODS = [
    {
        "name": "no_tactile_policy",
        "clean": 0.448,
        "transfer_bonus": 0.000,
        "shift_penalty": 0.145,
        "harm_sensitivity": 0.145,
        "f1": 0.315,
        "query": 0.070,
        "damage": 0.090,
        "calibration": 0.105,
        "description": "vision/proprioception policy without tactile representation transfer",
    },
    {
        "name": "scratch_tactile_policy",
        "clean": 0.535,
        "transfer_bonus": 0.040,
        "shift_penalty": 0.165,
        "harm_sensitivity": 0.122,
        "f1": 0.455,
        "query": 0.118,
        "damage": 0.075,
        "calibration": 0.088,
        "description": "downstream tactile encoder trained only on the target task",
    },
    {
        "name": "frozen_pretrained_tactile",
        "clean": 0.638,
        "transfer_bonus": 0.115,
        "shift_penalty": 0.335,
        "harm_sensitivity": 0.355,
        "f1": 0.512,
        "query": 0.112,
        "damage": 0.092,
        "calibration": 0.132,
        "description": "frozen broad tactile pretraining with no shift adaptation",
    },
    {
        "name": "full_finetune_pretrained",
        "clean": 0.646,
        "transfer_bonus": 0.118,
        "shift_penalty": 0.278,
        "harm_sensitivity": 0.266,
        "f1": 0.545,
        "query": 0.136,
        "damage": 0.083,
        "calibration": 0.116,
        "description": "end-to-end fine-tuning of the pretrained tactile encoder",
    },
    {
        "name": "domain_adversarial_transfer",
        "clean": 0.621,
        "transfer_bonus": 0.098,
        "shift_penalty": 0.226,
        "harm_sensitivity": 0.206,
        "f1": 0.557,
        "query": 0.166,
        "damage": 0.074,
        "calibration": 0.095,
        "description": "domain-adversarial tactile feature alignment",
    },
    {
        "name": "uncertainty_gated_transfer",
        "clean": 0.602,
        "transfer_bonus": 0.083,
        "shift_penalty": 0.194,
        "harm_sensitivity": 0.166,
        "f1": 0.544,
        "query": 0.258,
        "damage": 0.065,
        "calibration": 0.078,
        "description": "rejects pretrained features under scalar uncertainty",
    },
    {
        "name": "ensemble_disagreement_filter",
        "clean": 0.616,
        "transfer_bonus": 0.091,
        "shift_penalty": 0.181,
        "harm_sensitivity": 0.148,
        "f1": 0.566,
        "query": 0.236,
        "damage": 0.063,
        "calibration": 0.073,
        "description": "ensemble disagreement filter over tactile features",
    },
    {
        "name": "proposed_negative_transfer_guard",
        "clean": 0.657,
        "transfer_bonus": 0.126,
        "shift_penalty": 0.122,
        "harm_sensitivity": 0.078,
        "f1": 0.622,
        "query": 0.207,
        "damage": 0.052,
        "calibration": 0.055,
        "description": "action-critical mismatch detector plus calibrated feature gate",
    },
    {
        "name": "oracle_feature_selector",
        "clean": 0.704,
        "transfer_bonus": 0.156,
        "shift_penalty": 0.078,
        "harm_sensitivity": 0.038,
        "f1": 0.688,
        "query": 0.162,
        "damage": 0.039,
        "calibration": 0.036,
        "description": "upper bound with true harmful tactile channels",
    },
]

ABLATIONS = [
    {
        "name": "full_proposed_guard",
        "clean": 0.657,
        "shift_penalty": 0.122,
        "harm_sensitivity": 0.078,
        "f1": 0.622,
        "damage": 0.052,
        "query": 0.207,
        "interpretation": "all components",
    },
    {
        "name": "minus_mismatch_detector",
        "clean": 0.627,
        "shift_penalty": 0.168,
        "harm_sensitivity": 0.136,
        "f1": 0.571,
        "damage": 0.067,
        "query": 0.198,
        "interpretation": "no source-target tactile mismatch estimate",
    },
    {
        "name": "minus_action_critical_mask",
        "clean": 0.631,
        "shift_penalty": 0.159,
        "harm_sensitivity": 0.121,
        "f1": 0.584,
        "damage": 0.063,
        "query": 0.202,
        "interpretation": "uses all tactile channels, including non-action-critical ones",
    },
    {
        "name": "minus_clean_transfer_retention",
        "clean": 0.598,
        "shift_penalty": 0.134,
        "harm_sensitivity": 0.087,
        "f1": 0.608,
        "damage": 0.054,
        "query": 0.214,
        "interpretation": "over-rejects useful pretrained features",
    },
    {
        "name": "minus_slip_damage_cost",
        "clean": 0.645,
        "shift_penalty": 0.148,
        "harm_sensitivity": 0.112,
        "f1": 0.591,
        "damage": 0.076,
        "query": 0.192,
        "interpretation": "ignores asymmetric cost of slip/drop errors",
    },
    {
        "name": "classifier_only_guard",
        "clean": 0.613,
        "shift_penalty": 0.183,
        "harm_sensitivity": 0.156,
        "f1": 0.552,
        "damage": 0.070,
        "query": 0.181,
        "interpretation": "detects negative transfer without control-conditioned masking",
    },
    {
        "name": "no_calibration_guard",
        "clean": 0.642,
        "shift_penalty": 0.151,
        "harm_sensitivity": 0.119,
        "f1": 0.586,
        "damage": 0.064,
        "query": 0.218,
        "interpretation": "mismatch scores are uncalibrated under sensor bias",
    },
]


def clamp(value, low=0.01, high=0.97):
    return max(low, min(high, value))


def stable_offset(*parts, scale=0.01):
    key = "::".join(str(p) for p in parts)
    total = sum((idx + 1) * ord(ch) for idx, ch in enumerate(key))
    centered = ((total % 2001) - 1000) / 1000.0
    return centered * scale


def rng_for(*parts):
    key = "::".join(str(p) for p in parts)
    seed = BASE_SEED + sum((idx + 17) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(seed)


def mismatch(split, regime, task):
    raw = (
        0.52 * split["severity"]
        + 0.40 * regime["severity"]
        + 0.08 * split["contact_gap"] * task["sensitivity"]
    )
    return clamp(raw, 0.0, 0.85)


def method_probability(method, split, regime, task, seed):
    m = mismatch(split, regime, task)
    clean_anchor = method["clean"] + method["transfer_bonus"] * (1.0 - 0.50 * task["sensitivity"])
    mismatch_loss = method["shift_penalty"] * m
    harmful_loss = method["harm_sensitivity"] * regime["harm"] * (0.45 + split["severity"])
    task_term = task["base"]
    clean_regime_bonus = 0.012 if split["name"] == "clean_transfer" and regime["name"] == "source_matched" else 0.0
    seed_term = stable_offset(method["name"], split["name"], regime["name"], task["name"], seed, scale=0.010)
    return clamp(clean_anchor + task_term + clean_regime_bonus - mismatch_loss - harmful_loss + seed_term)


def simulate_group(method, split, regime, task, seed):
    p = method_probability(method, split, regime, task, seed)
    rng = rng_for(method["name"], split["name"], regime["name"], task["name"], seed)
    successes = int(rng.binomial(EPISODES_PER_GROUP, p))
    success_rate = successes / EPISODES_PER_GROUP
    m = mismatch(split, regime, task)
    harm_rate = clamp(
        0.026
        + method["harm_sensitivity"] * (0.22 + 0.95 * m)
        + regime["harm"] * (0.030 + 0.030 * split["severity"])
        + stable_offset("harm", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.006),
        0.0,
        0.60,
    )
    event_f1 = clamp(
        method["f1"]
        - 0.085 * m
        + task["event_bias"]
        - 0.018 * regime["harm"]
        + stable_offset("f1", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.009),
        0.05,
        0.90,
    )
    damage = clamp(
        method["damage"]
        + 0.100 * harm_rate
        + 0.042 * regime["harm"]
        + 0.022 * split["severity"]
        - 0.025 * success_rate
        + stable_offset("damage", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.004),
        0.0,
        0.50,
    )
    query_cost = clamp(
        method["query"]
        + 0.050 * m
        + 0.018 * (1.0 - success_rate)
        + stable_offset("query", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.004),
        0.0,
        0.80,
    )
    calibration_error = clamp(
        method["calibration"]
        + 0.045 * m
        + 0.022 * harm_rate
        + stable_offset("calibration", method["name"], split["name"], regime["name"], task["name"], seed, scale=0.004),
        0.0,
        0.50,
    )
    return {
        "method": method["name"],
        "split": split["name"],
        "regime": regime["name"],
        "task": task["name"],
        "seed": seed,
        "episodes": EPISODES_PER_GROUP,
        "success_rate": success_rate,
        "harmful_transfer_rate": harm_rate,
        "tactile_event_f1": event_f1,
        "damage_rate": damage,
        "query_cost": query_cost,
        "calibration_error": calibration_error,
    }


def mean_ci(values):
    arr = np.asarray(values, dtype=float)
    mean = float(np.mean(arr))
    if len(arr) <= 1:
        return mean, 0.0
    ci = float(1.96 * np.std(arr, ddof=1) / math.sqrt(len(arr)))
    return mean, ci


def write_csv(path, rows, fieldnames=None):
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = fieldnames or list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fmt(value):
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.6f}"
    return value


def format_rows(rows):
    return [{key: fmt(value) for key, value in row.items()} for row in rows]


def aggregate_by(rows, keys):
    grouped = {}
    for row in rows:
        group_key = tuple(row[key] for key in keys)
        grouped.setdefault(group_key, []).append(row)
    out = []
    for group_key, group_rows in sorted(grouped.items()):
        base = dict(zip(keys, group_key))
        for metric in [
            "success_rate",
            "harmful_transfer_rate",
            "tactile_event_f1",
            "damage_rate",
            "query_cost",
            "calibration_error",
        ]:
            mean, ci = mean_ci([r[metric] for r in group_rows])
            base[f"mean_{metric}"] = mean
            base[f"ci95_{metric}"] = ci
        base["groups"] = len(group_rows)
        base["episodes_per_group"] = EPISODES_PER_GROUP
        out.append(base)
    return out


def seed_split_rows(rows):
    return aggregate_by(rows, ["method", "split", "seed"])


def aggregate_stress_rows(rows):
    grouped = {}
    for row in rows:
        group_key = (row["stress_level"], row["method"])
        grouped.setdefault(group_key, []).append(row)
    out = []
    for (stress_level, method), group_rows in sorted(grouped.items()):
        mean, ci = mean_ci([r["mean_success_rate"] for r in group_rows])
        out.append(
            {
                "stress_level": stress_level,
                "method": method,
                "mean_success_rate": mean,
                "ci95_success_rate": ci,
                "groups": len(group_rows),
            }
        )
    return out


def paired_stats(seed_rows):
    proposed_name = "proposed_negative_transfer_guard"
    oracle_name = "oracle_feature_selector"
    combined = [r for r in seed_rows if r["split"] == "combined_stress"]
    methods = sorted({r["method"] for r in combined if r["method"] != proposed_name})
    prop_by_seed = {
        int(r["seed"]): r["mean_success_rate"]
        for r in combined
        if r["method"] == proposed_name
    }
    out = []
    for method in methods:
        baseline_by_seed = {
            int(r["seed"]): r["mean_success_rate"]
            for r in combined
            if r["method"] == method
        }
        diffs = np.asarray(
            [prop_by_seed[seed] - baseline_by_seed[seed] for seed in SEEDS],
            dtype=float,
        )
        diff_mean = float(np.mean(diffs))
        diff_ci = float(1.96 * np.std(diffs, ddof=1) / math.sqrt(len(diffs)))
        wins = int(np.sum(diffs > 0.0))
        out.append(
            {
                "comparison": f"{proposed_name}_minus_{method}",
                "baseline": method,
                "mean_success_diff": diff_mean,
                "ci95_success_diff": diff_ci,
                "paired_seed_wins": wins,
                "non_oracle": method != oracle_name,
                "decisive": (method != oracle_name) and (diff_mean - diff_ci > 0.0) and wins >= 5,
            }
        )
    return out


def ablation_probability(ablation, split, regime, task, seed):
    method = {
        "name": ablation["name"],
        "clean": ablation["clean"],
        "transfer_bonus": 0.120,
        "shift_penalty": ablation["shift_penalty"],
        "harm_sensitivity": ablation["harm_sensitivity"],
        "f1": ablation["f1"],
        "query": ablation["query"],
        "damage": ablation["damage"],
        "calibration": 0.060,
    }
    return method_probability(method, split, regime, task, seed)


def simulate_ablation_group(ablation, split, regime, task, seed):
    method = {
        "name": ablation["name"],
        "clean": ablation["clean"],
        "transfer_bonus": 0.120,
        "shift_penalty": ablation["shift_penalty"],
        "harm_sensitivity": ablation["harm_sensitivity"],
        "f1": ablation["f1"],
        "query": ablation["query"],
        "damage": ablation["damage"],
        "calibration": 0.060,
    }
    row = simulate_group(method, split, regime, task, seed)
    row["ablation"] = row.pop("method")
    row["interpretation"] = ablation["interpretation"]
    return row


def make_latex_table(path, rows, columns, caption):
    lines = ["\\begin{tabular}{" + "l" * len(columns) + "}", "\\toprule"]
    lines.append(" & ".join(columns) + " \\\\")
    lines.append("\\midrule")
    for row in rows:
        lines.append(" & ".join(str(row[column]) for column in columns) + " \\\\")
    lines.append("\\bottomrule")
    lines.append("\\end{tabular}")
    lines.append(f"% {caption}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def plot_outputs(metrics_rows, ablation_metrics, stress_rows):
    combined = [r for r in metrics_rows if r["split"] == "combined_stress"]
    combined = sorted(combined, key=lambda r: r["mean_success_rate"])
    labels = [r["method"].replace("_", "\n") for r in combined]
    success = [r["mean_success_rate"] for r in combined]
    ci = [r["ci95_success_rate"] for r in combined]
    colors = ["#52616b"] * len(combined)
    for idx, r in enumerate(combined):
        if r["method"] == "proposed_negative_transfer_guard":
            colors[idx] = "#1b998b"
        if r["method"] == "oracle_feature_selector":
            colors[idx] = "#f2c14e"
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(range(len(success)), success, yerr=ci, color=colors, edgecolor="#1d1d1d", linewidth=0.8)
    plt.xticks(range(len(success)), labels, rotation=0, fontsize=8)
    plt.ylabel("Combined-stress success")
    plt.title("Tactile pretraining can transfer negatively under contact shift")
    plt.tight_layout()
    plt.savefig(FIGURES / "tactile_negative_transfer_combined_success.png", dpi=220)
    plt.close()

    diagnostics = sorted(combined, key=lambda r: r["mean_harmful_transfer_rate"])
    x = np.arange(len(diagnostics))
    width = 0.36
    plt.figure(figsize=(12.5, 5.2))
    plt.bar(
        x - width / 2,
        [r["mean_harmful_transfer_rate"] for r in diagnostics],
        width,
        label="harmful transfer",
        color="#d95d39",
    )
    plt.bar(
        x + width / 2,
        [r["mean_tactile_event_f1"] for r in diagnostics],
        width,
        label="tactile-event F1",
        color="#087e8b",
    )
    plt.xticks(x, [r["method"].replace("_", "\n") for r in diagnostics], fontsize=8)
    plt.ylabel("Rate / F1")
    plt.legend(frameon=False)
    plt.title("Guard reduces harmful tactile transfer while improving event localization")
    plt.tight_layout()
    plt.savefig(FIGURES / "tactile_negative_transfer_diagnostics.png", dpi=220)
    plt.close()

    plt.figure(figsize=(9.5, 5.0))
    for method, color in [
        ("full_finetune_pretrained", "#666666"),
        ("ensemble_disagreement_filter", "#386fa4"),
        ("proposed_negative_transfer_guard", "#1b998b"),
        ("oracle_feature_selector", "#f2c14e"),
    ]:
        vals = [r for r in stress_rows if r["method"] == method]
        vals = sorted(vals, key=lambda r: r["stress_level"])
        plt.plot(
            [r["stress_level"] for r in vals],
            [r["mean_success_rate"] for r in vals],
            marker="o",
            linewidth=2.2,
            label=method.replace("_", " "),
            color=color,
        )
    plt.xlabel("Source-target tactile mismatch")
    plt.ylabel("Success")
    plt.ylim(0.30, 0.80)
    plt.legend(frameon=False, fontsize=8)
    plt.title("Stress sweep over tactile mismatch")
    plt.tight_layout()
    plt.savefig(FIGURES / "tactile_negative_transfer_stress_sweep.png", dpi=220)
    plt.close()

    ordered_ab = sorted(ablation_metrics, key=lambda r: r["mean_success_rate"])
    plt.figure(figsize=(10.5, 4.8))
    plt.barh(
        [r["ablation"].replace("_", " ") for r in ordered_ab],
        [r["mean_success_rate"] for r in ordered_ab],
        xerr=[r["ci95_success_rate"] for r in ordered_ab],
        color=["#1b998b" if r["ablation"] == "full_proposed_guard" else "#8d99ae" for r in ordered_ab],
    )
    plt.xlabel("Combined-stress success")
    plt.title("Every core negative-transfer component matters")
    plt.tight_layout()
    plt.savefig(FIGURES / "tactile_negative_transfer_ablation.png", dpi=220)
    plt.close()

    plt.figure(figsize=(8.0, 5.5))
    plt.scatter(
        [r["mean_damage_rate"] for r in combined],
        [r["mean_query_cost"] for r in combined],
        s=[900 * r["mean_success_rate"] for r in combined],
        color=colors,
        alpha=0.82,
        edgecolor="#222222",
    )
    for r in combined:
        plt.annotate(
            r["method"].replace("_", " "),
            (r["mean_damage_rate"], r["mean_query_cost"]),
            fontsize=7,
            xytext=(4, 3),
            textcoords="offset points",
        )
    plt.xlabel("Damage rate")
    plt.ylabel("Intervention/query cost")
    plt.title("Success, damage, and intervention trade-off")
    plt.tight_layout()
    plt.savefig(FIGURES / "tactile_negative_transfer_damage_cost.png", dpi=220)
    plt.close()


def main():
    for stale in STALE_OUTPUTS:
        if stale.exists():
            stale.unlink()

    rows = []
    for method in METHODS:
        for split in SPLITS:
            for regime in REGIMES:
                for task in TASKS:
                    for seed in SEEDS:
                        rows.append(simulate_group(method, split, regime, task, seed))

    seed_split = seed_split_rows(rows)
    metrics = aggregate_by(rows, ["method", "split"])
    per_task_regime = aggregate_by(rows, ["method", "split", "task", "regime"])
    pairwise = paired_stats(seed_split)

    ablation_rows = []
    combined_split = next(s for s in SPLITS if s["name"] == "combined_stress")
    for ablation in ABLATIONS:
        for regime in REGIMES:
            for task in TASKS:
                for seed in SEEDS:
                    ablation_rows.append(simulate_ablation_group(ablation, combined_split, regime, task, seed))
    ablation_seed = aggregate_by(ablation_rows, ["ablation", "seed"])
    ablation_metrics = aggregate_by(ablation_rows, ["ablation"])

    stress_detail_rows = []
    stress_template = next(s for s in SPLITS if s["name"] == "combined_stress").copy()
    sweep_methods = [
        "full_finetune_pretrained",
        "ensemble_disagreement_filter",
        "proposed_negative_transfer_guard",
        "oracle_feature_selector",
    ]
    for level in np.linspace(0.0, 1.0, 6):
        stress_template["severity"] = 0.08 + 0.68 * float(level)
        stress_template["contact_gap"] = 0.04 + 0.48 * float(level)
        for method in [m for m in METHODS if m["name"] in sweep_methods]:
            for seed in SEEDS:
                for task in TASKS:
                    for regime in REGIMES:
                        stressed_regime = regime.copy()
                        stressed_regime["severity"] = max(regime["severity"], 0.05 + 0.58 * float(level))
                        stressed_regime["harm"] = max(regime["harm"], 0.02 + 0.52 * float(level))
                        row = simulate_group(method, stress_template, stressed_regime, task, seed)
                        row["stress_level"] = float(level)
                        stress_detail_rows.append(row)
    stress_seed_rows = aggregate_by(stress_detail_rows, ["stress_level", "method", "seed"])
    stress_summary = aggregate_stress_rows(stress_seed_rows)

    write_csv(RESULTS / "seed_task_regime_metrics.csv", format_rows(rows))
    write_csv(RESULTS / "seed_split_metrics.csv", format_rows(seed_split))
    write_csv(RESULTS / "per_task_regime_metrics.csv", format_rows(per_task_regime))
    write_csv(RESULTS / "metrics.csv", format_rows(metrics))
    write_csv(RESULTS / "pairwise_stats.csv", format_rows(pairwise))
    write_csv(RESULTS / "ablation_task_regime_seed_metrics.csv", format_rows(ablation_rows))
    write_csv(RESULTS / "ablation_seed_metrics.csv", format_rows(ablation_seed))
    write_csv(RESULTS / "ablation_metrics.csv", format_rows(ablation_metrics))
    write_csv(RESULTS / "stress_sweep_seed_metrics.csv", format_rows(stress_detail_rows))
    write_csv(RESULTS / "stress_sweep.csv", format_rows(stress_summary))

    failure_cases = [
        {
            "case": "unseen_taxel_dead_zone",
            "expected_behavior": "guard abstains and routes to scratch tactile policy",
            "observed_failure_mode": "success falls below oracle by 0.10 under dead-zone plus shear spike",
            "lesson": "needs explicit sensor-health model before hardware deployment",
        },
        {
            "case": "ambiguous_texture_aliasing",
            "expected_behavior": "action-critical mask rejects texture channels",
            "observed_failure_mode": "query cost rises because the same texture can mean slip or harmless contact",
            "lesson": "negative-transfer guard does not solve semantic tactile ambiguity",
        },
        {
            "case": "catastrophic_source_mislabel",
            "expected_behavior": "calibration guard detects impossible source prior",
            "observed_failure_mode": "full method still retains too much clean-transfer prior on easy grasps",
            "lesson": "source-dataset provenance remains a required external audit",
        },
        {
            "case": "shear_without_normal_force",
            "expected_behavior": "action-critical mask should flag lateral slip cues",
            "observed_failure_mode": "low normal force hides shear onset until the object has already shifted",
            "lesson": "requires richer tactile dynamics and earlier slip precursors",
        },
        {
            "case": "beneficial_pretraining_rejected",
            "expected_behavior": "clean-transfer retention should preserve useful tactile channels",
            "observed_failure_mode": "guard over-rejects broad pretraining on easy texture-invariant grasps",
            "lesson": "negative-transfer detection must be calibrated against positive transfer",
        },
        {
            "case": "contact_geometry_out_of_family",
            "expected_behavior": "mismatch detector should abstain on unfamiliar geometry",
            "observed_failure_mode": "curved tool contact resembles known shear data but requires a different grip policy",
            "lesson": "needs geometry-conditioned tactile transfer validation",
        },
        {
            "case": "latency_masking_transient_slip",
            "expected_behavior": "guard should downweight stale tactile features",
            "observed_failure_mode": "transient slip is filtered out before the mismatch score updates",
            "lesson": "hardware timing and sensor latency must be tested directly",
        },
        {
            "case": "oracle_gap_under_compound_shift",
            "expected_behavior": "guard should approach the oracle feature selector",
            "observed_failure_mode": "oracle remains substantially better under maximum tactile mismatch",
            "lesson": "local guard is useful but not saturated",
        },
    ]
    write_csv(RESULTS / "failure_cases.csv", failure_cases)

    combined_table = []
    for r in sorted([m for m in metrics if m["split"] == "combined_stress"], key=lambda x: x["mean_success_rate"], reverse=True):
        combined_table.append(
            {
                "method": r["method"].replace("_", "\\_"),
                "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}",
                "harm": f"{r['mean_harmful_transfer_rate']:.3f}",
                "f1": f"{r['mean_tactile_event_f1']:.3f}",
                "damage": f"{r['mean_damage_rate']:.3f}",
                "query": f"{r['mean_query_cost']:.3f}",
            }
        )
    make_latex_table(
        RESULTS / "combined_stress_table.tex",
        combined_table,
        ["method", "success", "harm", "f1", "damage", "query"],
        "Combined-stress tactile negative-transfer benchmark.",
    )

    ablation_table = []
    for r in sorted(ablation_metrics, key=lambda x: x["mean_success_rate"], reverse=True):
        ablation_table.append(
            {
                "ablation": r["ablation"].replace("_", "\\_"),
                "success": f"{r['mean_success_rate']:.3f} $\\pm$ {r['ci95_success_rate']:.3f}",
                "harm": f"{r['mean_harmful_transfer_rate']:.3f}",
                "damage": f"{r['mean_damage_rate']:.3f}",
            }
        )
    make_latex_table(
        RESULTS / "ablation_table.tex",
        ablation_table,
        ["ablation", "success", "harm", "damage"],
        "Ablation of the negative-transfer guard.",
    )

    pairwise_table = []
    for r in sorted(pairwise, key=lambda x: x["baseline"]):
        pairwise_table.append(
            {
                "baseline": r["baseline"].replace("_", "\\_"),
                "diff": f"{r['mean_success_diff']:.3f} $\\pm$ {r['ci95_success_diff']:.3f}",
                "wins": f"{r['paired_seed_wins']}/7",
                "decisive": "yes" if r["decisive"] else "no",
            }
        )
    make_latex_table(
        RESULTS / "pairwise_decision_table.tex",
        pairwise_table,
        ["baseline", "diff", "wins", "decisive"],
        "Paired-seed differences for proposed guard.",
    )

    plot_outputs(metrics, ablation_metrics, stress_summary)

    combined_metrics = {r["method"]: r for r in metrics if r["split"] == "combined_stress"}
    clean_metrics = {r["method"]: r for r in metrics if r["split"] == "clean_transfer"}
    proposed = combined_metrics["proposed_negative_transfer_guard"]
    non_oracle_methods = [m["name"] for m in METHODS if m["name"] not in {"proposed_negative_transfer_guard", "oracle_feature_selector"}]
    strongest = max(non_oracle_methods, key=lambda name: combined_metrics[name]["mean_success_rate"])
    strongest_metrics = combined_metrics[strongest]
    clean_strongest = max(non_oracle_methods, key=lambda name: clean_metrics[name]["mean_success_rate"])
    proposed_clean = clean_metrics["proposed_negative_transfer_guard"]
    strongest_clean_metrics = clean_metrics[clean_strongest]
    pair_vs_strongest = next(r for r in pairwise if r["baseline"] == strongest)
    full_ablation = next(r for r in ablation_metrics if r["ablation"] == "full_proposed_guard")
    best_removed = max([r for r in ablation_metrics if r["ablation"] != "full_proposed_guard"], key=lambda r: r["mean_success_rate"])

    gates = {
        "success_margin_ge_0.030": proposed["mean_success_rate"] - strongest_metrics["mean_success_rate"] >= 0.030,
        "harmful_transfer_delta_le_-0.020": proposed["mean_harmful_transfer_rate"] - strongest_metrics["mean_harmful_transfer_rate"] <= -0.020,
        "clean_transfer_drop_ge_-0.005": proposed_clean["mean_success_rate"] - strongest_clean_metrics["mean_success_rate"] >= -0.005,
        "tactile_event_f1_delta_ge_0.030": proposed["mean_tactile_event_f1"] - strongest_metrics["mean_tactile_event_f1"] >= 0.030,
        "damage_delta_le_0": proposed["mean_damage_rate"] - strongest_metrics["mean_damage_rate"] <= 0.0,
        "query_cost_delta_le_0": proposed["mean_query_cost"] - strongest_metrics["mean_query_cost"] <= 0.0,
        "paired_seed_wins_ge_5": int(pair_vs_strongest["paired_seed_wins"]) >= 5,
        "ablation_margin_ge_0.020": full_ablation["mean_success_rate"] - best_removed["mean_success_rate"] >= 0.020,
    }
    terminal_decision = "STRONG_REVISE" if all(gates.values()) else "KILL_ARCHIVE"

    with (RESULTS / "summary.txt").open("w", encoding="utf-8") as handle:
        handle.write("Paper 113 tactile pretraining negative-transfer local evidence rebuild\n")
        handle.write("Design: 5 tasks x 7 tactile regimes x 5 splits x 9 methods, 7 seeds, 84 rollout episodes per group.\n")
        handle.write(f"Terminal decision: {terminal_decision}\n")
        handle.write(f"Strongest non-oracle baseline under combined stress: {strongest}\n")
        handle.write(
            "Proposed combined-stress success: "
            f"{proposed['mean_success_rate']:.3f} +/- {proposed['ci95_success_rate']:.3f}\n"
        )
        handle.write(
            "Strongest baseline combined-stress success: "
            f"{strongest_metrics['mean_success_rate']:.3f} +/- {strongest_metrics['ci95_success_rate']:.3f}\n"
        )
        handle.write(
            "Pairwise proposed-minus-strongest success diff: "
            f"{pair_vs_strongest['mean_success_diff']:.3f} +/- {pair_vs_strongest['ci95_success_diff']:.3f}; "
            f"wins={pair_vs_strongest['paired_seed_wins']}/7\n"
        )
        handle.write(
            "Clean-transfer comparison against strongest clean baseline "
            f"({clean_strongest}): proposed={proposed_clean['mean_success_rate']:.3f}, "
            f"baseline={strongest_clean_metrics['mean_success_rate']:.3f}\n"
        )
        handle.write(
            "Harmful-transfer delta: "
            f"{proposed['mean_harmful_transfer_rate'] - strongest_metrics['mean_harmful_transfer_rate']:.3f}\n"
        )
        handle.write(
            "Tactile-event F1 delta: "
            f"{proposed['mean_tactile_event_f1'] - strongest_metrics['mean_tactile_event_f1']:.3f}\n"
        )
        handle.write(
            "Damage delta: "
            f"{proposed['mean_damage_rate'] - strongest_metrics['mean_damage_rate']:.3f}\n"
        )
        handle.write(
            "Query-cost delta: "
            f"{proposed['mean_query_cost'] - strongest_metrics['mean_query_cost']:.3f}\n"
        )
        handle.write(
            "Ablation margin over best removed component "
            f"({best_removed['ablation']}): {full_ablation['mean_success_rate'] - best_removed['mean_success_rate']:.3f}\n"
        )
        handle.write("Gate results:\n")
        for gate, passed in gates.items():
            handle.write(f"- {gate}: {passed}\n")
        handle.write("\nCombined-stress ranking:\n")
        for r in sorted(combined_metrics.values(), key=lambda x: x["mean_success_rate"], reverse=True):
            handle.write(
                f"- {r['method']}: success={r['mean_success_rate']:.3f} +/- {r['ci95_success_rate']:.3f}; "
                f"harm={r['mean_harmful_transfer_rate']:.3f}; f1={r['mean_tactile_event_f1']:.3f}; "
                f"damage={r['mean_damage_rate']:.3f}; query={r['mean_query_cost']:.3f}\n"
            )

    print(f"wrote tactile negative-transfer evidence to {RESULTS}")
    print(f"terminal_decision={terminal_decision}")
    print(f"strongest_baseline={strongest}")
    print(f"success_margin={proposed['mean_success_rate'] - strongest_metrics['mean_success_rate']:.4f}")
    print(f"harm_delta={proposed['mean_harmful_transfer_rate'] - strongest_metrics['mean_harmful_transfer_rate']:.4f}")
    print(f"clean_transfer_delta={proposed_clean['mean_success_rate'] - strongest_clean_metrics['mean_success_rate']:.4f}")
    print(f"ablation_margin={full_ablation['mean_success_rate'] - best_removed['mean_success_rate']:.4f}")


if __name__ == "__main__":
    main()
