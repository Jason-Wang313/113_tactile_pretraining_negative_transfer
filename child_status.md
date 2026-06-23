# Child Status 113

Current stage: expanded-standard v5 terminal
Last update: 2026-06-23 14:24:29 +08:00
PDF: C:/Users/wangz/Downloads/113.pdf
PDF SHA256: D236462522C6A55DFFF55DA69B7D6681D6731A90C051D9AE2137F406302CA7F5
PDF pages: 25
PDF bytes: 628073
GitHub: https://github.com/Jason-Wang313/113_tactile_pretraining_negative_transfer
Submission-hardening version: v5_expanded
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence digest:
- Proposed method `action_critical_tactile_transfer_guard_v5` beats strongest non-oracle `proposed_negative_transfer_guard_v4`.
- Hard success is `0.74719` proposed vs `0.70035` strongest non-oracle.
- Hard utility is `0.63479` proposed vs `0.55307` strongest non-oracle.
- Paired hard utility wins are `10/10`.
- Harmful-transfer, damage, query cost, and regret decrease; tactile-event F1 increases.
- Evidence scale is 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases.
- All frozen local gates pass.
- Remaining blocker: no real tactile robot rollouts, no accepted high-fidelity tactile simulator validation, no trained checkpoint/calibration/video evidence, and no released tactile dataset.
