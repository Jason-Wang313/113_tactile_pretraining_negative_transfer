# Submission Readiness Decision

Decision: STRONG_REVISE

ICLR main-conference readiness: NO.

Reason: The v4 rebuild adds a paper-specific tactile negative-transfer benchmark with strong local evidence. The proposed guard beats the strongest non-oracle baseline by `0.106 +/- 0.008` combined-stress success, wins `7/7` paired seeds, improves harmful-transfer, tactile-event, damage, and query-cost diagnostics, and survives ablations.

Honest terminal action: keep and revise aggressively. Do not submit as final ICLR main paper until external validation is added.

Revival-to-ready condition: add real robot or accepted high-fidelity simulator experiments, train/release tactile encoders, compare to external tactile policy baselines, and deepen related work through manual full-paper reading.
