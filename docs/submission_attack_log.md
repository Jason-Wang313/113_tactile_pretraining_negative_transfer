# Submission Attack Log

Paper: 113 tactile_pretraining_negative_transfer

The v5_expanded pass replaces the earlier v4.1 continuation package with a 25-page local submission audit. The result is `STRONG_REVISE`, not final ICLR-main readiness.

## Attack 1: No real robot validation.

Verdict: Still a blocker for readiness.

Action: Preserve `ICLR main ready: no`; require real tactile robot or accepted high-fidelity tactile validation before final submission.

## Attack 2: Synthetic/template evidence.

Verdict: Locally addressed, globally still limited.

Action: Expanded the paper-specific tactile negative-transfer benchmark to 10 tasks, 8 regimes, 8 splits, 16 methods, and 10 paired seeds, producing 102,400 main cells. This is real local evidence, but not a substitute for hardware or accepted external simulation.

## Attack 3: Weak baselines.

Verdict: Addressed locally.

Action: Included no-tactile, scratch, frozen, fine-tuned, domain-adversarial, invariant-risk, uncertainty, ensemble, conformal, sensor-health, test-time adaptation, masked-pretraining, contrastive-pretraining, retained v4 guard, and oracle comparisons.

## Attack 4: The proposed method is just uncertainty filtering.

Verdict: Addressed locally.

Action: The v5 guard beats the retained v4 guard by `+0.04684` hard success and `+0.08172` hard utility, wins `10/10` paired hard utility seeds, and improves harmful transfer, tactile-event F1, damage, query cost, and regret.

## Attack 5: Tactile pretraining may only help clean transfer.

Verdict: Addressed locally.

Action: Clean-transfer success gap is `0.00000`, while hard-shift and stress/fixed-risk margins remain positive.

## Attack 6: Components may be unnecessary.

Verdict: Addressed locally.

Action: Best ablation trails the full method by `0.01693` success and `0.03438` utility.

## Attack 7: Missing trained checkpoints.

Verdict: Still a blocker for readiness.

Action: Document as a remaining requirement. The v5 benchmark is evidence for a rebuild direction, not a final trained model release.

## Attack 8: Related work still shallow.

Verdict: Still a blocker for readiness.

Action: Hostile-pool map is preserved, but final submission needs manual full-paper synthesis and exact positioning against tactile representation/policy papers.

## Attack 9: Main-conference decision.

Verdict: STRONG_REVISE.

Action: Keep the paper alive and expand with external validation; do not mark as submission-ready.

## Attack 10: Stress/failure coverage is thin.

Verdict: Addressed locally.

Action: Expanded stress evidence to 48,000 stress cells, fixed-risk evidence to 51,200 cells, and failure documentation to 24 boundaries.
