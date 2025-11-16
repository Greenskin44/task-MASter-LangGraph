#!/usr/bin/env python3
"""Script to run performance benchmarks and generate reports.

This script provides a convenient way to run benchmarks, save results,
and compare with previous baselines.

Usage:
    python scripts/run_benchmarks.py                    # Run all benchmarks
    python scripts/run_benchmarks.py --save baseline    # Save as baseline
    python scripts/run_benchmarks.py --compare baseline # Compare with baseline
    python scripts/run_benchmarks.py --histogram        # Generate histogram
"""

import argparse
import subprocess
import sys
from pathlib import Path


def run_benchmarks(
    save_name: str = None,
    compare_name: str = None,
    histogram: bool = False,
    min_rounds: int = 5,
    verbose: bool = False,
) -> int:
    """Run performance benchmarks with specified options.

    Args:
        save_name: Name to save benchmark results under
        compare_name: Name of baseline to compare against
        histogram: Whether to generate histogram
        min_rounds: Minimum number of benchmark rounds
        verbose: Whether to show verbose output

    Returns:
        Exit code from pytest
    """
    # Build pytest command
    cmd = [
        "pytest",
        "tests/test_benchmarks.py",
        "--benchmark-only",
        f"--benchmark-min-rounds={min_rounds}",
    ]

    if verbose:
        cmd.append("-v")

    if save_name:
        cmd.append(f"--benchmark-save={save_name}")
        print(f"Saving benchmark results as: {save_name}")

    if compare_name:
        cmd.append(f"--benchmark-compare={compare_name}")
        print(f"Comparing with baseline: {compare_name}")

    if histogram:
        cmd.append("--benchmark-histogram")
        print("Generating histogram...")

    # Run benchmarks
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 80)

    result = subprocess.run(cmd)

    return result.returncode


def main():
    """Main entry point for benchmark script."""
    parser = argparse.ArgumentParser(
        description="Run performance benchmarks for LangGraph graphs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run all benchmarks
  python scripts/run_benchmarks.py

  # Save results as baseline
  python scripts/run_benchmarks.py --save baseline

  # Compare with baseline
  python scripts/run_benchmarks.py --compare baseline

  # Generate histogram
  python scripts/run_benchmarks.py --histogram

  # Save and generate histogram
  python scripts/run_benchmarks.py --save baseline --histogram

  # Run with more rounds for accuracy
  python scripts/run_benchmarks.py --min-rounds 10

  # Compare with threshold (fail if >10% slower)
  pytest tests/test_benchmarks.py --benchmark-only --benchmark-compare=baseline --benchmark-compare-fail=mean:10%%

  # Run specific benchmark class
  pytest tests/test_benchmarks.py::TestStudioGraphBenchmarks --benchmark-only

  # Run single benchmark
  pytest tests/test_benchmarks.py::TestStudioGraphBenchmarks::test_parallelization_performance --benchmark-only
        """,
    )

    parser.add_argument(
        "--save",
        type=str,
        metavar="NAME",
        help="Save benchmark results with the specified name",
    )

    parser.add_argument(
        "--compare",
        type=str,
        metavar="NAME",
        help="Compare results with the specified baseline",
    )

    parser.add_argument(
        "--histogram",
        action="store_true",
        help="Generate histogram of benchmark results",
    )

    parser.add_argument(
        "--min-rounds",
        type=int,
        default=5,
        metavar="N",
        help="Minimum number of benchmark rounds (default: 5)",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show verbose output",
    )

    args = parser.parse_args()

    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("Warning: .env file not found. Make sure API keys are set.")
        print("Copy .env.example to .env and add your API keys.")
        print()

    # Run benchmarks
    exit_code = run_benchmarks(
        save_name=args.save,
        compare_name=args.compare,
        histogram=args.histogram,
        min_rounds=args.min_rounds,
        verbose=args.verbose,
    )

    if exit_code == 0:
        print()
        print("=" * 80)
        print("Benchmarks completed successfully!")
        print("=" * 80)

        if args.save:
            print(f"\nResults saved as: {args.save}")
            print(f"To compare future runs: python scripts/run_benchmarks.py --compare {args.save}")

        if args.histogram:
            print("\nHistogram generated in .benchmarks/ directory")

    else:
        print()
        print("=" * 80)
        print("Benchmarks failed or were skipped")
        print("=" * 80)
        print("\nCommon issues:")
        print("- Missing API keys in .env file")
        print("- Network connectivity issues")
        print("- Missing dependencies (run: pip install -r requirements.txt)")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
