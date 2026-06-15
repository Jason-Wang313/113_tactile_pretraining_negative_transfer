# Literature Map

## Tactile Control And Reactive Manipulation

Prior tactile-control work shows that high-bandwidth contact feedback improves grasp adjustment, force stabilization, and contact-rich manipulation. Paper 113 does not compete by claiming a better tactile controller. It studies when broad tactile pretraining harms downstream controllers under shifted contact physics.

## Tactile Representation And Diffusion Policies

Recent tactile representation and tactile-diffusion systems motivate the pretraining setting. The hostile boundary is that pretrained tactile encoders may encode source-domain regularities that invert on new materials, textures, or taxel biases. The proposed guard tests whether action-critical tactile channels should be retained or rejected.

## Transfer, Domain Adaptation, And Sim-To-Real

Domain-adversarial transfer and fine-tuning are natural baselines. In the local benchmark, they preserve some clean-transfer benefit but remain vulnerable under combined friction/compliance/texture/sensor shifts. The proposed contribution is a negative-transfer gate tied to control consequences rather than only representation invariance.

## Uncertainty And Ensemble Filtering

Uncertainty gates and ensemble disagreement filters are the closest local competitors. The strongest non-oracle baseline is `ensemble_disagreement_filter`. The proposed guard beats it by `0.106 +/- 0.008` combined-stress success while reducing harmful transfer, damage, and query cost.

## Remaining Related-Work Work

This map is still a hostile-pool synthesis, not a final related-work section. A submission-ready version needs manual full-paper reading and precise comparisons to specific tactile policy and tactile representation methods.
