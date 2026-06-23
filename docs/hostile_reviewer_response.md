# Hostile Reviewer Response

## Reviewer Attack: This is just uncertainty filtering with a new name.

Response: The v5 run retains uncertainty-style and ensemble baselines, but the strongest non-oracle competitor is now the previous v4 guard, `proposed_negative_transfer_guard_v4`. The v5 method reaches hard success `0.74719` and hard utility `0.63479`, compared with `0.70035` and `0.55307` for the retained v4 guard. It wins `10/10` paired hard utility seeds and also improves harmful-transfer rate, tactile-event F1, damage rate, query cost, and regret.

## Reviewer Attack: Frozen and fine-tuned tactile pretraining already solve this.

Response: The benchmark includes scratch, no-tactile, frozen-pretraining, full fine-tuning, domain-adversarial, invariant-risk, uncertainty, ensemble, conformal, sensor-health, test-time adaptation, masked-pretraining, contrastive-pretraining, retained v4, and oracle comparisons. The paper's claim is not that tactile pretraining never helps; it is that broad tactile pretraining becomes harmful when source contact regularities invert downstream, and the proposed guard rejects action-critical harmful channels while preserving clean-transfer benefit.

## Reviewer Attack: The mechanism is unnecessary.

Response: The v5 ablation gate is positive: best ablation utility trails the full method by `0.03438`, and best ablation success trails by `0.01693`. The fixed-risk and stress endpoint tests also remain positive, so the result is not only a main-table artifact.

## Reviewer Attack: The paper is not ready for ICLR main.

Response: Agreed. The honest decision is `STRONG_REVISE`, not ready. The v5 evidence is substantially stronger locally, with 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, 24 failure cases, a 25-page PDF, and a validator. It still needs real tactile robot or accepted high-fidelity validation, trained tactile checkpoints, calibration logs, released data/checkpoints, rollout videos, and external-baseline confirmation.
