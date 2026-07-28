from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from boardroom_audit.charts import write_charts
from boardroom_audit.model import load_config, reconcile_base_case, run_simulation


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "assumptions" / "boardroom_reconstruction.json"


class ReconciliationTests(unittest.TestCase):
    def test_base_case_exposes_contingency_gap(self) -> None:
        result = reconcile_base_case(load_config(CONFIG))
        self.assertTrue(result["reported_profit_recalculates"])
        self.assertTrue(result["displayed_total_profit_recalculates"])
        self.assertAlmostEqual(float(result["gap_millions"]), 3.396964, places=6)
        self.assertAlmostEqual(
            float(result["fully_loaded_profit_millions"]),
            3.025232,
            places=6,
        )

    def test_historical_scenarios_reconcile(self) -> None:
        config = load_config(CONFIG)
        history = config["historical_scenarios"]
        revenue = np.asarray(history["revenue_millions"], dtype=float)
        expense = np.asarray(
            history["expense_used_for_reported_profit_millions"],
            dtype=float,
        )
        profit = np.asarray(history["reported_profit_millions"], dtype=float)
        np.testing.assert_allclose(revenue - expense, profit, atol=1e-6)


class SimulationTests(unittest.TestCase):
    def test_seed_is_reproducible(self) -> None:
        config = load_config(CONFIG)
        first = run_simulation(config)
        second = run_simulation(config)
        np.testing.assert_array_equal(
            first.profit_fully_loaded,
            second.profit_fully_loaded,
        )
        self.assertEqual(first.summary, second.summary)

    def test_probability_outputs_are_bounded(self) -> None:
        result = run_simulation(load_config(CONFIG))
        for value in result.summary["probability"].values():
            self.assertGreaterEqual(float(value), 0.0)
            self.assertLessEqual(float(value), 1.0)

    def test_contingency_never_increases_profit(self) -> None:
        result = run_simulation(load_config(CONFIG))
        self.assertTrue(
            np.all(
                result.profit_fully_loaded
                <= result.profit_reported_definition
            )
        )

    def test_regression_is_ranked_and_explanatory(self) -> None:
        result = run_simulation(load_config(CONFIG))
        importance = [
            float(row["absolute_importance"]) for row in result.regression
        ]
        self.assertEqual(importance, sorted(importance, reverse=True))
        self.assertGreater(float(result.summary["regression_r_squared"]), 0.85)

    def test_committed_summary_matches_seeded_run(self) -> None:
        committed_path = ROOT / "results" / "summary.json"
        with committed_path.open("r", encoding="utf-8") as handle:
            committed = json.load(handle)

        result = run_simulation(load_config(CONFIG))
        self.assertEqual(result.summary, committed)

    def test_charts_use_the_documented_svg_format(self) -> None:
        result = run_simulation(load_config(CONFIG))
        with tempfile.TemporaryDirectory() as output_dir:
            write_charts(result, output_dir)
            generated = sorted(path.name for path in Path(output_dir).iterdir())

        self.assertEqual(
            generated,
            ["driver_importance.svg", "profit_distribution.svg"],
        )


if __name__ == "__main__":
    unittest.main()
