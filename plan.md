# Paper 113 v5 Frozen Submission Plan

Paper: `113_tactile_pretraining_negative_transfer`

Date: 2026-06-23

Target posture: ICLR-main hostile-review readiness audit, CPU-only and RAM-light.

## Goal

Rebuild Paper 113 into a 25+ page, evidence-bound submission artifact about tactile pretraining negative transfer. The rebuild must add theory, stronger baselines, wider stress tests, fixed-risk deployment analysis, ablations, failure cases, reproducibility checks, and bright boxed clickable citations while preserving the honest conclusion that the work is not ICLR-main ready without real tactile robot or accepted high-fidelity validation.

## Frozen Method Hypothesis

Tactile pretraining can be harmful when source-domain contact features invert under downstream friction, compliance, texture, shear, taxel-bias, latency, geometry, or sensor-health shifts. A useful transfer method should decide at the action-critical tactile-channel level when pretrained features are beneficial, harmful, or too risky to use. The proposed v5 method, `action_critical_tactile_transfer_guard_v5`, must outperform generic transfer, domain-adaptation, uncertainty, risk, and the retained v4.1 proposed guard under hostile contact-shift splits.

## Frozen Experimental Scope

- Main audit: 10 tasks x 8 tactile regimes x 8 deployment splits x 16 methods x 10 paired seeds = 102,400 cell rows.
- Aggregation: 10,240 task/regime/split/method rows, 1,280 method/split/seed rows, and 128 method/split metric rows.
- Hard aggregate: 160 method/seed rows, 16 method rows, and 15 paired comparisons against the proposed v5 method.
- Ablations: 10 variants x 10 tasks x 8 regimes x 10 seeds = 8,000 cell rows.
- Stress sweep: 6 stress levels x 10 methods x 10 tasks x 8 regimes x 10 seeds = 48,000 cell rows.
- Fixed-risk audit: 4 deployment risk budgets x 16 methods x 10 tasks x 8 regimes x 10 seeds = 51,200 cell rows.
- Failure analysis: 24 predefined boundary cases spanning aliasing, latency, taxel failures, over-rejection, unseen geometry, damage asymmetry, and oracle headroom.

## Strong Baselines

The non-oracle comparator set includes no tactile transfer, scratch tactile policy, frozen tactile pretraining, full fine-tuning, domain-adversarial transfer, invariant-risk tactile alignment, uncertainty-gated transfer, ensemble disagreement filtering, conformal tactile risk control, sensor-health filtering, test-time adaptation, masked autoencoder tactile pretraining, contrastive tactile pretraining, and the v4.1 proposed guard retained as `proposed_negative_transfer_guard_v4`.

## Frozen Local Gates

Paper 113 may remain `STRONG_REVISE` only if every local gate passes:

- Hard success margin over the strongest non-oracle baseline is at least 0.030.
- Hard utility margin over the strongest non-oracle baseline is at least 0.050.
- Harmful-transfer rate decreases by at least 0.025.
- Tactile-event F1 improves by at least 0.030.
- Damage, query cost, and regret do not increase.
- Proposed v5 wins at least 8/10 paired hard-utility seeds.
- Clean-transfer success remains within 0.020 of the best clean-transfer non-oracle method.
- The best removed-component ablation remains below the full method by at least 0.010 success or 0.040 utility.
- Stress endpoint utility margin is at least 0.050.
- Strict fixed-risk coverage is at least 0.300 and below 0.950, with positive fixed-risk utility margin.

## Scope Gate

The scope gate is intentionally separate and must fail for this local-only rebuild. The manuscript and ledgers must state that ICLR-main readiness remains `no` because the work lacks real tactile robot rollouts, accepted high-fidelity tactile simulation, trained policy checkpoints, sensor calibration logs, released tactile datasets/checkpoints, and rollout-video evidence.

## Artifact Rules

- Build manuscript claims from generated CSVs, tables, figures, and `summary.json`; avoid hand-entered result drift.
- Use bright boxed clickable citations.
- Validate CSV row counts, numeric finiteness, local gates, PDF page count, PDF hash, LaTeX/BibTeX logs, and artifact locations.
- Keep final numbered PDF only at `C:/Users/wangz/Downloads/113.pdf`; do not copy it to the visible Desktop.
