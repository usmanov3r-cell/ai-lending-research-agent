import argparse
import subprocess
import sys
from pathlib import Path


# Command-line parameters
parser = argparse.ArgumentParser(
    description="AI Lending Product Intelligence Pipeline"
)

parser.add_argument(
    "--data",
    choices=["synthetic", "real"],
    default="real",
    help="Select the research dataset"
)

parser.add_argument(
    "--with-ai",
    action="store_true",
    help="Generate an AI business brief (paid API call)"
)

args = parser.parse_args()


# Project location
project_dir = Path(__file__).resolve().parent


def run_step(name, command):
    """Execute a pipeline step and stop if it fails."""

    print(f"\n=== {name} ===", flush=True)

    subprocess.run(
        [sys.executable, *command],
        cwd=project_dir,
        check=True
    )


print("\nAI LENDING PRODUCT INTELLIGENCE AGENT")
print(f"Dataset: {args.data}")
print(f"AI enabled: {args.with_ai}")


# STEP 1: Normalize real competitor data
if args.data == "real":

    run_step(
        "DATA NORMALIZATION",
        ["normalize.py"]
    )

# STEP 1.5: Run automated financial tests
if args.data == "real":

    run_step(
        "AUTOMATED FINANCIAL TESTS",
        [
            "-m", "unittest",
            "discover",
            "-s", "tests",
            "-v"
        ]
    )

# STEP 2: Generate research report
run_step(
    "LENDING RESEARCH AND VALIDATION",
    [
        "main.py",
        "--country", "PL",
        "--product", "unsecured_instalment_loan",
        "--data", args.data
    ]
)


# STEP 3: Generate or validate AI input
ai_command = [
    "ai_analysis.py",
    "--data", args.data
]

if not args.with_ai:
    ai_command.append("--dry-run")

run_step(
    "AI BUSINESS ANALYSIS",
    ai_command
)


print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")

if args.with_ai:
    print("AI business brief generated.")
else:
    print("AI dry run completed. No API call made.")