# ICLR Main Gate

Paper: 113 tactile_pretraining_negative_transfer

Existing v3 decision: KILL_ARCHIVE

v4.1 gate verdict: STRONG_REVISE

Evidence digest: tactile-negative-transfer-local-v4.1

## Passed Local Gates

- Success margin over strongest non-oracle baseline: `0.106 >= 0.030`.
- Harmful-transfer delta: `-0.045 <= -0.020`.
- Clean-transfer delta vs strongest clean baseline: `+0.050 >= -0.005`.
- Tactile-event F1 delta: `+0.056 >= +0.030`.
- Damage delta: `-0.019 <= 0`.
- Query-cost delta: `-0.031 <= 0`.
- Paired-seed wins: `7/7 >= 5/7`.
- Ablation margin: `0.026 >= 0.020`.
- Expanded stress coverage: `5,880` task/regime/seed rows.
- Failure-case coverage: `8` rows.
- Numeric integrity: no NaN or infinite values.

## Remaining Main-Conference Blockers

- No real robot validation.
- No external high-fidelity simulator benchmark.
- No released trained tactile encoder/checkpoints.
- Related work still needs manual full-paper synthesis.

The only honest main-conference-safe terminal state is STRONG_REVISE.
