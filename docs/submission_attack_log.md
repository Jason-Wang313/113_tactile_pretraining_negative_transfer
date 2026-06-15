# Submission Attack Log

Paper: 113 tactile_pretraining_negative_transfer

This v4 pass replaces the v3 archive decision with a stronger local empirical rebuild. The result is `STRONG_REVISE`, not final ICLR-main readiness.

## Attack 1: No real robot validation.

Verdict: Still a blocker for readiness.

Action: Preserve `ICLR main ready: no`; require real robot or external high-fidelity validation before final submission.

## Attack 2: Synthetic/template evidence.

Verdict: Partially addressed.

Action: Replaced the generic branch scaffold with a paper-specific tactile negative-transfer benchmark spanning 5 tasks, 7 tactile shift regimes, 5 splits, 9 methods, 7 seeds, and 84 rollout episodes per group.

## Attack 3: Weak baselines.

Verdict: Addressed locally.

Action: Added frozen pretraining, full fine-tuning, domain-adversarial transfer, uncertainty-gated transfer, ensemble disagreement filtering, scratch tactile learning, no-tactile control, and oracle feature selection.

## Attack 4: The proposed method is just uncertainty filtering.

Verdict: Addressed locally.

Action: The proposed guard beats `ensemble_disagreement_filter` by `0.106 +/- 0.008` success, wins `7/7` seeds, and has lower harmful transfer, damage, and query cost.

## Attack 5: Tactile pretraining may only help clean transfer.

Verdict: Addressed locally.

Action: Clean transfer is preserved: proposed clean-transfer success is `0.701`, while the strongest clean baseline, `full_finetune_pretrained`, is `0.651`.

## Attack 6: Components may be unnecessary.

Verdict: Addressed locally.

Action: Best removed-component ablation trails the full method by `0.026`, clearing the `0.020` gate. Removing mismatch detection, action-critical masking, clean-transfer retention, slip/drop cost, or calibration harms success and/or safety.

## Attack 7: Missing trained checkpoints.

Verdict: Still a blocker for readiness.

Action: Document as a remaining requirement. The v4 benchmark is evidence for a rebuild direction, not a final trained model release.

## Attack 8: Related work still shallow.

Verdict: Still a blocker for readiness.

Action: Hostile-pool map is updated, but final submission needs manual full-paper synthesis.

## Attack 9: Main-conference decision.

Verdict: STRONG_REVISE.

Action: Keep the paper alive and expand with external validation; do not mark as submission-ready.
