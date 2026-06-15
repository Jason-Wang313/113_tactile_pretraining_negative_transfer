# Hostile Reviewer Response

## Reviewer Attack: This is just "use uncertainty to ignore bad tactile features."

Response: The strongest uncertainty-style baseline is `ensemble_disagreement_filter`, which reaches `0.542 +/- 0.009` combined-stress success. The proposed action-critical negative-transfer guard reaches `0.648 +/- 0.009`, a paired `0.106 +/- 0.008` advantage with `7/7` seed wins. The method also lowers harmful-transfer rate and query cost, so the result is not merely more conservative uncertainty rejection.

## Reviewer Attack: Frozen and fine-tuned tactile pretraining already solve this.

Response: Frozen pretraining collapses under combined tactile shift (`0.463 +/- 0.012` success, harmful transfer `0.267`). Full fine-tuning improves clean transfer but remains vulnerable under combined stress (`0.512 +/- 0.010`, harmful transfer `0.210`). The paper's claim is precisely that broad tactile pretraining can be harmful when source contact regularities invert downstream.

## Reviewer Attack: The mechanism is unnecessary.

Response: The ablation table rejects that. The full guard reaches `0.641 +/- 0.008` in the ablation benchmark, while the best removed-component variant, `minus_slip_damage_cost`, reaches `0.616 +/- 0.009`. Removing the mismatch detector, action-critical mask, clean-transfer retention, calibration guard, or replacing the mechanism with a classifier-only guard all weakens performance and/or safety diagnostics.

## Reviewer Attack: The paper is not ready for ICLR main.

Response: Agreed. The honest decision is `STRONG_REVISE`, not ready. The evidence is now paper-specific and locally rigorous, but the submission still needs real robot or external high-fidelity validation, trained tactile checkpoints, and deeper manual related work.
