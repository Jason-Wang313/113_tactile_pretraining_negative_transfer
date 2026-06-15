# Final Audit

Paper: 113 tactile_pretraining_negative_transfer

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE

## Evidence

The archive scaffold was replaced with a tactile negative-transfer benchmark. The benchmark evaluates 5 tasks, 7 tactile shift regimes, 5 splits, 9 methods, 7 seeds, and 84 rollout episodes per group. The proposed negative-transfer guard beats the strongest non-oracle baseline, `ensemble_disagreement_filter`, under combined stress.

Key results:
- Success: `0.648 +/- 0.009` proposed vs `0.542 +/- 0.009` strongest baseline.
- Paired difference: `0.106 +/- 0.008`; wins `7/7`.
- Harmful-transfer delta: `-0.045`.
- Tactile-event F1 delta: `+0.056`.
- Damage delta: `-0.019`.
- Query-cost delta: `-0.031`.
- Best ablation gap: `0.026`.
- Stress sweep coverage: `5,880` task/regime/seed rows and `24` aggregate rows.
- Failure cases: `8` documented tactile-transfer boundaries.
- Numeric integrity: no NaN or infinite values found across result CSVs.

Artifact audit passes: `C:/Users/wangz/Downloads/113.pdf` exists, is 410,386 bytes, has SHA256 `1D96558152C75EC2AE38B7946F4F171FCFF4EB2DD813DFFA76CE985FC1ADF945`, and `C:/Users/wangz/Desktop/113.pdf` is absent.

## Remaining Risk

The result is local benchmark evidence. It does not include real robot experiments, external tactile datasets, high-fidelity simulator transfer, trained checkpoint release, or hardware videos. The correct terminal action is strong revise, not ICLR-main-ready submission.
