# RoboMME-Interference Results

This directory is the single source of truth for the RoboMME-Interference cross-session memory evaluation results.

## Files

- `canonical_rollouts.csv`: one deduplicated rollout row per `(variant, family, condition, episode)`.
- `coverage.csv`: cell-level coverage and missing episodes.
- `grid_summary.csv`: success rate by variant and memory condition.
- `by_family_condition.csv`: success rate by family, variant, and condition.
- `by_difficulty.csv`: success rate by variant and difficulty.
- `MANIFEST.json`: source files and build metadata.

## Current Coverage

- Complete cells: 369/369
- Partial cells: 0
- Missing cells: 0
- Row coverage: 18450/18450

The live rollout may still be running. Rebuild this directory after the live run finishes for final paper numbers.
