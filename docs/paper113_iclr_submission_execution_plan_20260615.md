# Paper 113 ICLR Submission Execution Plan - 2026-06-15

Paper: `tactile_pretraining_negative_transfer`

Target venue posture: ICLR main target, evidence-bound.

Current terminal posture before continuation: `STRONG_REVISE`, not ICLR-main ready.

## Goal

Re-audit Paper 113 as if preparing a real ICLR-main submission, while keeping the decision honest. The paper may remain `STRONG_REVISE` only if the rerun reproduces a decisive local advantage for an action-critical tactile negative-transfer guard over the strongest non-oracle tactile-transfer baseline, without increasing harmful transfer, damage, or query cost. It must not be marked ICLR-main ready without real robot or independent high-fidelity tactile validation.

## Execution Steps

1. Compile and rerun the experiment with low-RAM thread caps:

```powershell
$env:OMP_NUM_THREADS='1'
$env:OPENBLAS_NUM_THREADS='1'
$env:MKL_NUM_THREADS='1'
python -m py_compile src\run_experiment.py
python src\run_experiment.py *> C:\Users\wangz\robotics_massive_pool_paper_factory\logs\113_tactile_pretraining_negative_transfer_continuation_rerun_20260615.log
```

2. Verify CSV integrity:
- `metrics.csv`: 45 rows.
- `per_task_regime_metrics.csv`: 1,575 rows.
- `seed_task_regime_metrics.csv`: 11,025 rows.
- `seed_split_metrics.csv`: 315 rows.
- `pairwise_stats.csv`: 8 rows.
- `ablation_metrics.csv`: 7 rows.
- `ablation_seed_metrics.csv`: 49 rows.
- `ablation_task_regime_seed_metrics.csv`: 1,715 rows.
- `stress_sweep.csv`: 24 aggregate rows.
- `stress_sweep_seed_metrics.csv`: target 5,880 task/regime/seed rows after recoverable coverage patch.
- `failure_cases.csv`: target 8 documented failure boundaries after recoverable coverage patch.

3. Verify result gates:
- Strongest non-oracle baseline remains `ensemble_disagreement_filter`.
- Proposed method clears at least `+0.030` combined-stress success over the strongest non-oracle baseline.
- Harmful-transfer rate decreases by at least `0.020`.
- Clean-transfer performance does not materially drop versus the strongest clean-transfer baseline.
- Tactile-event F1 improves by at least `0.030`.
- Damage and query cost do not regress.
- Paired seed wins over the strongest non-oracle baseline are at least 5/7.
- Best removed-component ablation remains at least `0.020` success below the full method.

4. Harden documentation and paper:
- Update README, child status, decision docs, final audit, version log, checklists, hostile reviewer response, and manuscript text to v4.1.
- Make clear the evidence is local and generated.
- Preserve the negative-transfer claim narrowly: action-critical tactile transfer selection can beat broad pretraining, finetuning, domain-adversarial transfer, uncertainty gating, and ensemble-disagreement filtering on the local benchmark.

5. Build and verify artifact:
- Build `paper/main.pdf` with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
- Copy only to `C:/Users/wangz/Downloads/113.pdf`.
- Verify SHA256, file size, LaTeX/BibTeX warnings, public GitHub repo, and no `C:/Users/wangz/Desktop/113.pdf`.

6. Update root ledgers:
- `GLOBAL_POOL_STATUS.md`
- `BATCH_STATUS.md`
- `SUBMISSION_STATUS.md`
- `MASTER_REPORT.md`
- `MASTER_SUBMISSION_REPORT.md`

## Terminal Decision Rule

`STRONG_REVISE`: local tactile negative-transfer evidence remains strong, stress/failure coverage is expanded, reproducibility and artifact gates pass, but real tactile robot or independent high-fidelity evidence is missing.

`KILL_ARCHIVE`: rerun fails to reproduce the strongest-baseline, harmful-transfer, clean-transfer, tactile-event, safety/cost, paired-seed, or ablation gates.

No `ICLR main ready` label is allowed without real robot or independent high-fidelity tactile validation, plus a deeper manual related-work review.
