# Literature Map

## Tactile Control And Reactive Manipulation

Prior tactile-control work shows that high-bandwidth contact feedback improves grasp adjustment, force stabilization, and contact-rich manipulation. Paper 113 does not compete by claiming a better tactile controller. It studies when broad tactile pretraining harms downstream controllers under shifted contact physics.

## Tactile Representation And Diffusion Policies

Recent tactile representation and tactile-diffusion systems motivate the pretraining setting. The hostile boundary is that pretrained tactile encoders may encode source-domain regularities that invert on new materials, textures, wear states, latency profiles, or taxel biases. The proposed guard tests whether action-critical tactile channels should be retained or rejected.

## Transfer, Domain Adaptation, And Sim-To-Real

Domain-adversarial transfer, invariant-risk transfer, fine-tuning, and test-time adaptation are natural baselines. In the local benchmark, they preserve some clean-transfer benefit but remain vulnerable under combined contact shifts. The proposed contribution is a negative-transfer gate tied to control consequences rather than only representation invariance.

## Uncertainty, Ensemble, And Retained Prior Guarding

Uncertainty gates and ensemble disagreement filters are close competitors, but the strongest v5 non-oracle comparator is the retained previous guard, `proposed_negative_transfer_guard_v4`. The new method improves hard success by `+0.04684`, hard utility by `+0.08172`, and wins `10/10` paired hard utility seeds while reducing harmful transfer, damage, query cost, and regret.

## Remaining Related-Work Work

This map is still a hostile-pool synthesis, not a final related-work section. A submission-ready version needs manual full-paper reading and precise comparisons to specific tactile policy, tactile representation, sim-to-real, and robot-safety methods.
