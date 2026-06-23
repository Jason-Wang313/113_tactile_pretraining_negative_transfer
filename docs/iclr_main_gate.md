# ICLR Main Gate

Paper: 113 tactile_pretraining_negative_transfer

Earlier v3 decision: KILL_ARCHIVE

v5 gate verdict: STRONG_REVISE

Evidence digest: tactile-negative-transfer-local-v5-expanded

## Passed Local Gates

- Hard success margin over strongest non-oracle baseline: `0.04684 > 0`.
- Hard utility margin over strongest non-oracle baseline: `0.08172 > 0`.
- Harmful-transfer delta: `-0.02940 < 0`.
- Clean-transfer success gap: `0.00000 >= -0.005`.
- Tactile-event F1 delta: `+0.10400 > 0`.
- Damage-rate delta: `-0.01333 <= 0`.
- Query-cost delta: `-0.02280 <= 0`.
- Regret delta: `-0.01132 <= 0`.
- Paired hard utility wins: `10/10`.
- Ablation utility margin: `+0.03438`.
- Stress endpoint utility margin: `+0.08478`.
- Fixed-risk coverage: `0.89750`.
- Fixed-risk breach under strict budget `0.06000`: `0.01875`.
- Fixed-risk utility margin: `+0.49760`.
- Evidence scale: 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases.
- PDF integrity: 25 pages, bright boxed clickable citations, and Downloads-only final artifact.
- Numeric integrity: validator reports no NaN or infinite values.

## Failed Scope Gate

- No real tactile robot validation.
- No accepted high-fidelity tactile simulator benchmark.
- No trained tactile policy checkpoint release.
- No tactile sensor calibration logs.
- No released tactile dataset or checkpoint.
- No hardware rollout videos.

The only honest main-conference-safe terminal state is STRONG_REVISE.
