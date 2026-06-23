# Novelty Boundary Map

## Inside The Claim

- Detecting when tactile source pretraining becomes action-critical negative transfer.
- Separating harmful tactile channels from useful clean-transfer features.
- Calibrating a feature gate under friction, compliance, texture, shear, wear, latency, and taxel-bias shifts.
- Showing control metrics, safety diagnostics, fixed-risk behavior, and failure boundaries, not just representation diagnostics.

## Outside The Claim

- Real hardware SOTA.
- Universal tactile representation learning.
- A replacement for tactile sensor-health diagnostics.
- Solving semantic ambiguity in tactile observations.
- External benchmark generality.
- Deployed safety under calibrated hardware.

## Closest Baseline Boundary

The closest current local competitor is the retained previous guard, `proposed_negative_transfer_guard_v4`. It is strong because it already encodes a contact-shift rejection mechanism. The v5 guard still wins by `+0.04684` hard success and `+0.08172` hard utility, with `10/10` paired hard utility wins and better harmful-transfer, tactile-event F1, damage, query-cost, regret, stress-endpoint, and fixed-risk diagnostics.
