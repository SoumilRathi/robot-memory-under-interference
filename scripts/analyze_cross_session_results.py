#!/usr/bin/env python3
"""Generate analysis tables and figures for RoboMME-Interference cross-session results."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


CONDITIONS = ["no-history", "k0", "k1", "k3", "k7"]
MEMORY_CONDITIONS = ["k0", "k1", "k3", "k7"]
VARIANT_ORDER = [
    "pi05_baseline",
    "perceptual-framesamp-modul",
    "perceptual-tokendrop-modul",
    "perceptual-framesamp-context",
    "perceptual-framesamp-expert",
    "perceptual-tokendrop-context",
    "perceptual-tokendrop-expert",
    "recurrent-ttt-expert",
    "recurrent-ttt-context",
]
HEADLINE_VARIANTS = [
    "perceptual-framesamp-modul",
    "perceptual-tokendrop-modul",
    "perceptual-framesamp-context",
    "perceptual-tokendrop-context",
    "recurrent-ttt-expert",
    "recurrent-ttt-context",
]
MEMORY_VARIANTS = [v for v in VARIANT_ORDER if v != "pi05_baseline"]
DISPLAY_NAMES = {
    "pi05_baseline": "pi0.5 baseline",
    "perceptual-framesamp-modul": "FrameSamp-Modul",
    "perceptual-tokendrop-modul": "TokenDrop-Modul",
    "perceptual-framesamp-context": "FrameSamp-Context",
    "perceptual-framesamp-expert": "FrameSamp-Expert",
    "perceptual-tokendrop-context": "TokenDrop-Context",
    "perceptual-tokendrop-expert": "TokenDrop-Expert",
    "recurrent-ttt-expert": "Recurrent-TTT-Expert",
    "recurrent-ttt-context": "Recurrent-TTT-Context",
}
PAPER_FAMILIES = [
    "MoveCube",
    "RouteStick",
    "VideoUnmask",
    "VideoUnmaskSwap",
    "VideoRepick",
    "VideoPlaceButton",
    "VideoPlaceOrder",
    "InsertPeg",
    "PatternLock",
]


def wilson(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return float("nan"), float("nan")
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, center - half), min(1.0, center + half)


def diff_ci(success_a: int, n_a: int, success_b: int, n_b: int, z: float = 1.96) -> tuple[float, float, float]:
    if n_a == 0 or n_b == 0:
        return float("nan"), float("nan"), float("nan")
    p_a = success_a / n_a
    p_b = success_b / n_b
    diff = p_a - p_b
    se = math.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b))
    return diff, diff - z * se, diff + z * se


def summarize(grouped: pd.core.groupby.DataFrameGroupBy) -> pd.DataFrame:
    rows = []
    for keys, g in grouped:
        if not isinstance(keys, tuple):
            keys = (keys,)
        successes = int(g["success_bool"].sum())
        n = int(len(g))
        lo, hi = wilson(successes, n)
        rows.append((*keys, successes, n, successes / n if n else np.nan, lo, hi))
    return pd.DataFrame(rows)


def pct(series: pd.Series | np.ndarray) -> np.ndarray:
    return np.asarray(series, dtype=float) * 100


def savefig(out_dir: Path, name: str) -> None:
    plt.savefig(out_dir / f"{name}.png", bbox_inches="tight", dpi=220)
    plt.close()


def plot_wilson_errorbar(ax: plt.Axes, x: np.ndarray, sub: pd.DataFrame, **kwargs) -> None:
    y = pct(sub["rate"])
    yerr = np.vstack([pct(sub["rate"] - sub["ci_low"]), pct(sub["ci_high"] - sub["rate"])])
    ax.errorbar(x, y, yerr=yerr, capsize=3, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()

    results_dir = Path(args.results_dir).resolve()
    analysis_dir = results_dir / "analysis"
    figures_dir = analysis_dir / "figures"
    tables_dir = analysis_dir / "tables"
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 10,
            "legend.fontsize": 8,
        }
    )

    df = pd.read_csv(results_dir / "canonical_rollouts.csv")
    df["success_bool"] = df["success"].astype(str).str.lower().eq("true")
    df["variant"] = pd.Categorical(df["variant"], VARIANT_ORDER, ordered=True)
    df["condition"] = pd.Categorical(df["condition"], CONDITIONS, ordered=True)

    manifest = json.loads((results_dir / "MANIFEST.json").read_text())

    vc = summarize(df.groupby(["variant", "condition"], observed=True))
    vc.columns = ["variant", "condition", "successes", "n", "rate", "ci_low", "ci_high"]
    vc.to_csv(tables_dir / "variant_condition_stats.csv", index=False)
    vc.to_csv(tables_dir / "main_success_rates.csv", index=False)

    fc = summarize(df.groupby(["family", "variant", "condition"], observed=True))
    fc.columns = ["family", "variant", "condition", "successes", "n", "rate", "ci_low", "ci_high"]
    fc.to_csv(tables_dir / "family_variant_condition_stats.csv", index=False)
    fc.to_csv(tables_dir / "family_success_rates.csv", index=False)

    diff = summarize(df.groupby(["variant", "difficulty"], observed=True))
    diff.columns = ["variant", "difficulty", "successes", "n", "rate", "ci_low", "ci_high"]
    diff.to_csv(tables_dir / "variant_difficulty_stats.csv", index=False)
    diff.to_csv(tables_dir / "difficulty_success_rates.csv", index=False)

    baseline = vc[vc["condition"].astype(str).eq("no-history")].set_index("variant")
    lift_rows = []
    for _, row in vc.iterrows():
        variant = str(row["variant"])
        condition = str(row["condition"])
        if condition == "no-history" or variant == "pi05_baseline":
            continue
        base = baseline.loc[variant]
        d, lo, hi = diff_ci(int(row["successes"]), int(row["n"]), int(base["successes"]), int(base["n"]))
        lift_rows.append(
            {
                "variant": variant,
                "condition": condition,
                "successes": int(row["successes"]),
                "n": int(row["n"]),
                "rate": row["rate"],
                "no_history_rate": base["rate"],
                "lift": d,
                "lift_ci_low": lo,
                "lift_ci_high": hi,
            }
        )
    lift = pd.DataFrame(lift_rows)
    lift.to_csv(tables_dir / "memory_lift_vs_no_history.csv", index=False)

    effect_rows = []
    wide = vc.pivot(index="variant", columns="condition", values="rate")
    for variant, row in wide.iterrows():
        effect = {"variant": str(variant)}
        for condition in CONDITIONS:
            effect[f"{condition}_rate"] = float(row[condition]) if condition in row and pd.notna(row[condition]) else np.nan
        if str(variant) != "pi05_baseline":
            for condition in MEMORY_CONDITIONS:
                effect[f"{condition}_minus_no_history"] = effect[f"{condition}_rate"] - effect["no-history_rate"]
            effect["k0_minus_k7"] = effect["k0_rate"] - effect["k7_rate"]
            effect["k0_minus_k3"] = effect["k0_rate"] - effect["k3_rate"]
        effect_rows.append(effect)
    effects = pd.DataFrame(effect_rows)
    effects.to_csv(tables_dir / "effect_sizes.csv", index=False)

    # Figure 1: plain overall success rates. This is the paper-facing headline.
    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    x = np.arange(len(CONDITIONS))
    for variant in MEMORY_VARIANTS:
        sub = vc[vc["variant"].astype(str).eq(variant)].copy()
        sub = sub.set_index(sub["condition"].astype(str)).loc[CONDITIONS]
        plot_wilson_errorbar(
            ax,
            x,
            sub,
            marker="o",
            linewidth=1.7,
            label=DISPLAY_NAMES.get(variant, variant),
        )
    pi = vc[(vc["variant"].astype(str).eq("pi05_baseline")) & (vc["condition"].astype(str).eq("no-history"))].iloc[0]
    ax.axhline(pi["rate"] * 100, color="black", linestyle="--", linewidth=1.3, label="pi0.5 baseline")
    ax.fill_between(
        [-0.25, len(CONDITIONS) - 0.75],
        [pi["ci_low"] * 100, pi["ci_low"] * 100],
        [pi["ci_high"] * 100, pi["ci_high"] * 100],
        color="black",
        alpha=0.08,
        linewidth=0,
    )
    ax.set_xticks(x, CONDITIONS)
    ax.set_ylabel("Success rate (%)")
    ax.set_xlabel("History condition")
    ax.set_title("Cross-session memory benchmark: success by session distance")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(ncol=2, loc="upper right")
    savefig(figures_dir, "overall_plain_success_by_condition")

    # Figure 2: per-family small multiples, with all memory variants shown as plain accuracy.
    fig, axes = plt.subplots(3, 3, figsize=(16, 11), sharex=True, sharey=True)
    family_stats = fc.copy()
    family_stats["family"] = family_stats["family"].astype(str)
    family_stats["variant"] = family_stats["variant"].astype(str)
    family_stats["condition"] = family_stats["condition"].astype(str)
    for ax, family in zip(axes.flat, PAPER_FAMILIES):
        pi_family = family_stats[
            family_stats["family"].eq(family)
            & family_stats["variant"].eq("pi05_baseline")
            & family_stats["condition"].eq("no-history")
        ]
        if not pi_family.empty:
            ax.axhline(float(pi_family.iloc[0]["rate"]) * 100, color="black", linestyle="--", linewidth=1.0, alpha=0.8)
        for variant in MEMORY_VARIANTS:
            sub = family_stats[family_stats["family"].eq(family) & family_stats["variant"].eq(variant)]
            sub = sub.set_index("condition").reindex(CONDITIONS)
            ax.plot(x, pct(sub["rate"]), marker="o", linewidth=1.2, markersize=3, label=DISPLAY_NAMES.get(variant, variant))
        ax.set_title(family)
        ax.grid(axis="y", alpha=0.2)
        ax.set_xticks(x, CONDITIONS, rotation=35, ha="right")
    axes[1, 0].set_ylabel("Success rate (%)")
    axes[2, 1].set_xlabel("History condition")
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, ncol=4, loc="lower center", bbox_to_anchor=(0.5, -0.015))
    fig.suptitle("Per-family success curves across memory systems", y=0.995)
    savefig(figures_dir, "per_family_plain_success_small_multiples")

    # Figure 3: family x condition heatmap for strongest variant, shown as plain success.
    best_variant = "perceptual-framesamp-modul"
    heat = fc[fc["variant"].astype(str).eq(best_variant)].copy()
    heat["condition"] = heat["condition"].astype(str)
    pivot = heat.pivot(index="family", columns="condition", values="rate").reindex(PAPER_FAMILIES)[CONDITIONS] * 100
    plt.figure(figsize=(8.2, 6.0))
    im = plt.imshow(pivot.to_numpy(), aspect="auto", cmap="viridis", vmin=0, vmax=max(50, float(np.nanmax(pivot.to_numpy()))))
    plt.colorbar(im, label="Success rate (%)")
    plt.yticks(np.arange(len(pivot.index)), pivot.index)
    plt.xticks(np.arange(len(CONDITIONS)), CONDITIONS)
    plt.title(f"Per-family success heatmap: {DISPLAY_NAMES[best_variant]}")
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            val = pivot.iloc[i, j]
            plt.text(j, i, f"{val:.0f}", ha="center", va="center", color="white" if val < 28 else "black", fontsize=8)
    savefig(figures_dir, "framesamp_modul_family_heatmap")

    # Figure 4: success by difficulty. This uses plain success, not lift.
    plt.figure(figsize=(10.5, 5.8))
    plot_variants = [
        "pi05_baseline",
        "perceptual-framesamp-modul",
        "perceptual-tokendrop-modul",
        "recurrent-ttt-expert",
        "recurrent-ttt-context",
    ]
    difficulties = ["easy", "medium", "hard"]
    width = 0.16
    centers = np.arange(len(difficulties))
    for idx, variant in enumerate(plot_variants):
        sub = diff[diff["variant"].astype(str).eq(variant)].set_index("difficulty").loc[difficulties]
        xpos = centers + (idx - (len(plot_variants) - 1) / 2) * width
        y = sub["rate"].to_numpy() * 100
        yerr = np.vstack([(sub["rate"] - sub["ci_low"]).to_numpy(), (sub["ci_high"] - sub["rate"]).to_numpy()]) * 100
        plt.bar(xpos, y, width=width, yerr=yerr, capsize=2, label=DISPLAY_NAMES.get(variant, variant))
    plt.xticks(centers, difficulties)
    plt.ylabel("Success rate (%)")
    plt.title("Success by task difficulty")
    plt.grid(axis="y", alpha=0.25)
    plt.legend(fontsize=8)
    savefig(figures_dir, "difficulty_plain_success")

    # Supporting figures: lift over no-history is useful, but not the main claim.
    plt.figure(figsize=(9.5, 5.8))
    x_memory = np.arange(len(MEMORY_CONDITIONS))
    for variant in HEADLINE_VARIANTS:
        sub = lift[(lift["variant"] == variant) & (lift["condition"].isin(MEMORY_CONDITIONS))]
        sub = sub.set_index("condition").loc[MEMORY_CONDITIONS]
        y = sub["lift"].to_numpy() * 100
        yerr = np.vstack([(sub["lift"] - sub["lift_ci_low"]).to_numpy(), (sub["lift_ci_high"] - sub["lift"]).to_numpy()]) * 100
        plt.errorbar(x_memory, y, yerr=yerr, marker="o", linewidth=2, capsize=3, label=DISPLAY_NAMES.get(variant, variant))
    plt.axhline(0, color="black", linewidth=1)
    plt.xticks(x_memory, MEMORY_CONDITIONS)
    plt.ylabel("Lift over no-history (percentage points)")
    plt.xlabel("Memory condition")
    plt.title("Supporting analysis: memory lift over each variant's no-history baseline")
    plt.grid(axis="y", alpha=0.25)
    plt.legend(fontsize=8, ncol=2)
    savefig(figures_dir, "memory_lift_vs_no_history")

    # Supporting compact all-variant k0 lift ranking.
    k0 = lift[lift["condition"].eq("k0")].copy()
    k0["variant"] = k0["variant"].astype(str)
    k0 = k0.sort_values("lift", ascending=True)
    plt.figure(figsize=(8.5, 5.8))
    y = np.arange(len(k0))
    vals = k0["lift"].to_numpy() * 100
    err = np.vstack([(k0["lift"] - k0["lift_ci_low"]).to_numpy(), (k0["lift_ci_high"] - k0["lift"]).to_numpy()]) * 100
    plt.barh(y, vals, xerr=err, capsize=3)
    plt.yticks(y, [DISPLAY_NAMES.get(v, v) for v in k0["variant"]])
    plt.axvline(0, color="black", linewidth=1)
    plt.xlabel("k0 lift over no-history (percentage points)")
    plt.title("Supporting analysis: nearest prior-session memory benefit")
    plt.grid(axis="x", alpha=0.25)
    savefig(figures_dir, "k0_lift_ranking")

    summary = {
        "results_dir": args.results_dir,
        "expected_cells": manifest["expected_cells"],
        "complete_cells": manifest["complete_cells"],
        "row_coverage": f"{manifest['row_coverage']}/{manifest['expected_rows']}",
        "generated_tables": sorted(p.name for p in tables_dir.glob("*.csv")),
        "generated_figures": sorted(p.name for p in figures_dir.glob("*.png")),
    }
    (analysis_dir / "analysis_manifest.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
