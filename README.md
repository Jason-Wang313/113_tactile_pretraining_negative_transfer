# 113 Tactile Pretraining Negative Transfer

Submission-hardening version: v5_expanded

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This expanded rebuild replaces the earlier v4.1 local package with a 25-page, evidence-heavy submission audit for tactile pretraining negative transfer. The proposed action-critical tactile transfer guard is stronger than the retained v4 guard under hard contact-shift evaluation, fixed-risk evaluation, ablations, and stress sweeps. The paper is still not ICLR-main ready because the evidence remains local and synthetic: no real tactile robot rollouts, accepted high-fidelity tactile simulation, trained policy checkpoints, calibration logs, released tactile dataset, or rollout videos are present.

## Evidence Snapshot

- Design: 10 contact-rich tasks x 8 tactile shift regimes x 8 train/test splits x 16 methods x 10 paired seeds.
- Main evidence: 102,400 main cells, 10,240 main group rows, 1,280 seed metrics, and 128 aggregate metrics.
- Additional evidence: 8,000 ablation cells, 48,000 stress cells, 51,200 fixed-risk cells, and 24 documented failure cases.
- Proposed method: `action_critical_tactile_transfer_guard_v5`.
- Strongest non-oracle baseline: `proposed_negative_transfer_guard_v4`.
- Oracle upper bound: `oracle_contact_shift_feature_selector`.
- Hard success: proposed `0.74719` vs strongest non-oracle `0.70035`.
- Hard utility: proposed `0.63479` vs strongest non-oracle `0.55307`.
- Hard margins: success `+0.04684`, utility `+0.08172`, with `10/10` paired hard-seed utility wins.
- Diagnostics: harmful-transfer delta `-0.02940`, tactile-event F1 delta `+0.10400`, damage-rate delta `-0.01333`, query-cost delta `-0.02280`, regret delta `-0.01132`.
- Fixed-risk result: strict budget `0.06000`, coverage `0.89750`, breach `0.01875`, utility margin `+0.49760`.
- Local gates: all frozen local gates pass.
- Scope gate: fails by design because external tactile evidence is absent.
- Citation behavior: in-text citations are bright boxed clickable links routed to the reference section.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
python scripts\generate_manuscript.py
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
cd ..
python scripts\validate_submission_artifacts.py
```

Canonical local PDF: `C:/Users/wangz/Downloads/113.pdf`

PDF SHA256: `D236462522C6A55DFFF55DA69B7D6681D6731A90C051D9AE2137F406302CA7F5`

PDF pages: `25`

PDF size: `628073` bytes.

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
