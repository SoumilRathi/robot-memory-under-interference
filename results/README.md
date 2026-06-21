# RoboMME-Interference Results

The canonical results for the RoboMME-Interference cross-session memory benchmark.

## Files

- `canonical_rollouts.csv`: one deduplicated rollout per `(variant, family, condition, episode)` — the source of truth.
- `coverage.csv`: cell-level coverage and any missing episodes.
- `grid_summary.csv`: success rate by variant and condition.
- `by_family_condition.csv`: success rate by family, variant, and condition.
- `by_difficulty.csv`: success rate by variant and difficulty.
- `MANIFEST.json`: grid definition and coverage counts.
- `SHA256SUMS`: checksums for the files above.
- `analysis/`: generated tables and figures (rebuild with [`scripts/analyze_cross_session_results.py`](../scripts/analyze_cross_session_results.py)).

## Coverage

369 / 369 cells complete; 18,450 / 18,450 rollouts.

## Integrity

```bash
cd results && shasum -a 256 -c SHA256SUMS
```
