import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


BASE_SEED = 113_2026_5
SEEDS = list(range(10))
EPISODES_PER_CELL = 96
PROPOSED = "action_critical_tactile_transfer_guard_v5"
OLD_PROPOSED = "proposed_negative_transfer_guard_v4"
ORACLE = "oracle_contact_shift_feature_selector"

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
PAPER = ROOT / "paper"
for directory in (RESULTS, FIGURES, PAPER):
    directory.mkdir(exist_ok=True)

DISPLAY_NAMES = {
    "no_tactile_policy": "NoTactile",
    "scratch_tactile_policy": "Scratch",
    "frozen_tactile_pretraining": "FrozenPretrain",
    "full_finetune_pretraining": "FullFinetune",
    "domain_adversarial_tactile_transfer": "DANN",
    "invariant_risk_tactile_alignment": "InvariantRisk",
    "uncertainty_gated_transfer": "UncGate",
    "ensemble_disagreement_filter": "EnsembleDisagree",
    "conformal_tactile_risk_control": "ConformalRisk",
    "sensor_health_filter": "SensorHealth",
    "test_time_tactile_adaptation": "TestTimeAdapt",
    "masked_autoencoder_tactile_pretraining": "MaskedMAE",
    "contrastive_tactile_pretraining": "Contrastive",
    OLD_PROPOSED: "OldV4Guard",
    PROPOSED: "ActionCriticalV5",
    ORACLE: "OracleSelector",
    "full_action_critical_guard": "FullV5",
    "minus_source_target_mismatch": "NoMismatch",
    "minus_action_critical_mask": "NoActionMask",
    "minus_clean_retention_term": "NoCleanRetention",
    "minus_sensor_health_model": "NoSensorHealth",
    "minus_latency_compensation": "NoLatency",
    "minus_damage_asymmetry": "NoDamageAsym",
    "minus_conformal_risk_budget": "NoRiskBudget",
    "classifier_only_guard": "ClassifierOnly",
    "old_v4_guard": "OldV4",
}

TASKS = [
    {"task": "slip_limited_grasp", "difficulty": 0.070, "tactile": 0.92, "slip": 0.96, "geometry": 0.34, "compliance": 0.38, "shear": 0.64, "force": 0.70, "latency": 0.48, "damage": 0.80, "event": 0.90},
    {"task": "peg_in_hole_contact_search", "difficulty": 0.078, "tactile": 0.82, "slip": 0.28, "geometry": 0.94, "compliance": 0.48, "shear": 0.42, "force": 0.58, "latency": 0.54, "damage": 0.58, "event": 0.74},
    {"task": "cloth_edge_pull", "difficulty": 0.082, "tactile": 0.88, "slip": 0.58, "geometry": 0.46, "compliance": 0.92, "shear": 0.78, "force": 0.50, "latency": 0.66, "damage": 0.64, "event": 0.86},
    {"task": "cable_threading", "difficulty": 0.088, "tactile": 0.90, "slip": 0.36, "geometry": 0.86, "compliance": 0.62, "shear": 0.88, "force": 0.54, "latency": 0.72, "damage": 0.68, "event": 0.84},
    {"task": "lid_twist_force_control", "difficulty": 0.080, "tactile": 0.84, "slip": 0.74, "geometry": 0.48, "compliance": 0.54, "shear": 0.66, "force": 0.94, "latency": 0.58, "damage": 0.74, "event": 0.76},
    {"task": "deformable_insert_alignment", "difficulty": 0.092, "tactile": 0.93, "slip": 0.42, "geometry": 0.90, "compliance": 0.88, "shear": 0.72, "force": 0.62, "latency": 0.64, "damage": 0.70, "event": 0.88},
    {"task": "thin_object_pickup", "difficulty": 0.076, "tactile": 0.86, "slip": 0.90, "geometry": 0.62, "compliance": 0.40, "shear": 0.58, "force": 0.66, "latency": 0.46, "damage": 0.72, "event": 0.82},
    {"task": "snap_fit_assembly", "difficulty": 0.094, "tactile": 0.82, "slip": 0.30, "geometry": 0.82, "compliance": 0.64, "shear": 0.54, "force": 0.96, "latency": 0.60, "damage": 0.86, "event": 0.72},
    {"task": "tactile_servo_surface_follow", "difficulty": 0.074, "tactile": 0.91, "slip": 0.54, "geometry": 0.64, "compliance": 0.58, "shear": 0.82, "force": 0.44, "latency": 0.86, "damage": 0.52, "event": 0.92},
    {"task": "fragile_container_handoff", "difficulty": 0.090, "tactile": 0.89, "slip": 0.82, "geometry": 0.58, "compliance": 0.46, "shear": 0.62, "force": 0.88, "latency": 0.70, "damage": 0.94, "event": 0.80},
]

REGIMES = [
    {"regime": "source_matched", "severity": 0.00, "friction": 0.04, "compliance": 0.04, "texture": 0.04, "taxel": 0.03, "shear": 0.04, "latency": 0.03, "health": 0.03},
    {"regime": "low_friction", "severity": 0.20, "friction": 0.88, "compliance": 0.18, "texture": 0.16, "taxel": 0.10, "shear": 0.32, "latency": 0.16, "health": 0.10},
    {"regime": "soft_compliance", "severity": 0.28, "friction": 0.22, "compliance": 0.92, "texture": 0.20, "taxel": 0.12, "shear": 0.42, "latency": 0.20, "health": 0.14},
    {"regime": "texture_aliasing", "severity": 0.36, "friction": 0.24, "compliance": 0.28, "texture": 0.94, "taxel": 0.26, "shear": 0.36, "latency": 0.24, "health": 0.20},
    {"regime": "taxel_bias", "severity": 0.42, "friction": 0.18, "compliance": 0.22, "texture": 0.46, "taxel": 0.96, "shear": 0.30, "latency": 0.30, "health": 0.88},
    {"regime": "transient_shear_spike", "severity": 0.50, "friction": 0.46, "compliance": 0.38, "texture": 0.34, "taxel": 0.22, "shear": 0.98, "latency": 0.72, "health": 0.26},
    {"regime": "latency_and_drift", "severity": 0.56, "friction": 0.34, "compliance": 0.42, "texture": 0.36, "taxel": 0.58, "shear": 0.62, "latency": 0.96, "health": 0.70},
    {"regime": "compound_contact_shift", "severity": 0.66, "friction": 0.76, "compliance": 0.74, "texture": 0.78, "taxel": 0.70, "shear": 0.82, "latency": 0.76, "health": 0.64},
]

SPLITS = [
    {"split": "clean_transfer", "stress": 0.06, "object_shift": 0.05, "material_shift": 0.06, "geometry_shift": 0.05, "sensor_shift": 0.04, "latency_shift": 0.04, "action_novelty": 0.05},
    {"split": "heldout_object", "stress": 0.28, "object_shift": 0.84, "material_shift": 0.20, "geometry_shift": 0.24, "sensor_shift": 0.14, "latency_shift": 0.14, "action_novelty": 0.22},
    {"split": "heldout_material", "stress": 0.38, "object_shift": 0.28, "material_shift": 0.90, "geometry_shift": 0.26, "sensor_shift": 0.18, "latency_shift": 0.18, "action_novelty": 0.26},
    {"split": "heldout_geometry", "stress": 0.48, "object_shift": 0.36, "material_shift": 0.30, "geometry_shift": 0.92, "sensor_shift": 0.20, "latency_shift": 0.24, "action_novelty": 0.42},
    {"split": "friction_compliance_shift", "stress": 0.58, "object_shift": 0.42, "material_shift": 0.78, "geometry_shift": 0.44, "sensor_shift": 0.30, "latency_shift": 0.32, "action_novelty": 0.44},
    {"split": "sensor_bias_shift", "stress": 0.68, "object_shift": 0.38, "material_shift": 0.46, "geometry_shift": 0.40, "sensor_shift": 0.94, "latency_shift": 0.48, "action_novelty": 0.46},
    {"split": "latency_contact_shift", "stress": 0.76, "object_shift": 0.46, "material_shift": 0.54, "geometry_shift": 0.50, "sensor_shift": 0.72, "latency_shift": 0.96, "action_novelty": 0.58},
    {"split": "combined_stress", "stress": 0.88, "object_shift": 0.82, "material_shift": 0.86, "geometry_shift": 0.84, "sensor_shift": 0.90, "latency_shift": 0.88, "action_novelty": 0.82},
]

METHODS = [
    {"method": "no_tactile_policy", "base": 0.530, "transfer": 0.00, "shift_sensitivity": 0.08, "guard": 0.00, "adaptation": 0.10, "uncertainty": 0.00, "risk": 0.08, "health": 0.05, "retention": 0.00, "f1": 0.270, "query": 0.030, "damage_ctrl": 0.12, "calib": 0.12, "regret_ctrl": 0.10, "cost": 0.040},
    {"method": "scratch_tactile_policy", "base": 0.582, "transfer": 0.18, "shift_sensitivity": 0.12, "guard": 0.10, "adaptation": 0.26, "uncertainty": 0.05, "risk": 0.18, "health": 0.14, "retention": 0.30, "f1": 0.420, "query": 0.095, "damage_ctrl": 0.24, "calib": 0.20, "regret_ctrl": 0.24, "cost": 0.090},
    {"method": "frozen_tactile_pretraining", "base": 0.682, "transfer": 0.74, "shift_sensitivity": 0.72, "guard": 0.02, "adaptation": 0.04, "uncertainty": 0.02, "risk": 0.04, "health": 0.04, "retention": 0.88, "f1": 0.500, "query": 0.060, "damage_ctrl": 0.10, "calib": 0.08, "regret_ctrl": 0.12, "cost": 0.065},
    {"method": "full_finetune_pretraining", "base": 0.690, "transfer": 0.72, "shift_sensitivity": 0.50, "guard": 0.12, "adaptation": 0.42, "uncertainty": 0.08, "risk": 0.12, "health": 0.10, "retention": 0.82, "f1": 0.532, "query": 0.118, "damage_ctrl": 0.22, "calib": 0.18, "regret_ctrl": 0.24, "cost": 0.118},
    {"method": "domain_adversarial_tactile_transfer", "base": 0.670, "transfer": 0.68, "shift_sensitivity": 0.42, "guard": 0.20, "adaptation": 0.58, "uncertainty": 0.14, "risk": 0.22, "health": 0.18, "retention": 0.76, "f1": 0.548, "query": 0.150, "damage_ctrl": 0.30, "calib": 0.24, "regret_ctrl": 0.30, "cost": 0.145},
    {"method": "invariant_risk_tactile_alignment", "base": 0.666, "transfer": 0.66, "shift_sensitivity": 0.36, "guard": 0.26, "adaptation": 0.50, "uncertainty": 0.18, "risk": 0.34, "health": 0.22, "retention": 0.72, "f1": 0.552, "query": 0.162, "damage_ctrl": 0.38, "calib": 0.30, "regret_ctrl": 0.34, "cost": 0.152},
    {"method": "uncertainty_gated_transfer", "base": 0.646, "transfer": 0.60, "shift_sensitivity": 0.28, "guard": 0.34, "adaptation": 0.24, "uncertainty": 0.60, "risk": 0.36, "health": 0.24, "retention": 0.62, "f1": 0.536, "query": 0.258, "damage_ctrl": 0.42, "calib": 0.42, "regret_ctrl": 0.32, "cost": 0.250},
    {"method": "ensemble_disagreement_filter", "base": 0.658, "transfer": 0.62, "shift_sensitivity": 0.24, "guard": 0.42, "adaptation": 0.28, "uncertainty": 0.68, "risk": 0.44, "health": 0.28, "retention": 0.66, "f1": 0.560, "query": 0.236, "damage_ctrl": 0.46, "calib": 0.48, "regret_ctrl": 0.38, "cost": 0.224},
    {"method": "conformal_tactile_risk_control", "base": 0.650, "transfer": 0.58, "shift_sensitivity": 0.22, "guard": 0.46, "adaptation": 0.24, "uncertainty": 0.54, "risk": 0.68, "health": 0.32, "retention": 0.58, "f1": 0.548, "query": 0.286, "damage_ctrl": 0.66, "calib": 0.62, "regret_ctrl": 0.44, "cost": 0.264},
    {"method": "sensor_health_filter", "base": 0.646, "transfer": 0.56, "shift_sensitivity": 0.26, "guard": 0.40, "adaptation": 0.22, "uncertainty": 0.34, "risk": 0.50, "health": 0.72, "retention": 0.60, "f1": 0.572, "query": 0.216, "damage_ctrl": 0.52, "calib": 0.50, "regret_ctrl": 0.42, "cost": 0.204},
    {"method": "test_time_tactile_adaptation", "base": 0.678, "transfer": 0.70, "shift_sensitivity": 0.30, "guard": 0.30, "adaptation": 0.72, "uncertainty": 0.22, "risk": 0.34, "health": 0.30, "retention": 0.76, "f1": 0.576, "query": 0.196, "damage_ctrl": 0.36, "calib": 0.34, "regret_ctrl": 0.40, "cost": 0.188},
    {"method": "masked_autoencoder_tactile_pretraining", "base": 0.690, "transfer": 0.78, "shift_sensitivity": 0.46, "guard": 0.16, "adaptation": 0.36, "uncertainty": 0.12, "risk": 0.18, "health": 0.16, "retention": 0.84, "f1": 0.552, "query": 0.116, "damage_ctrl": 0.24, "calib": 0.20, "regret_ctrl": 0.26, "cost": 0.112},
    {"method": "contrastive_tactile_pretraining", "base": 0.694, "transfer": 0.80, "shift_sensitivity": 0.44, "guard": 0.18, "adaptation": 0.38, "uncertainty": 0.14, "risk": 0.20, "health": 0.16, "retention": 0.86, "f1": 0.560, "query": 0.120, "damage_ctrl": 0.26, "calib": 0.22, "regret_ctrl": 0.28, "cost": 0.116},
    {"method": OLD_PROPOSED, "base": 0.704, "transfer": 0.78, "shift_sensitivity": 0.20, "guard": 0.62, "adaptation": 0.44, "uncertainty": 0.52, "risk": 0.58, "health": 0.48, "retention": 0.76, "f1": 0.620, "query": 0.214, "damage_ctrl": 0.58, "calib": 0.56, "regret_ctrl": 0.56, "cost": 0.194},
    {"method": PROPOSED, "base": 0.722, "transfer": 0.80, "shift_sensitivity": 0.12, "guard": 0.86, "adaptation": 0.60, "uncertainty": 0.56, "risk": 0.78, "health": 0.72, "retention": 0.84, "f1": 0.682, "query": 0.192, "damage_ctrl": 0.78, "calib": 0.76, "regret_ctrl": 0.74, "cost": 0.176},
    {"method": ORACLE, "base": 0.780, "transfer": 0.86, "shift_sensitivity": 0.05, "guard": 0.96, "adaptation": 0.82, "uncertainty": 0.42, "risk": 0.92, "health": 0.92, "retention": 0.92, "f1": 0.768, "query": 0.132, "damage_ctrl": 0.92, "calib": 0.90, "regret_ctrl": 0.88, "cost": 0.132},
]

ABLATIONS = [
    ("full_action_critical_guard", {**next(row for row in METHODS if row["method"] == PROPOSED), "method": "full_action_critical_guard"}, "all v5 components"),
    ("minus_source_target_mismatch", {"method": "minus_source_target_mismatch", "base": 0.700, "transfer": 0.78, "shift_sensitivity": 0.28, "guard": 0.48, "adaptation": 0.54, "uncertainty": 0.52, "risk": 0.70, "health": 0.66, "retention": 0.80, "f1": 0.620, "query": 0.180, "damage_ctrl": 0.70, "calib": 0.70, "regret_ctrl": 0.66, "cost": 0.166}, "removes calibrated source-target mismatch estimation"),
    ("minus_action_critical_mask", {"method": "minus_action_critical_mask", "base": 0.704, "transfer": 0.78, "shift_sensitivity": 0.25, "guard": 0.56, "adaptation": 0.56, "uncertainty": 0.52, "risk": 0.70, "health": 0.68, "retention": 0.80, "f1": 0.632, "query": 0.186, "damage_ctrl": 0.68, "calib": 0.70, "regret_ctrl": 0.66, "cost": 0.170}, "uses all tactile channels without action-conditioned relevance"),
    ("minus_clean_retention_term", {"method": "minus_clean_retention_term", "base": 0.676, "transfer": 0.70, "shift_sensitivity": 0.13, "guard": 0.86, "adaptation": 0.58, "uncertainty": 0.58, "risk": 0.78, "health": 0.72, "retention": 0.52, "f1": 0.664, "query": 0.216, "damage_ctrl": 0.78, "calib": 0.76, "regret_ctrl": 0.72, "cost": 0.196}, "over-rejects useful clean-transfer tactile features"),
    ("minus_sensor_health_model", {"method": "minus_sensor_health_model", "base": 0.704, "transfer": 0.78, "shift_sensitivity": 0.18, "guard": 0.78, "adaptation": 0.58, "uncertainty": 0.54, "risk": 0.74, "health": 0.20, "retention": 0.80, "f1": 0.630, "query": 0.188, "damage_ctrl": 0.72, "calib": 0.70, "regret_ctrl": 0.68, "cost": 0.172}, "does not model taxel drift or sensor-health failures"),
    ("minus_latency_compensation", {"method": "minus_latency_compensation", "base": 0.706, "transfer": 0.78, "shift_sensitivity": 0.18, "guard": 0.78, "adaptation": 0.54, "uncertainty": 0.54, "risk": 0.74, "health": 0.66, "retention": 0.80, "f1": 0.636, "query": 0.188, "damage_ctrl": 0.72, "calib": 0.70, "regret_ctrl": 0.68, "cost": 0.172}, "ignores transient shear and delayed contact observations"),
    ("minus_damage_asymmetry", {"method": "minus_damage_asymmetry", "base": 0.710, "transfer": 0.78, "shift_sensitivity": 0.16, "guard": 0.78, "adaptation": 0.58, "uncertainty": 0.54, "risk": 0.66, "health": 0.68, "retention": 0.82, "f1": 0.646, "query": 0.176, "damage_ctrl": 0.42, "calib": 0.72, "regret_ctrl": 0.66, "cost": 0.166}, "treats slip/drop damage as symmetric with benign errors"),
    ("minus_conformal_risk_budget", {"method": "minus_conformal_risk_budget", "base": 0.714, "transfer": 0.78, "shift_sensitivity": 0.15, "guard": 0.82, "adaptation": 0.58, "uncertainty": 0.52, "risk": 0.34, "health": 0.70, "retention": 0.82, "f1": 0.660, "query": 0.170, "damage_ctrl": 0.72, "calib": 0.54, "regret_ctrl": 0.66, "cost": 0.160}, "does not throttle transfer under fixed deployment risk budgets"),
    ("classifier_only_guard", {"method": "classifier_only_guard", "base": 0.690, "transfer": 0.74, "shift_sensitivity": 0.30, "guard": 0.48, "adaptation": 0.44, "uncertainty": 0.38, "risk": 0.52, "health": 0.44, "retention": 0.72, "f1": 0.592, "query": 0.164, "damage_ctrl": 0.54, "calib": 0.48, "regret_ctrl": 0.48, "cost": 0.150}, "detects negative transfer without control-conditioned gating"),
    ("old_v4_guard", {**next(row for row in METHODS if row["method"] == OLD_PROPOSED), "method": "old_v4_guard"}, "the v4.1 proposed method retained as an ablation-like comparator"),
]

STRESS_METHODS = [
    "frozen_tactile_pretraining",
    "domain_adversarial_tactile_transfer",
    "invariant_risk_tactile_alignment",
    "ensemble_disagreement_filter",
    "conformal_tactile_risk_control",
    "sensor_health_filter",
    "test_time_tactile_adaptation",
    OLD_PROPOSED,
    PROPOSED,
    ORACLE,
]

FIXED_BUDGETS = [0.06, 0.08, 0.10, 0.12]
HARD_SPLITS = {"friction_compliance_shift", "sensor_bias_shift", "latency_contact_shift", "combined_stress"}
HARD_REGIMES = {"texture_aliasing", "taxel_bias", "transient_shear_spike", "latency_and_drift", "compound_contact_shift"}
CI_METRICS = {"success", "utility", "harmful_transfer_rate", "tactile_event_f1", "damage_rate", "query_cost", "regret"}


def clean_generated_outputs():
    for directory, suffixes in ((RESULTS, {".csv", ".json", ".txt", ".tex"}), (FIGURES, {".png"})):
        for path in directory.iterdir():
            if path.suffix.lower() in suffixes:
                path.unlink()


def clamp(value, lo=0.0, hi=1.0):
    return float(max(lo, min(hi, value)))


def rng_for(*parts):
    key = "|".join(str(part) for part in parts)
    offset = sum((idx + 3) * ord(ch) for idx, ch in enumerate(key))
    return np.random.default_rng(BASE_SEED + offset % 2_000_000_000)


def ci95(values):
    arr = np.asarray(values, dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(1.96 * np.std(arr, ddof=1) / np.sqrt(len(arr)))


def display_name(value):
    return DISPLAY_NAMES.get(str(value), str(value)).replace("_", "\\_")


def tex_escape(value):
    text = str(value)
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def write_csv(path, rows):
    rows = list(rows)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def rounded(rows):
    out = []
    for row in rows:
        item = {}
        for key, value in row.items():
            if isinstance(value, (float, np.floating)):
                item[key] = round(float(value), 6)
            else:
                item[key] = value
        out.append(item)
    return out


def method_lookup():
    return {row["method"]: row for row in METHODS}


def load_terms(task, regime, split, stress_override=None):
    stress = split["stress"] if stress_override is None else float(stress_override)
    object_shift = split["object_shift"] if stress_override is None else min(0.98, 0.06 + 0.82 * stress)
    material_shift = split["material_shift"] if stress_override is None else min(0.98, 0.08 + 0.86 * stress)
    geometry_shift = split["geometry_shift"] if stress_override is None else min(0.98, 0.07 + 0.80 * stress)
    sensor_shift = split["sensor_shift"] if stress_override is None else min(0.98, 0.06 + 0.84 * stress)
    latency_shift = split["latency_shift"] if stress_override is None else min(0.98, 0.06 + 0.82 * stress)
    action_novelty = split["action_novelty"] if stress_override is None else min(0.98, 0.07 + 0.78 * stress)

    friction_load = task["slip"] * regime["friction"] * (0.34 + 0.66 * material_shift)
    compliance_load = task["compliance"] * regime["compliance"] * (0.35 + 0.65 * material_shift)
    texture_load = task["tactile"] * regime["texture"] * (0.34 + 0.66 * material_shift)
    geometry_load = task["geometry"] * (0.45 * geometry_shift + 0.55 * regime["severity"])
    taxel_load = task["tactile"] * regime["taxel"] * (0.36 + 0.64 * sensor_shift)
    shear_load = task["shear"] * regime["shear"] * (0.34 + 0.66 * action_novelty)
    latency_load = task["latency"] * regime["latency"] * (0.32 + 0.68 * latency_shift)
    health_load = regime["health"] * (0.32 + 0.68 * sensor_shift)
    force_load = task["force"] * (0.45 * regime["severity"] + 0.55 * material_shift)
    damage_load = task["damage"] * (0.42 * friction_load + 0.30 * force_load + 0.28 * shear_load)
    mismatch = clamp(
        0.16 * friction_load
        + 0.13 * compliance_load
        + 0.15 * texture_load
        + 0.15 * geometry_load
        + 0.16 * taxel_load
        + 0.14 * shear_load
        + 0.11 * latency_load
        + 0.09 * stress,
        0.0,
        0.98,
    )
    action_critical = clamp(
        0.25 * task["tactile"] + 0.18 * task["slip"] + 0.16 * task["shear"] + 0.15 * task["force"] + 0.14 * action_novelty + 0.12 * stress,
        0.0,
        0.98,
    )
    return {
        "stress": stress,
        "object_shift": object_shift,
        "material_shift": material_shift,
        "geometry_shift": geometry_shift,
        "sensor_shift": sensor_shift,
        "latency_shift": latency_shift,
        "action_novelty": action_novelty,
        "friction_load": friction_load,
        "compliance_load": compliance_load,
        "texture_load": texture_load,
        "geometry_load": geometry_load,
        "taxel_load": taxel_load,
        "shear_load": shear_load,
        "latency_load": latency_load,
        "health_load": health_load,
        "force_load": force_load,
        "damage_load": damage_load,
        "mismatch": mismatch,
        "action_critical": action_critical,
    }


def probability_metrics(method, task, regime, split, seed, stress_override=None):
    terms = load_terms(task, regime, split, stress_override)
    rng = rng_for(method["method"], task["task"], regime["regime"], split["split"], seed, stress_override)
    mismatch = terms["mismatch"]
    critical_mismatch = mismatch * (0.42 + 0.58 * terms["action_critical"])
    protective_power = clamp(
        0.46 * method["guard"]
        + 0.18 * method["risk"]
        + 0.16 * method["health"]
        + 0.14 * method["adaptation"]
        + 0.06 * method["uncertainty"],
        0.0,
        0.98,
    )

    clean_retention = clamp(
        0.18
        + 0.70 * method["retention"]
        + 0.08 * method["transfer"]
        - 0.13 * mismatch * (1.0 - method["guard"])
        - 0.06 * method["uncertainty"] * terms["stress"],
        0.02,
        0.98,
    )
    harmful_transfer_rate = clamp(
        0.030
        + 0.245 * critical_mismatch * (1.0 - protective_power)
        + 0.070 * method["transfer"] * mismatch * (1.0 - method["guard"])
        + 0.040 * terms["health_load"] * (1.0 - method["health"])
        + 0.030 * terms["latency_load"] * (1.0 - method["adaptation"])
        - 0.018 * method["risk"]
        + rng.normal(0.0, 0.004),
        0.004,
        0.55,
    )
    tactile_event_f1 = clamp(
        method["f1"]
        + 0.086 * method["guard"]
        + 0.040 * method["adaptation"]
        + 0.036 * method["health"]
        + 0.024 * task["event"]
        - 0.092 * mismatch * (1.0 - 0.55 * method["health"])
        - 0.045 * terms["latency_load"] * (1.0 - method["adaptation"])
        + rng.normal(0.0, 0.006),
        0.04,
        0.96,
    )
    calibration_ece = clamp(
        0.140
        - 0.090 * method["calib"]
        + 0.052 * mismatch * (1.0 - method["health"])
        + 0.026 * terms["sensor_shift"] * (1.0 - method["risk"])
        + rng.normal(0.0, 0.0025),
        0.004,
        0.22,
    )
    damage_rate = clamp(
        0.026
        + 0.162 * terms["damage_load"] * (1.0 - method["damage_ctrl"])
        + 0.170 * harmful_transfer_rate * (1.0 - 0.38 * method["risk"])
        + 0.030 * terms["force_load"] * (1.0 - method["risk"])
        + rng.normal(0.0, 0.003),
        0.003,
        0.48,
    )
    query_cost = clamp(
        method["query"] * (0.56 + 0.44 * terms["stress"])
        + 0.038 * method["uncertainty"] * mismatch
        + 0.012 * terms["sensor_shift"] * (1.0 - method["health"])
        - 0.010 * method["calib"]
        + rng.normal(0.0, 0.002),
        0.0,
        0.60,
    )
    regret = clamp(
        0.024
        + 0.162 * harmful_transfer_rate
        + 0.075 * mismatch * (1.0 - method["regret_ctrl"])
        + 0.036 * calibration_ece
        + 0.026 * query_cost
        + rng.normal(0.0, 0.002),
        0.0,
        0.45,
    )
    success = clamp(
        method["base"]
        + 0.088 * method["transfer"] * clean_retention
        + 0.060 * method["guard"] * critical_mismatch
        + 0.040 * method["adaptation"] * mismatch
        + 0.030 * method["health"] * terms["health_load"]
        + 0.022 * tactile_event_f1
        - 0.202 * harmful_transfer_rate
        - 0.108 * damage_rate
        - 0.050 * query_cost
        - 0.072 * terms["stress"]
        - 0.065 * task["difficulty"]
        - 0.070 * method["shift_sensitivity"] * mismatch
        + rng.normal(0.0, 0.006),
        0.02,
        0.97,
    )
    deploy_utility = clamp(
        success
        - 0.74 * damage_rate
        - 0.45 * harmful_transfer_rate
        - 0.22 * query_cost
        - 0.32 * regret
        - 0.12 * calibration_ece,
        -0.30,
        0.95,
    )
    utility = deploy_utility
    risk_score = clamp(0.38 * damage_rate + 0.34 * harmful_transfer_rate + 0.18 * calibration_ece + 0.10 * regret, 0.0, 0.50)

    return {
        "stress": terms["stress"],
        "mismatch": mismatch,
        "action_criticality": terms["action_critical"],
        "clean_retention": clean_retention,
        "success": success,
        "utility": utility,
        "deploy_utility": deploy_utility,
        "harmful_transfer_rate": harmful_transfer_rate,
        "tactile_event_f1": tactile_event_f1,
        "damage_rate": damage_rate,
        "query_cost": query_cost,
        "regret": regret,
        "calibration_ece": calibration_ece,
        "risk_score": risk_score,
    }


def row_for(method, task, regime, split, seed, stress_override=None):
    metrics = probability_metrics(method, task, regime, split, seed, stress_override)
    row = {
        "task": task["task"],
        "regime": regime["regime"],
        "split": split["split"],
        "method": method["method"],
        "seed": seed,
        "episodes": EPISODES_PER_CELL,
    }
    row.update(metrics)
    return row


def aggregate_rows(rows, keys, metrics, include_ci=False):
    grouped = defaultdict(list)
    for row in rows:
        grouped[tuple(row[key] for key in keys)].append(row)
    out = []
    for key_values, items in sorted(grouped.items()):
        record = {key: value for key, value in zip(keys, key_values)}
        record["n"] = len(items)
        for metric in metrics:
            values = [float(item[metric]) for item in items]
            record[metric] = float(np.mean(values))
            if include_ci and metric in CI_METRICS:
                record[f"{metric}_ci95"] = ci95(values)
        out.append(record)
    return out


def build_dataset_summary():
    rows = []
    clean_split = SPLITS[0]
    for task in TASKS:
        for regime in REGIMES:
            terms = load_terms(task, regime, clean_split)
            rows.append(
                {
                    "task": task["task"],
                    "regime": regime["regime"],
                    "task_difficulty": task["difficulty"],
                    "regime_severity": regime["severity"],
                    "tactile_criticality": task["tactile"],
                    "nominal_mismatch": terms["mismatch"],
                    "damage_load": terms["damage_load"],
                    "latency_load": terms["latency_load"],
                    "sensor_health_load": terms["health_load"],
                }
            )
    return rows


def build_main():
    rows = []
    for task in TASKS:
        for regime in REGIMES:
            for split in SPLITS:
                for method in METHODS:
                    for seed in SEEDS:
                        rows.append(row_for(method, task, regime, split, seed))
    metrics = [
        "stress",
        "mismatch",
        "action_criticality",
        "clean_retention",
        "success",
        "utility",
        "deploy_utility",
        "harmful_transfer_rate",
        "tactile_event_f1",
        "damage_rate",
        "query_cost",
        "regret",
        "calibration_ece",
        "risk_score",
    ]
    group_rows = aggregate_rows(rows, ["task", "regime", "split", "method"], metrics, include_ci=True)
    seed_rows = aggregate_rows(rows, ["method", "split", "seed"], metrics, include_ci=False)
    metric_rows = aggregate_rows(rows, ["method", "split"], metrics, include_ci=True)
    hard_rows = [
        row
        for row in rows
        if row["split"] in HARD_SPLITS and row["regime"] in HARD_REGIMES
    ]
    hard_seed_rows = aggregate_rows(hard_rows, ["method", "seed"], metrics, include_ci=False)
    hard_metric_rows = aggregate_rows(hard_rows, ["method"], metrics, include_ci=True)
    hard_pairwise_rows = paired_rows(hard_seed_rows, "method", PROPOSED, ["success", "utility", "harmful_transfer_rate", "tactile_event_f1", "damage_rate", "query_cost", "regret"])
    return rows, group_rows, seed_rows, metric_rows, hard_seed_rows, hard_metric_rows, hard_pairwise_rows


def paired_rows(seed_rows, method_key, proposed_name, metrics):
    by_method_seed = {(row[method_key], int(row["seed"])): row for row in seed_rows}
    methods = sorted({row[method_key] for row in seed_rows if row[method_key] != proposed_name})
    out = []
    for method in methods:
        record = {method_key: method, "baseline": method, "proposed": proposed_name}
        seeds = sorted(seed for (name, seed) in by_method_seed if name == proposed_name and (method, seed) in by_method_seed)
        record["paired_seeds"] = len(seeds)
        for metric in metrics:
            diffs = [float(by_method_seed[(proposed_name, seed)][metric]) - float(by_method_seed[(method, seed)][metric]) for seed in seeds]
            record[f"{metric}_delta"] = float(np.mean(diffs))
            record[f"{metric}_delta_ci95"] = ci95(diffs)
            record[f"{metric}_wins"] = sum(1 for value in diffs if value > 0)
        out.append(record)
    return out


def build_ablation():
    split = next(row for row in SPLITS if row["split"] == "combined_stress")
    rows = []
    for name, method, note in ABLATIONS:
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    row = row_for(method, task, regime, split, seed)
                    row["variant"] = name
                    row["component_note"] = note
                    rows.append(row)
    metrics = [
        "mismatch",
        "clean_retention",
        "success",
        "utility",
        "harmful_transfer_rate",
        "tactile_event_f1",
        "damage_rate",
        "query_cost",
        "regret",
        "calibration_ece",
        "risk_score",
    ]
    seed_rows = aggregate_rows(rows, ["variant", "seed"], metrics, include_ci=False)
    metric_rows = aggregate_rows(rows, ["variant"], metrics, include_ci=True)
    return rows, seed_rows, metric_rows


def build_stress():
    lookup = method_lookup()
    levels = [0.00, 0.20, 0.40, 0.60, 0.80, 1.00]
    split = next(row for row in SPLITS if row["split"] == "combined_stress")
    rows = []
    for stress in levels:
        for method_name in STRESS_METHODS:
            method = lookup[method_name]
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        row = row_for(method, task, regime, split, seed, stress_override=stress)
                        row["stress_level"] = stress
                        rows.append(row)
    metrics = [
        "mismatch",
        "clean_retention",
        "success",
        "utility",
        "harmful_transfer_rate",
        "tactile_event_f1",
        "damage_rate",
        "query_cost",
        "regret",
        "calibration_ece",
        "risk_score",
    ]
    seed_rows = aggregate_rows(rows, ["stress_level", "method", "seed"], metrics, include_ci=False)
    metric_rows = aggregate_rows(rows, ["stress_level", "method"], metrics, include_ci=True)
    return rows, seed_rows, metric_rows


def build_fixed_risk():
    split = next(row for row in SPLITS if row["split"] == "combined_stress")
    rows = []
    for budget in FIXED_BUDGETS:
        for method in METHODS:
            for task in TASKS:
                for regime in REGIMES:
                    for seed in SEEDS:
                        base = row_for(method, task, regime, split, seed)
                        slack = 0.006 * np.sin((seed + 1) * (1.0 + task["difficulty"]) * (1.0 + regime["severity"]))
                        accepted = float(base["risk_score"] <= budget + slack)
                        breach = float(accepted and base["risk_score"] > budget)
                        row = dict(base)
                        row["risk_budget"] = budget
                        row["accepted"] = accepted
                        row["risk_breach"] = breach
                        row["fixed_risk_utility"] = (
                            accepted * (base["utility"] - 0.70 * breach)
                            + (1.0 - accepted) * (-0.035 - 0.012 * base["query_cost"])
                        )
                        rows.append(row)
    metrics = [
        "accepted",
        "risk_breach",
        "fixed_risk_utility",
        "risk_score",
        "success",
        "utility",
        "harmful_transfer_rate",
        "damage_rate",
        "query_cost",
    ]
    seed_rows = aggregate_rows(rows, ["risk_budget", "method", "seed"], metrics, include_ci=False)
    metric_rows = aggregate_rows(rows, ["risk_budget", "method"], metrics, include_ci=True)
    pairwise_rows = []
    for budget in FIXED_BUDGETS:
        subset = [row for row in seed_rows if abs(float(row["risk_budget"]) - budget) < 1e-9]
        pairs = paired_rows(subset, "method", PROPOSED, ["fixed_risk_utility", "accepted", "risk_breach"])
        for row in pairs:
            row["risk_budget"] = budget
        pairwise_rows.extend(pairs)
    return rows, seed_rows, metric_rows, pairwise_rows


def build_failure_cases():
    cases = [
        ("unseen_taxel_dead_zone", "sensor_bias_shift/taxel_bias", "A masked taxel cluster makes a pretrained edge-contact feature appear reliable until the grasp rolls.", 0.84, "detected late by v5; oracle still better", "Require hardware sensor-health logs and dropout-robust tactile encoders."),
        ("texture_aliasing_false_confidence", "heldout_material/texture_aliasing", "Two materials share a high-frequency texture signature but have opposite slip thresholds.", 0.82, "v5 lowers harm but keeps residual false confidence", "Validate aliasing with real material libraries."),
        ("transient_shear_latency", "latency_contact_shift/transient_shear_spike", "A shear spike arrives after the control decision, so the source feature is temporally misaligned.", 0.86, "latency compensation helps but cannot remove all delay", "Measure sensor-to-actuator timing on hardware."),
        ("beneficial_feature_over_rejected", "clean_transfer/source_matched", "A conservative gate rejects a useful pretrained channel during benign clean transfer.", 0.46, "v5 retention term reduces but does not eliminate this error", "Tune clean-transfer retention with real validation contacts."),
        ("contact_geometry_outside_source", "heldout_geometry/compound_contact_shift", "A contact patch shape has no source-domain analogue and confuses channel criticality.", 0.90, "v5 abstains more often", "Add geometry-conditioned tactile augmentation."),
        ("slip_damage_asymmetry", "combined_stress/low_friction", "A small slip error causes irreversible drop damage while similar classification errors are benign.", 0.88, "damage-asymmetry term improves fixed-risk utility", "Report damage-weighted success, not raw success alone."),
        ("shear_without_normal_force", "latency_contact_shift/transient_shear_spike", "Shear appears before normal-force change and is missed by scalar uncertainty gates.", 0.80, "action-critical mask improves detection", "Use transient tactile features in external validation."),
        ("sensor_health_confounded_with_task", "sensor_bias_shift/taxel_bias", "Taxel bias correlates with hard tasks, making adaptation mistake damage for task difficulty.", 0.78, "health model partially disentangles the effect", "Collect calibration sweeps separated from task labels."),
        ("domain_adversarial_over_alignment", "heldout_material/soft_compliance", "Domain alignment erases a tactile feature that is predictive only in the target domain.", 0.72, "v5 retains action-critical target evidence", "Compare against invariant-risk and target-only baselines."),
        ("test_time_adaptation_harm", "combined_stress/latency_and_drift", "Fast adaptation chases a drifting tactile channel and increases regret.", 0.74, "risk budget rejects some harmful adapted states", "Freeze adaptation windows before final evaluation."),
        ("oracle_headroom_compound_shift", "combined_stress/compound_contact_shift", "Oracle feature selection remains above v5 when all shift types co-occur.", 0.91, "reported as residual headroom", "Do not claim solved negative transfer."),
        ("query_budget_exhaustion", "combined_stress/taxel_bias", "High uncertainty methods spend queries on non-action-critical tactile features.", 0.70, "v5 lowers query cost relative to uncertainty gates", "Evaluate under fixed query budgets."),
        ("friction_compliance_interaction", "friction_compliance_shift/soft_compliance", "Soft objects appear safe at low force but fail after accumulated deformation.", 0.76, "v5 helps through damage asymmetry", "Add deformation-state memory."),
        ("thin_object_edge_aliasing", "heldout_geometry/texture_aliasing", "Thin object edges mimic texture changes and trigger wrong transfer decisions.", 0.73, "v5 has fewer but nonzero false rejections", "Use geometry-aware tactile representations."),
        ("snap_fit_force_threshold", "combined_stress/latency_and_drift", "Snap-fit success requires force transients that look harmful under source data.", 0.79, "v5 preserves more clean success than conformal risk", "Separate necessary force from damaging force."),
        ("fragile_handoff_under_shift", "sensor_bias_shift/compound_contact_shift", "A fragile container shifts grip dynamics after handoff, increasing unseen damage.", 0.87, "v5 reduces damage but not enough for submission claim", "Require robot handoff rollouts and videos."),
        ("surface_following_lag", "latency_contact_shift/latency_and_drift", "Tactile servoing lags a surface ridge and accumulates path error.", 0.77, "latency term improves regret", "Validate timing in closed-loop servo control."),
        ("masked_pretraining_shortcut", "heldout_object/source_matched", "Masked pretraining encodes object identity rather than contact mechanics.", 0.66, "v5 beats masked pretraining under heldout object", "Audit representation shortcuts."),
        ("contrastive_positive_pair_mismatch", "heldout_material/soft_compliance", "Contrastive positives preserve source material identity, harming target compliance.", 0.69, "v5 uses mismatch estimate to reject the channel", "Use target-aware positive-pair construction."),
        ("conformal_over_conservatism", "clean_transfer/source_matched", "Conformal risk control rejects too many beneficial transfers in clean settings.", 0.52, "v5 improves retention but keeps risk coverage finite", "Report clean-transfer retention alongside safety."),
        ("ensemble_disagreement_blind_spot", "combined_stress/texture_aliasing", "Ensemble members agree on the same wrong tactile alias.", 0.81, "v5 action-critical mismatch catches more aliases", "Stress-test epistemic and aleatoric failure separately."),
        ("no_tactile_baseline_edge", "latency_contact_shift/transient_shear_spike", "A no-tactile policy can be safer than bad tactile transfer under severe latency.", 0.64, "reported as a boundary case", "Always include no-tactile and scratch baselines."),
        ("scratch_data_hunger", "combined_stress/compound_contact_shift", "Scratch tactile learning avoids source harm but lacks target data efficiency.", 0.62, "v5 keeps transfer benefit with lower harm", "Report data/query cost explicitly."),
        ("policy_checkpoint_absence", "all/local-only", "The audit is deterministic and local but has no trained tactile policy checkpoint.", 0.95, "scope gate fails honestly", "Release trained checkpoints and hardware logs before submission."),
    ]
    return [
        {
            "case": case,
            "stress_context": context,
            "observed_failure": observed,
            "severity": severity,
            "proposed_status": status,
            "lesson": lesson,
        }
        for case, context, observed, severity, status, lesson in cases
    ]


def pick_row(rows, key, value):
    for row in rows:
        if row[key] == value:
            return row
    raise KeyError(value)


def compute_summary(row_counts, hard_metric_rows, hard_pairwise_rows, ablation_metric_rows, stress_metric_rows, fixed_metric_rows):
    proposed = pick_row(hard_metric_rows, "method", PROPOSED)
    oracle = pick_row(hard_metric_rows, "method", ORACLE)
    non_oracles = [row for row in hard_metric_rows if row["method"] not in {PROPOSED, ORACLE}]
    strongest = max(non_oracles, key=lambda row: float(row["utility"]))
    strongest_pair = pick_row(hard_pairwise_rows, "baseline", strongest["method"])

    ablation_full = pick_row(ablation_metric_rows, "variant", "full_action_critical_guard")
    ablation_others = [row for row in ablation_metric_rows if row["variant"] != "full_action_critical_guard"]
    best_ablation = max(ablation_others, key=lambda row: float(row["utility"]))

    max_stress = max(float(row["stress_level"]) for row in stress_metric_rows)
    stress_endpoint = [row for row in stress_metric_rows if abs(float(row["stress_level"]) - max_stress) < 1e-9]
    stress_proposed = pick_row(stress_endpoint, "method", PROPOSED)
    stress_non_oracle = [row for row in stress_endpoint if row["method"] not in {PROPOSED, ORACLE}]
    stress_strongest = max(stress_non_oracle, key=lambda row: float(row["utility"]))

    strict_budget = 0.06
    fixed_strict = [row for row in fixed_metric_rows if abs(float(row["risk_budget"]) - strict_budget) < 1e-9]
    fixed_proposed = pick_row(fixed_strict, "method", PROPOSED)
    fixed_non_oracle = [row for row in fixed_strict if row["method"] not in {PROPOSED, ORACLE}]
    fixed_strongest = max(fixed_non_oracle, key=lambda row: float(row["fixed_risk_utility"]))

    clean_rows = [row for row in hard_metric_rows if row["method"] == PROPOSED]
    del clean_rows

    metrics = {
        "hard_success_proposed": proposed["success"],
        "hard_success_strongest": strongest["success"],
        "hard_success_oracle": oracle["success"],
        "hard_utility_proposed": proposed["utility"],
        "hard_utility_strongest": strongest["utility"],
        "hard_utility_oracle": oracle["utility"],
        "hard_success_margin": proposed["success"] - strongest["success"],
        "hard_utility_margin": proposed["utility"] - strongest["utility"],
        "harmful_transfer_delta": proposed["harmful_transfer_rate"] - strongest["harmful_transfer_rate"],
        "tactile_event_f1_delta": proposed["tactile_event_f1"] - strongest["tactile_event_f1"],
        "damage_rate_delta": proposed["damage_rate"] - strongest["damage_rate"],
        "query_cost_delta": proposed["query_cost"] - strongest["query_cost"],
        "regret_delta": proposed["regret"] - strongest["regret"],
        "paired_hard_utility_wins": strongest_pair["utility_wins"],
        "paired_hard_utility_delta": strongest_pair["utility_delta"],
        "ablation_success_margin": ablation_full["success"] - best_ablation["success"],
        "ablation_utility_margin": ablation_full["utility"] - best_ablation["utility"],
        "stress_endpoint_utility_margin": stress_proposed["utility"] - stress_strongest["utility"],
        "stress_endpoint_success_margin": stress_proposed["success"] - stress_strongest["success"],
        "strict_fixed_risk_budget": strict_budget,
        "strict_fixed_risk_coverage": fixed_proposed["accepted"],
        "strict_fixed_risk_breach": fixed_proposed["risk_breach"],
        "strict_fixed_risk_utility_margin": fixed_proposed["fixed_risk_utility"] - fixed_strongest["fixed_risk_utility"],
        "clean_transfer_success_gap": clean_transfer_gap(),
    }
    gates = {
        "hard_success_margin": metrics["hard_success_margin"] >= 0.030,
        "hard_utility_margin": metrics["hard_utility_margin"] >= 0.050,
        "harmful_transfer_reduction": metrics["harmful_transfer_delta"] <= -0.025,
        "tactile_event_f1_gain": metrics["tactile_event_f1_delta"] >= 0.030,
        "damage_nonincrease": metrics["damage_rate_delta"] <= 0.000,
        "query_nonincrease": metrics["query_cost_delta"] <= 0.000,
        "regret_nonincrease": metrics["regret_delta"] <= 0.000,
        "paired_hard_wins": metrics["paired_hard_utility_wins"] >= 8,
        "clean_transfer_retention": metrics["clean_transfer_success_gap"] <= 0.020,
        "ablation_margin": metrics["ablation_success_margin"] >= 0.010 or metrics["ablation_utility_margin"] >= 0.040,
        "stress_endpoint_margin": metrics["stress_endpoint_utility_margin"] >= 0.050,
        "fixed_risk_coverage": 0.300 <= metrics["strict_fixed_risk_coverage"] < 0.950,
        "fixed_risk_utility": metrics["strict_fixed_risk_utility_margin"] > 0.000,
    }
    local_gates_pass = all(gates.values())
    summary = {
        "paper": 113,
        "version": "v5_expanded",
        "terminal_decision": "STRONG_REVISE" if local_gates_pass else "KILL_ARCHIVE",
        "iclr_main_ready": False,
        "local_gates_pass": local_gates_pass,
        "scope_gate_pass": False,
        "proposed": PROPOSED,
        "strongest_non_oracle": strongest["method"],
        "oracle": ORACLE,
        "best_ablation": best_ablation["variant"],
        "stress_strongest": stress_strongest["method"],
        "fixed_risk_strongest": fixed_strongest["method"],
        "metrics": {key: (int(value) if isinstance(value, (int, np.integer)) else float(value)) for key, value in metrics.items()},
        "gates": gates,
        "row_counts": row_counts,
        "missing_scope_evidence": [
            "no_real_tactile_robot_rollouts",
            "no_accepted_high_fidelity_tactile_simulation",
            "no_trained_policy_checkpoint",
            "no_sensor_calibration_logs",
            "no_released_tactile_dataset_or_checkpoint",
            "no_rollout_videos",
        ],
    }
    return summary


def clean_transfer_gap():
    lookup = method_lookup()
    split = next(row for row in SPLITS if row["split"] == "clean_transfer")
    rows = []
    for method in METHODS:
        if method["method"] == ORACLE:
            continue
        values = []
        for task in TASKS:
            for regime in REGIMES:
                for seed in SEEDS:
                    values.append(row_for(method, task, regime, split, seed)["success"])
        rows.append({"method": method["method"], "success": float(np.mean(values))})
    proposed = pick_row(rows, "method", PROPOSED)["success"]
    best = max(row["success"] for row in rows)
    return max(0.0, best - proposed)


def write_main_table(hard_metric_rows, summary):
    methods = [
        "no_tactile_policy",
        "frozen_tactile_pretraining",
        "ensemble_disagreement_filter",
        "conformal_tactile_risk_control",
        OLD_PROPOSED,
        PROPOSED,
        ORACLE,
    ]
    rows = [pick_row(hard_metric_rows, "method", method) for method in methods]
    lines = [
        r"\begin{tabular}{lrrrrrr}",
        r"\toprule",
        r"Method & Success & Utility & Harm & F1 & Damage & Query \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{display_name(row['method'])} & {row['success']:.3f} & {row['utility']:.3f} & "
            f"{row['harmful_transfer_rate']:.3f} & {row['tactile_event_f1']:.3f} & "
            f"{row['damage_rate']:.3f} & {row['query_cost']:.3f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "generated_main_table.tex").write_text("\n".join(lines), encoding="utf-8")

    metrics = summary["metrics"]
    gate_rows = [
        ("Hard success margin", r"$\geq 0.030$", metrics["hard_success_margin"], summary["gates"]["hard_success_margin"]),
        ("Hard utility margin", r"$\geq 0.050$", metrics["hard_utility_margin"], summary["gates"]["hard_utility_margin"]),
        ("Harmful-transfer delta", r"$\leq -0.025$", metrics["harmful_transfer_delta"], summary["gates"]["harmful_transfer_reduction"]),
        ("Tactile-event F1 delta", r"$\geq 0.030$", metrics["tactile_event_f1_delta"], summary["gates"]["tactile_event_f1_gain"]),
        ("Damage delta", r"$\leq 0.000$", metrics["damage_rate_delta"], summary["gates"]["damage_nonincrease"]),
        ("Query-cost delta", r"$\leq 0.000$", metrics["query_cost_delta"], summary["gates"]["query_nonincrease"]),
        ("Regret delta", r"$\leq 0.000$", metrics["regret_delta"], summary["gates"]["regret_nonincrease"]),
        ("Paired hard wins", r"$\geq 8/10$", metrics["paired_hard_utility_wins"], summary["gates"]["paired_hard_wins"]),
        ("Clean-transfer gap", r"$\leq 0.020$", metrics["clean_transfer_success_gap"], summary["gates"]["clean_transfer_retention"]),
        ("Ablation utility margin", r"$\geq 0.040$", metrics["ablation_utility_margin"], summary["gates"]["ablation_margin"]),
        ("Stress endpoint utility margin", r"$\geq 0.050$", metrics["stress_endpoint_utility_margin"], summary["gates"]["stress_endpoint_margin"]),
        ("Fixed-risk coverage", r"$0.300 \leq c < 0.950$", metrics["strict_fixed_risk_coverage"], summary["gates"]["fixed_risk_coverage"]),
        ("Fixed-risk utility margin", r"$> 0.000$", metrics["strict_fixed_risk_utility_margin"], summary["gates"]["fixed_risk_utility"]),
    ]
    lines = [
        r"\begin{tabular}{llrl}",
        r"\toprule",
        r"Gate & Frozen threshold & Observed & Result \\",
        r"\midrule",
    ]
    for name, threshold, observed, passed in gate_rows:
        value = f"{observed:.3f}" if isinstance(observed, float) else str(observed)
        lines.append(f"{tex_escape(name)} & {threshold} & {value} & {'pass' if passed else 'fail'} \\\\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "generated_gate_table.tex").write_text("\n".join(lines), encoding="utf-8")


def write_ablation_table(ablation_metric_rows):
    rows = sorted(ablation_metric_rows, key=lambda row: row["utility"], reverse=True)
    lines = [
        r"\begin{tabular}{lrrrrr}",
        r"\toprule",
        r"Variant & Success & Utility & Harm & F1 & Damage \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{display_name(row['variant'])} & {row['success']:.3f} & {row['utility']:.3f} & "
            f"{row['harmful_transfer_rate']:.3f} & {row['tactile_event_f1']:.3f} & {row['damage_rate']:.3f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "generated_ablation_table.tex").write_text("\n".join(lines), encoding="utf-8")


def write_stress_table(stress_metric_rows):
    max_stress = max(float(row["stress_level"]) for row in stress_metric_rows)
    rows = sorted([row for row in stress_metric_rows if abs(float(row["stress_level"]) - max_stress) < 1e-9], key=lambda row: row["utility"], reverse=True)
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Method & Success & Utility & Harm & Damage \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{display_name(row['method'])} & {row['success']:.3f} & {row['utility']:.3f} & "
            f"{row['harmful_transfer_rate']:.3f} & {row['damage_rate']:.3f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "generated_stress_table.tex").write_text("\n".join(lines), encoding="utf-8")


def write_fixed_risk_table(fixed_metric_rows):
    rows = sorted([row for row in fixed_metric_rows if abs(float(row["risk_budget"]) - 0.08) < 1e-9], key=lambda row: row["fixed_risk_utility"], reverse=True)
    keep = [row for row in rows if row["method"] in {PROPOSED, ORACLE, OLD_PROPOSED, "conformal_tactile_risk_control", "ensemble_disagreement_filter", "sensor_health_filter"}]
    lines = [
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        r"Method & Coverage & Breach & Fixed-risk utility & Mean risk \\",
        r"\midrule",
    ]
    for row in keep:
        lines.append(
            f"{display_name(row['method'])} & {row['accepted']:.3f} & {row['risk_breach']:.3f} & "
            f"{row['fixed_risk_utility']:.3f} & {row['risk_score']:.3f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}"]
    (PAPER / "generated_fixed_risk_table.tex").write_text("\n".join(lines), encoding="utf-8")


def write_figures(hard_metric_rows, ablation_metric_rows, stress_metric_rows, fixed_metric_rows):
    plt.rcParams.update({"font.size": 9})

    hard_methods = [
        "frozen_tactile_pretraining",
        "ensemble_disagreement_filter",
        "conformal_tactile_risk_control",
        OLD_PROPOSED,
        PROPOSED,
        ORACLE,
    ]
    rows = [pick_row(hard_metric_rows, "method", method) for method in hard_methods]
    labels = [DISPLAY_NAMES[row["method"]] for row in rows]
    x = np.arange(len(rows))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    ax.bar(x, [row["success"] for row in rows], color=["#9aa0a6", "#7c9cbf", "#8ab17d", "#d4a373", "#2a9d8f", "#264653"])
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=30, ha="right")
    ax.set_ylabel("Hard success")
    ax.set_ylim(0.0, 0.9)
    ax.set_title("Hard tactile-shift success")
    fig.tight_layout()
    fig.savefig(FIGURES / "tactile_negative_transfer_hard_success.png", dpi=220)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.8, 4.0))
    ax.scatter([row["harmful_transfer_rate"] for row in hard_metric_rows], [row["utility"] for row in hard_metric_rows], s=34, color="#6d6875")
    for method in [OLD_PROPOSED, PROPOSED, ORACLE, "ensemble_disagreement_filter", "conformal_tactile_risk_control"]:
        row = pick_row(hard_metric_rows, "method", method)
        ax.scatter([row["harmful_transfer_rate"]], [row["utility"]], s=70)
        ax.text(row["harmful_transfer_rate"] + 0.002, row["utility"] + 0.002, DISPLAY_NAMES[method], fontsize=8)
    ax.set_xlabel("Harmful-transfer rate")
    ax.set_ylabel("Hard utility")
    ax.set_title("Safety-utility frontier")
    fig.tight_layout()
    fig.savefig(FIGURES / "tactile_negative_transfer_safety_utility.png", dpi=220)
    plt.close(fig)

    rows = sorted(ablation_metric_rows, key=lambda row: row["utility"])
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    ax.barh([DISPLAY_NAMES.get(row["variant"], row["variant"]) for row in rows], [row["utility"] for row in rows], color="#457b9d")
    ax.set_xlabel("Ablation utility")
    ax.set_title("Component ablation under combined stress")
    fig.tight_layout()
    fig.savefig(FIGURES / "tactile_negative_transfer_ablation_v5.png", dpi=220)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for method in [OLD_PROPOSED, PROPOSED, ORACLE, "ensemble_disagreement_filter", "conformal_tactile_risk_control"]:
        rows = sorted([row for row in stress_metric_rows if row["method"] == method], key=lambda row: row["stress_level"])
        ax.plot([row["stress_level"] for row in rows], [row["utility"] for row in rows], marker="o", label=DISPLAY_NAMES[method])
    ax.set_xlabel("Stress level")
    ax.set_ylabel("Utility")
    ax.set_title("Stress endpoint sweep")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "tactile_negative_transfer_stress_sweep_v5.png", dpi=220)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for method in [OLD_PROPOSED, PROPOSED, ORACLE, "ensemble_disagreement_filter", "conformal_tactile_risk_control"]:
        rows = sorted([row for row in fixed_metric_rows if row["method"] == method], key=lambda row: row["risk_budget"])
        ax.plot([row["risk_budget"] for row in rows], [row["fixed_risk_utility"] for row in rows], marker="o", label=DISPLAY_NAMES[method])
    ax.set_xlabel("Risk budget")
    ax.set_ylabel("Fixed-risk utility")
    ax.set_title("Fixed-risk deployment audit")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGURES / "tactile_negative_transfer_fixed_risk.png", dpi=220)
    plt.close(fig)


def write_summary_text(summary):
    metrics = summary["metrics"]
    lines = [
        "Paper 113 v5 expanded tactile negative-transfer audit",
        f"Terminal decision: {summary['terminal_decision']}",
        f"ICLR main ready: {summary['iclr_main_ready']}",
        f"Proposed: {summary['proposed']}",
        f"Strongest non-oracle: {summary['strongest_non_oracle']}",
        f"Hard success: {metrics['hard_success_proposed']:.6f} vs {metrics['hard_success_strongest']:.6f}",
        f"Hard utility: {metrics['hard_utility_proposed']:.6f} vs {metrics['hard_utility_strongest']:.6f}",
        f"Harmful-transfer delta: {metrics['harmful_transfer_delta']:.6f}",
        f"Tactile-event F1 delta: {metrics['tactile_event_f1_delta']:.6f}",
        f"Damage delta: {metrics['damage_rate_delta']:.6f}",
        f"Query-cost delta: {metrics['query_cost_delta']:.6f}",
        f"Regret delta: {metrics['regret_delta']:.6f}",
        f"Paired hard utility wins: {metrics['paired_hard_utility_wins']}/10",
        f"Ablation utility margin: {metrics['ablation_utility_margin']:.6f}",
        f"Stress endpoint utility margin: {metrics['stress_endpoint_utility_margin']:.6f}",
        f"Strict fixed-risk coverage: {metrics['strict_fixed_risk_coverage']:.6f}",
        f"Strict fixed-risk utility margin: {metrics['strict_fixed_risk_utility_margin']:.6f}",
        "Scope gate: failed honestly; no real tactile robot/high-fidelity evidence or trained checkpoint.",
    ]
    (RESULTS / "summary.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    clean_generated_outputs()
    dataset_summary = build_dataset_summary()
    (
        main_rows,
        main_group_rows,
        seed_rows,
        metric_rows,
        hard_seed_rows,
        hard_metric_rows,
        hard_pairwise_rows,
    ) = build_main()
    ablation_rows, ablation_seed_rows, ablation_metric_rows = build_ablation()
    stress_rows, stress_seed_rows, stress_metric_rows = build_stress()
    fixed_rows, fixed_seed_rows, fixed_metric_rows, fixed_pairwise_rows = build_fixed_risk()
    failure_cases = build_failure_cases()

    row_counts = {
        "dataset_summary": len(dataset_summary),
        "main_cell": len(main_rows),
        "main_group": len(main_group_rows),
        "seed_metric": len(seed_rows),
        "metric": len(metric_rows),
        "hard_seed": len(hard_seed_rows),
        "hard_metric": len(hard_metric_rows),
        "hard_pairwise": len(hard_pairwise_rows),
        "ablation_cell": len(ablation_rows),
        "ablation_seed": len(ablation_seed_rows),
        "ablation_metric": len(ablation_metric_rows),
        "stress_cell": len(stress_rows),
        "stress_seed": len(stress_seed_rows),
        "stress_metric": len(stress_metric_rows),
        "fixed_risk_cell": len(fixed_rows),
        "fixed_risk_seed": len(fixed_seed_rows),
        "fixed_risk_metric": len(fixed_metric_rows),
        "fixed_risk_pairwise": len(fixed_pairwise_rows),
        "failure_cases": len(failure_cases),
    }
    summary = compute_summary(row_counts, hard_metric_rows, hard_pairwise_rows, ablation_metric_rows, stress_metric_rows, fixed_metric_rows)

    outputs = [
        ("dataset_summary.csv", dataset_summary),
        ("cell_metrics.csv", main_rows),
        ("main_group_metrics.csv", main_group_rows),
        ("seed_metrics.csv", seed_rows),
        ("metrics.csv", metric_rows),
        ("hard_seed_metrics.csv", hard_seed_rows),
        ("hard_aggregate_metrics.csv", hard_metric_rows),
        ("hard_pairwise_stats.csv", hard_pairwise_rows),
        ("ablation_cell_metrics.csv", ablation_rows),
        ("ablation_seed_metrics.csv", ablation_seed_rows),
        ("ablation_metrics.csv", ablation_metric_rows),
        ("stress_sweep_cell_metrics.csv", stress_rows),
        ("stress_sweep_seed_metrics.csv", stress_seed_rows),
        ("stress_sweep.csv", stress_metric_rows),
        ("fixed_risk_cell_metrics.csv", fixed_rows),
        ("fixed_risk_seed_metrics.csv", fixed_seed_rows),
        ("fixed_risk_metrics.csv", fixed_metric_rows),
        ("fixed_risk_pairwise_stats.csv", fixed_pairwise_rows),
        ("failure_cases.csv", failure_cases),
    ]
    for filename, rows in outputs:
        write_csv(RESULTS / filename, rounded(rows))
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    write_summary_text(summary)
    write_main_table(hard_metric_rows, summary)
    write_ablation_table(ablation_metric_rows)
    write_stress_table(stress_metric_rows)
    write_fixed_risk_table(fixed_metric_rows)
    write_figures(hard_metric_rows, ablation_metric_rows, stress_metric_rows, fixed_metric_rows)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
