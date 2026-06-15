# Novelty Boundary Map

## Inside The Claim

- Detecting when tactile source pretraining becomes action-critical negative transfer.
- Separating harmful tactile channels from useful clean-transfer features.
- Calibrating a feature gate under friction, compliance, texture, shear, and taxel-bias shifts.
- Showing control metrics, not just representation diagnostics.

## Outside The Claim

- Real hardware SOTA.
- Universal tactile representation learning.
- A replacement for tactile sensor-health diagnostics.
- Solving semantic ambiguity in tactile observations.
- External benchmark generality.

## Closest Baseline Boundary

The closest local competitor is `ensemble_disagreement_filter`. It is strong because it rejects uncertain tactile features, but it does not know whether disagreement is action-critical or merely representation noise. The proposed guard wins by `0.106 +/- 0.008` combined-stress success and reduces harmful transfer, damage, and query cost.
