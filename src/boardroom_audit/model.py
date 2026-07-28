from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np


@dataclass(frozen=True)
class SimulationResult:
    variables: dict[str, np.ndarray]
    profit_reported_definition: np.ndarray
    profit_fully_loaded: np.ndarray
    summary: dict[str, Any]
    regression: list[dict[str, float | str]]


def load_config(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def reconcile_base_case(config: dict[str, Any]) -> dict[str, float | bool]:
    case = config["base_case_reconciliation"]
    revenue = float(case["revenue_millions"])
    expense_for_reported_profit = float(
        case["expense_used_for_reported_profit_millions"]
    )
    displayed_total_expense = float(case["displayed_total_expense_millions"])
    reported_profit = float(case["reported_profit_millions"])
    fully_loaded_profit = revenue - displayed_total_expense
    gap = displayed_total_expense - expense_for_reported_profit

    return {
        "reported_profit_recalculates": bool(
            np.isclose(revenue - expense_for_reported_profit, reported_profit)
        ),
        "displayed_total_profit_recalculates": bool(
            np.isclose(
                fully_loaded_profit,
                float(case["fully_loaded_profit_millions"]),
            )
        ),
        "revenue_millions": revenue,
        "expense_used_for_reported_profit_millions": expense_for_reported_profit,
        "displayed_total_expense_millions": displayed_total_expense,
        "reported_profit_millions": reported_profit,
        "fully_loaded_profit_millions": fully_loaded_profit,
        "gap_millions": gap,
    }


def _triangular(
    rng: np.random.Generator,
    spec: dict[str, Any],
    size: int,
) -> np.ndarray:
    return rng.triangular(
        float(spec["low"]),
        float(spec["mode"]),
        float(spec["high"]),
        size=size,
    )


def _shock_cost(
    rng: np.random.Generator,
    spec: dict[str, Any],
    size: int,
) -> np.ndarray:
    occurs = rng.random(size) < float(spec["probability"])
    magnitude = _triangular(rng, spec["cost_millions"], size)
    return occurs.astype(float) * magnitude


def _standardized_regression(
    variables: dict[str, np.ndarray],
    target: np.ndarray,
) -> tuple[list[dict[str, float | str]], float]:
    names = list(variables)
    matrix = np.column_stack([variables[name] for name in names])
    x_mean = matrix.mean(axis=0)
    x_std = matrix.std(axis=0)
    y_mean = target.mean()
    y_std = target.std()

    if np.any(x_std == 0) or y_std == 0:
        raise ValueError("Regression inputs must have non-zero variance.")

    x_scaled = (matrix - x_mean) / x_std
    y_scaled = (target - y_mean) / y_std
    design = np.column_stack([np.ones(len(target)), x_scaled])
    coefficients, *_ = np.linalg.lstsq(design, y_scaled, rcond=None)
    predicted = design @ coefficients

    residual_sum = float(np.sum((y_scaled - predicted) ** 2))
    total_sum = float(np.sum((y_scaled - y_scaled.mean()) ** 2))
    r_squared = 1.0 - residual_sum / total_sum

    rows = [
        {
            "variable": name,
            "standardized_coefficient": float(value),
            "absolute_importance": float(abs(value)),
        }
        for name, value in zip(names, coefficients[1:], strict=True)
    ]
    rows.sort(key=lambda row: float(row["absolute_importance"]), reverse=True)
    return rows, r_squared


def run_simulation(config: dict[str, Any]) -> SimulationResult:
    model = config["monte_carlo"]
    history = config["historical_scenarios"]
    iterations = int(model["iterations"])
    rng = np.random.default_rng(int(model["seed"]))

    sell_through = _triangular(rng, model["sell_through"], iterations)
    revenue_execution = _triangular(
        rng, model["revenue_execution_factor"], iterations
    )
    expense_overrun = _triangular(
        rng, model["expense_overrun_factor"], iterations
    )
    contingency_rate = _triangular(rng, model["contingency_rate"], iterations)
    sponsorship_delta = _triangular(
        rng, model["sponsorship_delta_millions"], iterations
    )
    headliner_cost_delta = _triangular(
        rng, model["headliner_cost_delta_millions"], iterations
    )
    weather_cost = _shock_cost(rng, model["weather_shock"], iterations)
    permit_delay_cost = _shock_cost(rng, model["permit_delay_shock"], iterations)

    historical_sell_through = np.asarray(history["sell_through"], dtype=float)
    historical_revenue = np.asarray(history["revenue_millions"], dtype=float)
    historical_operating_expense = np.asarray(
        history["expense_used_for_reported_profit_millions"], dtype=float
    )

    revenue_curve = np.interp(
        sell_through,
        historical_sell_through,
        historical_revenue,
    )
    operating_expense_curve = np.interp(
        sell_through,
        historical_sell_through,
        historical_operating_expense,
    )

    revenue = revenue_curve * revenue_execution + sponsorship_delta
    operating_expense = (
        operating_expense_curve * expense_overrun
        + headliner_cost_delta
        + weather_cost
        + permit_delay_cost
    )
    contingency_reserve = operating_expense_curve * contingency_rate

    profit_reported_definition = revenue - operating_expense
    profit_fully_loaded = profit_reported_definition - contingency_reserve

    variables = {
        "sell_through": sell_through,
        "revenue_execution_factor": revenue_execution,
        "expense_overrun_factor": expense_overrun,
        "contingency_rate": contingency_rate,
        "sponsorship_delta_millions": sponsorship_delta,
        "headliner_cost_delta_millions": headliner_cost_delta,
        "weather_cost_millions": weather_cost,
        "permit_delay_cost_millions": permit_delay_cost,
    }
    regression, r_squared = _standardized_regression(variables, profit_fully_loaded)

    quantiles = np.quantile(profit_fully_loaded, [0.05, 0.25, 0.50, 0.75, 0.95])
    summary = {
        "iterations": iterations,
        "seed": int(model["seed"]),
        "profit_fully_loaded_millions": {
            "mean": float(profit_fully_loaded.mean()),
            "p05": float(quantiles[0]),
            "p25": float(quantiles[1]),
            "median": float(quantiles[2]),
            "p75": float(quantiles[3]),
            "p95": float(quantiles[4]),
            "minimum": float(profit_fully_loaded.min()),
            "maximum": float(profit_fully_loaded.max()),
        },
        "probability": {
            "profit_above_zero": float(np.mean(profit_fully_loaded > 0)),
            "profit_at_least_3m": float(np.mean(profit_fully_loaded >= 3.0)),
            "profit_at_least_5m": float(np.mean(profit_fully_loaded >= 5.0)),
            "loss_of_at_least_2m": float(np.mean(profit_fully_loaded <= -2.0)),
        },
        "definition_gap_millions": {
            "mean": float(
                np.mean(profit_reported_definition - profit_fully_loaded)
            ),
            "median": float(
                np.median(profit_reported_definition - profit_fully_loaded)
            ),
        },
        "regression_r_squared": float(r_squared),
    }

    return SimulationResult(
        variables=variables,
        profit_reported_definition=profit_reported_definition,
        profit_fully_loaded=profit_fully_loaded,
        summary=summary,
        regression=regression,
    )


def write_results(
    result: SimulationResult,
    output_dir: str | Path,
) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    with (output_path / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(result.summary, handle, indent=2)
        handle.write("\n")

    with (output_path / "standardized_regression.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "variable",
                "standardized_coefficient",
                "absolute_importance",
            ],
        )
        writer.writeheader()
        writer.writerows(result.regression)

