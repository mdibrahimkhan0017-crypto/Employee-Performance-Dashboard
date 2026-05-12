"""
run_all.py
----------
Master pipeline script that orchestrates the entire Employee Performance
Dashboard workflow:
  1. Generate synthetic HR data
  2. Execute SQL window-function queries
  3. Produce visualisation charts
"""

import sys
import subprocess


def _run_step(step_num: int, total: int, label: str, script: str):
    """Run a Python script as a subprocess and report status."""
    print(f"\n[STEP {step_num}/{total}] {label}...")
    try:
        subprocess.run(
            [sys.executable, script],
            check=True,
        )
        print(f"[STEP {step_num}/{total}] {label}... DONE ✅")
    except subprocess.CalledProcessError as exc:
        print(f"[STEP {step_num}/{total}] {label}... FAILED ❌")
        print(f"Error: {exc}")
        sys.exit(1)


def main():
    print("=" * 50)
    print("=== Employee Performance Dashboard ===")
    print("=" * 50)

    _run_step(1, 3, "Generating HR Data",        "generate_hr_data.py")
    _run_step(2, 3, "Running SQL Queries",        "sql_runner.py")
    _run_step(3, 3, "Generating Visualizations",  "hr_visualizations.py")

    print("\n" + "=" * 50)
    print("Pipeline Complete. Check the outputs/ folder for results.")
    print("=" * 50)


if __name__ == "__main__":
    main()
