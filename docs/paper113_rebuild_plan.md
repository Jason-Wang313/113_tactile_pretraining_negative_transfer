# Paper 113 Rebuild Plan

Started: 2026-06-15 02:27:00 +0100

## Goal

Rebuild `tactile_pretraining_negative_transfer` from an archive memo into a real local empirical submission package. The paper must test whether tactile pretraining can cause physical negative transfer under contact-regime shift, and whether an explicit negative-transfer guard can retain useful tactile transfer while refusing harmful pretrained features.

## Claim To Test

Tactile representations pretrained on broad contact data are not uniformly helpful for downstream robot control. A controller that estimates action-critical tactile feature mismatch and gates harmful pretrained channels should beat strong tactile-pretraining baselines under shifted contact regimes without sacrificing clean-transfer performance.

## Evidence Design

- Benchmark dimensions: 5 contact-rich manipulation tasks, 7 tactile shift regimes, 5 train/test splits, 9 methods, 7 paired seeds, 84 rollout episodes per task/regime/split/seed/method.
- Methods: no-tactile policy, scratch tactile learner, frozen pretrained tactile encoder, full fine-tuning, domain-adversarial tactile transfer, uncertainty-gated transfer, ensemble disagreement filter, proposed negative-transfer guard, and oracle feature selector.
- Metrics: task success, harmful-transfer rate, clean-transfer retention, tactile-event F1, slip/drop damage, intervention/query cost, calibration error, and paired-seed wins.
- Stress sweep: increasing mismatch between source tactile pretraining and downstream contact physics.
- Ablations: remove mismatch detector, remove action-critical feature mask, remove clean-transfer retention term, remove slip/drop cost model, classifier-only guard, and no calibration guard.

## Terminal Gates

The paper may become `STRONG_REVISE` only if the proposed method clears all gates against the strongest non-oracle baseline:

- Combined-stress task-success margin is at least 0.030.
- Harmful-transfer rate decreases by at least 0.020.
- Clean-transfer success does not decrease by more than 0.005.
- Tactile-event F1 increases by at least 0.030.
- Damage and intervention/query cost do not increase.
- Paired-seed success wins are at least 5/7.
- Best ablation trails the full method by at least 0.020.

If any gate fails, the terminal state remains `KILL_ARCHIVE` with the negative result documented.

## Execution Steps

1. Replace the generic branch-mechanism script with a paper-specific tactile negative-transfer benchmark.
2. Generate raw per-seed/per-task/per-regime evidence, aggregate metrics, pairwise tests, stress-sweep outputs, ablation tables, and failure cases.
3. Replace stale branch-mechanism artifacts and remove obsolete `raw_seed_metrics.csv`, `negative_cases.csv`, and `figures/stress_curve_data.csv` if superseded.
4. Rewrite the README, child status, ICLR gate, claims, attack log, novelty docs, reproducibility checklist, and final audit around the new evidence.
5. Rewrite the manuscript as an ICLR-style evidence report with tables, figures, limitations, and honest readiness decision.
6. Compile the PDF and copy the numbered artifact to `C:/Users/wangz/Downloads/113.pdf` only.
7. Audit Python, LaTeX, CSV finiteness, stale outputs, Git status, Downloads-only PDF placement, and public GitHub visibility.
8. Update the root batch/status/master reports only after the paper reaches a terminal decision.
