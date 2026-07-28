from __future__ import annotations

import argparse
import json
from pathlib import Path

from .charts import write_charts
from .model import load_config, reconcile_base_case, run_simulation, write_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run the reproducible AI-boardroom forecast audit."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("assumptions/boardroom_reconstruction.json"),
    )
    parser.add_argument("--output", type=Path, default=Path("results"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    config = load_config(args.config)
    reconciliation = reconcile_base_case(config)
    result = run_simulation(config)
    write_results(result, args.output)
    write_charts(result, args.output)

    print("BASE-CASE RECONCILIATION")
    print(json.dumps(reconciliation, indent=2))
    print("\nMONTE CARLO SUMMARY")
    print(json.dumps(result.summary, indent=2))


if __name__ == "__main__":
    main()

