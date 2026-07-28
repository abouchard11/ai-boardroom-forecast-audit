from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from .model import SimulationResult


INK = "#172033"
BLUE = "#2364AA"
CYAN = "#00A6A6"
RED = "#D1495B"
CREAM = "#F7F4ED"


def _style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": CREAM,
            "axes.facecolor": CREAM,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "font.family": "DejaVu Sans",
        }
    )


def write_charts(result: SimulationResult, output_dir: str | Path) -> None:
    _style()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    profit = result.profit_fully_loaded
    median = float(np.median(profit))
    p05, p95 = np.quantile(profit, [0.05, 0.95])

    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.hist(profit, bins=90, color=BLUE, alpha=0.88, edgecolor="none")
    ax.axvline(0, color=RED, linewidth=2, label="Break-even")
    ax.axvline(median, color=CYAN, linewidth=2, label=f"Median: ${median:.1f}M")
    ax.axvspan(p05, p95, color=CYAN, alpha=0.10, label="5th–95th percentile")
    ax.set_title("Fully loaded profit distribution", loc="left", weight="bold")
    ax.set_xlabel("Profit (USD millions)")
    ax.set_ylabel("Simulation runs")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(output_path / "profit_distribution.svg")
    plt.close(fig)

    rows = result.regression
    names = [str(row["variable"]).replace("_", " ") for row in rows][::-1]
    values = [float(row["standardized_coefficient"]) for row in rows][::-1]
    colors = [CYAN if value >= 0 else RED for value in values]

    fig, ax = plt.subplots(figsize=(10, 5.8))
    ax.barh(names, values, color=colors)
    ax.axvline(0, color=INK, linewidth=1)
    ax.set_title(
        "Standardized drivers of fully loaded profit",
        loc="left",
        weight="bold",
    )
    ax.set_xlabel("Standardized regression coefficient")
    fig.tight_layout()
    fig.savefig(output_path / "driver_importance.svg")
    plt.close(fig)
