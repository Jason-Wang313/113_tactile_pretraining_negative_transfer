# 113 Tactile Pretraining Negative Transfer

Submission-hardening version: v4.1

Terminal decision: STRONG_REVISE for an ICLR-main-target robotics submission package.

This rebuild replaces the archive/template scaffold with a paper-specific local benchmark for tactile pretraining negative transfer. The v4.1 continuation audit expands stress and failure coverage while preserving the same honest decision: an action-critical negative-transfer guard beats the strongest non-oracle tactile-transfer baseline under combined contact stress, but the paper is not yet ICLR-main ready because it still lacks real robot or external high-fidelity validation.

## Evidence Snapshot

- Design: 5 contact-rich tasks x 7 tactile shift regimes x 5 train/test splits x 9 methods, 7 paired seeds, 84 rollout episodes per group.
- Strongest non-oracle baseline: `ensemble_disagreement_filter`.
- Combined-stress success: proposed `0.648 +/- 0.009` vs baseline `0.542 +/- 0.009`.
- Paired difference: `0.106 +/- 0.008`, wins `7/7` seeds.
- Harmful-transfer delta: `-0.045`.
- Tactile-event F1 delta: `+0.056`.
- Damage delta: `-0.019`; query-cost delta: `-0.031`.
- Best ablation gap: `0.026` success behind the full method.
- Stress sweep coverage: `5,880` task/regime/seed rows plus `24` aggregate rows.
- Failure cases: `8` documented tactile-transfer boundaries.
- Latest rerun log: `C:/Users/wangz/robotics_massive_pool_paper_factory/logs/113_tactile_pretraining_negative_transfer_continuation_rerun_20260615.log`.

## Reproduce

```powershell
pip install -r requirements.txt
python src\run_experiment.py
```

## Rebuild PDF

```powershell
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Canonical local PDF: `C:/Users/wangz/Downloads/113.pdf`

PDF SHA256: `1D96558152C75EC2AE38B7946F4F171FCFF4EB2DD813DFFA76CE985FC1ADF945`

PDF size: `410386` bytes.

Artifact rule: keep the numbered PDF in Downloads only; do not copy it to the visible Desktop.
