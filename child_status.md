# Child Status 113

Current stage: ICLR main gate terminal
Last update: 2026-06-15 02:39:00 +0100
PDF: C:/Users/wangz/Downloads/113.pdf
GitHub: https://github.com/Jason-Wang313/113_tactile_pretraining_negative_transfer
Submission-hardening version: v4
Terminal decision: STRONG_REVISE
ICLR main ready: no

Evidence digest:
- Proposed negative-transfer guard beats the strongest non-oracle baseline, `ensemble_disagreement_filter`, by `0.106 +/- 0.008` combined-stress success with `7/7` paired-seed wins.
- Proposed success is `0.648 +/- 0.009`; strongest baseline success is `0.542 +/- 0.009`.
- Harmful-transfer rate, damage, and query cost decrease; tactile-event F1 increases.
- Best ablation trails the full method by `0.026` success.
- Remaining blocker: no real robot or external high-fidelity benchmark validation.
