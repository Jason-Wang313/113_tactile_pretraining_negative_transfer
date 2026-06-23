# Claims

- Mechanism claim: tactile pretraining can create action-critical negative transfer when source tactile features encode contact regularities that invert under downstream friction, compliance, texture, wear, latency, or sensor-bias shifts.
- Method claim: an action-critical mismatch detector plus calibrated tactile feature gate can retain useful pretrained channels while rejecting harmful channels.
- Evidence claim: the v5 local benchmark shows `action_critical_tactile_transfer_guard_v5` beats the strongest non-oracle retained guard, `proposed_negative_transfer_guard_v4`, with hard success `0.74719` vs `0.70035`, hard utility `0.63479` vs `0.55307`, and `10/10` paired hard utility wins.
- Stress and safety claim: the method improves harmful-transfer rate by `-0.02940`, tactile-event F1 by `+0.10400`, damage rate by `-0.01333`, query cost by `-0.02280`, regret by `-0.01132`, and strict fixed-risk utility by `+0.49760`.
- Evidence-scale claim: the current package contains 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases.
- Scope claim: the result is strong local evidence for an expanded submission rebuild, not final ICLR-main readiness.
- Unsupported claim explicitly avoided: no claim of real-robot SOTA, external benchmark superiority, deployed safety, or hardware-calibrated tactile transfer.
