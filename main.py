import argparse

# Create the command-line interface
parser = argparse.ArgumentParser(
    description="AI Lending Market Research Agent"
)

# Define required inputs
parser.add_argument("--country", required=True)
parser.add_argument("--product", required=True)

# Read the inputs
args = parser.parse_args()

# Display the results
print("=== Lending Market Research Agent ===")
print(f"Country: {args.country}")
print(f"Product: {args.product}")