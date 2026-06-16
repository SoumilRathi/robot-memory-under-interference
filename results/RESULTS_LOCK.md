# Results Lock

This directory is the canonical local snapshot for the RoboMME-Interference cross-session
memory evaluation.

## Locked Snapshot

- Local directory: `/Users/soumil/Documents/robotics/artifacts/robomme_cross_session_results`
- Source tarball: `/Users/soumil/Documents/robotics/artifacts/robomme_cross_session_results_20260615T205323Z.tar.gz`
- Provenance archive: `/Users/soumil/Documents/robotics/artifacts/robomme_cross_session_provenance_light_20260615T205323Z.tar.gz`
- Locked rows: `18,450 / 18,450`
- Locked cells: `369 / 369`
- Task families: `9`
- Variants: `9`
- Conditions: `no-history`, `k0`, `k1`, `k3`, `k7`

## Authoritative Files

- `canonical_rollouts.csv`: per-rollout source of truth.
- `coverage.csv`: cell-level coverage; all expected cells are complete.
- `grid_summary.csv`: variant-by-condition success table.
- `by_family_condition.csv`: family-level table.
- `by_difficulty.csv`: difficulty-level table.
- `analysis/tables/*.csv`: generated paper-facing tables with confidence intervals.
- `analysis/figures/*.png` and `analysis/figures/*.pdf`: generated first-pass figures.

## Validation

The final result set has full expected coverage:

```text
expected_cells: 369
complete_cells: 369
partial_cells: 0
missing_cells: 0
row_coverage: 18450 / 18450
```

Checksums for the canonical result files are stored in `SHA256SUMS`.

## Notes

Old wave directories and remote scratch folders are not authoritative. If a
number differs from this directory, this directory wins unless a new results
lock is intentionally created.
