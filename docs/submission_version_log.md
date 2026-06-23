# Submission Version Log

## v1

Generated draft scaffold.

## v2

Workshop-level synthetic stress-test pass.

## v3

ICLR-main gate archive pass. Decision: KILL_ARCHIVE because the paper lacked paper-specific empirical evidence, implemented baselines, and real robot/high-fidelity validation.

## v4

Rebuilt as a tactile negative-transfer empirical package. Added a paper-specific benchmark, strong baselines, paired-seed tests, stress sweep, ablations, figures, tables, revised docs, and an evidence manuscript.

Terminal decision: STRONG_REVISE.

Remaining gap: real robot or external high-fidelity validation.

## v4.1

Reran the experiment under low-RAM thread caps, expanded stress/failure coverage, rechecked row counts and numeric integrity, and hardened manuscript/docs around the same evidence-bound terminal state.

Terminal decision: STRONG_REVISE.

Remaining gap: real robot or independent high-fidelity tactile validation, trained checkpoint release, and deeper manual related-work synthesis.

## v5_expanded

Expanded the paper to a 25-page submission-audit artifact without padding: added a frozen v5 plan, new method/theory framing, a larger CPU-only benchmark, stronger retained baselines, fixed-risk evaluation, broader stress tests, more failure cases, generated manuscript tables, bright boxed clickable citations, a validator, and rendered-PNG visual QA.

Evidence scale: 102,400 main cells, 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 failure cases.

Terminal decision: STRONG_REVISE.

Remaining gap: real tactile robot or accepted high-fidelity tactile validation, trained checkpoint release, sensor calibration logs, released tactile dataset/checkpoint, rollout videos, and external-baseline confirmation.
