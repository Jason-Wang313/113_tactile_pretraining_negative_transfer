# Hostile Prior Work

The hostile set contains 100 papers from the shared robotics literature pool. The strongest threats are tactile control, tactile-diffusion policy, tactile representation, and sim-to-real transfer work:

- High-Bandwidth Tactile-Reactive Control for Grasp Adjustment (2025)
- PolyTouch: A Robust Multi-Modal Tactile Sensor for Contact-rich Manipulation Using Tactile-Diffusion Policies (2025)
- TranTac: Leveraging Transient Tactile Signals for Contact-Rich Robotic Manipulation (2025)
- exUMI: Extensible Robot Teaching System with Action-aware Task-agnostic Tactile Representation (2025)
- ManipForce: Force-Guided Policy Learning with Frequency-Aware Representation for Contact-Rich Manipulation (2025)
- Grasping Force Control of Multi-Fingered Robotic Hands through Tactile Sensing for Object Stabilization (2020)
- Magnetic-based Soft Tactile Sensors with Deformable Continuous Force Transfer Medium for Resolving Contact Locations in Robotic Grasping and Manipulation (2019)
- Sim2Real Transfer of Imitation Learning of Motion Control for Car-like Mobile Robots Using Digital Twin Testbed (2025)

## Novelty Pressure

These papers make tactile sensing, tactile policy learning, tactile diffusion, and sim-to-real transfer crowded. The v4 contribution therefore cannot be "tactile pretraining helps" or "add uncertainty." The defensible boundary is narrower: source tactile pretraining can become harmful under contact-regime shift, and a control-conditioned negative-transfer guard can reject harmful pretrained channels while preserving clean-transfer benefit.

## Evidence Boundary

The local benchmark supports this narrower boundary against frozen pretraining, full fine-tuning, domain-adversarial transfer, uncertainty gating, and ensemble disagreement filtering. It does not settle real hardware generality.
