# Submission Readiness Audit v4.1

Paper: 113 `tactile_pretraining_negative_transfer`

Date: 2026-06-15

Terminal decision: STRONG_REVISE

ICLR main ready: no

## Evidence Rerun

Command:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\113_tactile_pretraining_negative_transfer_continuation_rerun_20260615.log
```

## Integrity Gates

- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1,575 rows.
- `seed_task_regime_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 24 rows.
- `stress_sweep_seed_metrics.csv`: 5,880 task/regime/seed rows.
- `failure_cases.csv`: 8 rows.
- Numeric sanity: no NaN or infinite values found.

## Result Gates

- Strongest non-oracle baseline: `ensemble_disagreement_filter`.
- Combined-stress success: `0.648 +/- 0.009` proposed vs `0.542 +/- 0.009` baseline.
- Paired success gain: `0.106 +/- 0.008`, 7/7 seed wins.
- Harmful-transfer rate: `0.088` proposed vs `0.133` baseline.
- Tactile-event F1: `0.591` proposed vs `0.535` baseline.
- Damage rate: `0.068` proposed vs `0.086` baseline.
- Query cost: `0.236` proposed vs `0.267` baseline.
- Clean-transfer success: `0.701` proposed vs `0.651` strongest clean baseline.
- Ablation margin over best removed component: `0.026`.
- Max stress success: `0.590 +/- 0.006` proposed vs `0.439 +/- 0.007` ensemble disagreement and `0.711 +/- 0.006` oracle.

## Submission Decision

The local evidence clears the strong-revise gate: strongest-baseline margin, harmful-transfer reduction, clean-transfer retention, tactile-event F1 gain, damage/query-cost non-regression, paired-seed wins, ablation margin, expanded stress detail, and failure-case documentation all pass.

The paper is not ICLR-main ready. It still needs real tactile robot or independent high-fidelity validation, trained tactile checkpoint release, hardware/video artifacts, and deeper manual related-work synthesis before submission.

## Artifact Gate

- PDF: `C:/Users/wangz/Downloads/113.pdf`.
- SHA256: `1D96558152C75EC2AE38B7946F4F171FCFF4EB2DD813DFFA76CE985FC1ADF945`.
- Size: `410386` bytes.
- Desktop copy: absent.
- LaTeX scan: no substantive warnings; only the `rerunfilecheck` package line matched the warning scan after the final pass.
- BibTeX scan: `missing$ -- 0` and no warning or error lines.
