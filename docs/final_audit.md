# Final Audit

Paper: 113 tactile_pretraining_negative_transfer

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE

ICLR main ready: NO

## Evidence

The v5 rebuild expands the tactile negative-transfer package into a 25-page submission audit. The frozen CPU-only experiment evaluates 10 tasks, 8 tactile shift regimes, 8 splits, 16 methods, and 10 paired seeds. It records 102,400 main cells, 10,240 main group rows, 1,280 seed metrics, 128 aggregate metrics, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases.

Key results:
- Proposed method: `action_critical_tactile_transfer_guard_v5`.
- Strongest non-oracle: `proposed_negative_transfer_guard_v4`.
- Oracle: `oracle_contact_shift_feature_selector`.
- Hard success: `0.74719` proposed vs `0.70035` strongest non-oracle.
- Hard utility: `0.63479` proposed vs `0.55307` strongest non-oracle.
- Hard margins: success `+0.04684`, utility `+0.08172`.
- Paired hard utility wins: `10/10`.
- Harmful-transfer delta: `-0.02940`.
- Tactile-event F1 delta: `+0.10400`.
- Damage-rate delta: `-0.01333`.
- Query-cost delta: `-0.02280`.
- Regret delta: `-0.01132`.
- Ablation utility margin: `+0.03438`.
- Stress endpoint utility margin: `+0.08478`.
- Strict fixed-risk budget: `0.06000`.
- Strict fixed-risk coverage: `0.89750`.
- Strict fixed-risk breach: `0.01875`.
- Strict fixed-risk utility margin: `+0.49760`.
- Numeric integrity: no NaN or infinite values found by the validator.

Artifact audit passes: `C:/Users/wangz/Downloads/113.pdf` exists, has 25 pages, is 628,073 bytes, has SHA256 `D236462522C6A55DFFF55DA69B7D6681D6731A90C051D9AE2137F406302CA7F5`, and `C:/Users/wangz/Desktop/113.pdf` is absent.

## Remaining Risk

The result remains local evidence. It does not include real tactile robot rollouts, an accepted high-fidelity tactile simulator, trained policy checkpoints, tactile sensor calibration logs, a released tactile dataset/checkpoint, or rollout videos. The correct terminal action is strong revise, not ICLR-main-ready submission.
