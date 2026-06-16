#!/usr/bin/env python3
"""Create the paper protocol diagram for the cross-session benchmark."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUT_DIR = Path("paper/figures")


def box(ax, xy, width, height, label, facecolor, edgecolor="#222222"):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.035,rounding_size=0.04",
        linewidth=1.4,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(patch)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, label, ha="center", va="center", fontsize=11)
    return patch


def arrow(ax, start, end, text=None, yoff=0.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=18,
            linewidth=1.6,
            color="#222222",
            shrinkA=4,
            shrinkB=4,
        )
    )
    if text:
        ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2 + yoff, text, ha="center", va="center", fontsize=9)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(14.5, 6.0))
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 6.0)
    ax.axis("off")

    ax.text(0.25, 5.55, "RoboMME-Interference protocol", fontsize=18, weight="bold", ha="left")
    ax.text(
        0.25,
        5.15,
        "A policy must act in the query session after seeing a relevant lesson mixed with unrelated prior sessions.",
        fontsize=11,
        ha="left",
        color="#333333",
    )

    box(ax, (0.35, 3.15), 2.15, 0.95, "Relevant lesson\nsession", "#c7e9c0", "#276419")
    box(ax, (3.05, 3.15), 2.15, 0.95, "Distractor\nsession", "#fdd0a2", "#a63603")
    box(ax, (5.55, 3.15), 2.15, 0.95, "More unrelated\nsessions", "#fdd0a2", "#a63603")
    box(ax, (8.35, 3.15), 2.15, 0.95, "Memory buffer\nfed to policy", "#dadaeb", "#54278f")
    box(ax, (11.25, 3.15), 2.15, 0.95, "Query rollout\nsuccess/fail", "#c6dbef", "#08519c")

    arrow(ax, (2.55, 3.62), (3.0, 3.62))
    arrow(ax, (5.25, 3.62), (5.5, 3.62))
    arrow(ax, (7.75, 3.62), (8.3, 3.62))
    arrow(ax, (10.55, 3.62), (11.2, 3.62))

    ax.text(1.42, 2.65, "The useful evidence", ha="center", fontsize=9, color="#276419")
    ax.text(4.12, 2.65, "Different-family filler", ha="center", fontsize=9, color="#a63603")
    ax.text(6.62, 2.65, "k controls interference", ha="center", fontsize=9, color="#a63603")
    ax.text(9.42, 2.65, "Same policy interface", ha="center", fontsize=9, color="#54278f")
    ax.text(12.32, 2.65, "Robot acts normally", ha="center", fontsize=9, color="#08519c")

    condition_y = 1.35
    ax.text(0.35, condition_y + 0.55, "History conditions:", fontsize=11, weight="bold", ha="left")
    conditions = [
        ("no-history", "empty\nexternal history"),
        ("k0", "lesson\nonly"),
        ("k1", "lesson + 1\ndistractor"),
        ("k3", "lesson + 3\ndistractors"),
        ("k7", "lesson + 7\ndistractors"),
    ]
    x = 0.35
    for name, desc in conditions:
        width = 2.55 if name == "no-history" else 2.35
        box(ax, (x, condition_y - 0.28), width, 0.78, f"{name}\n{desc}", "#f7f7f7", "#777777")
        x += width + 0.18

    ax.text(
        0.35,
        0.35,
        "Measurement: one rollout per episode/condition. Report success rates, Wilson confidence intervals, and paired episode-level bootstrap differences.",
        fontsize=10,
        ha="left",
        color="#333333",
    )

    for ext in ["png", "pdf"]:
        fig.savefig(OUT_DIR / f"protocol_diagram.{ext}", bbox_inches="tight", dpi=240)
    plt.close(fig)


if __name__ == "__main__":
    main()
