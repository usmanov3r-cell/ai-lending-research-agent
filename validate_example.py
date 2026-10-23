import argparse
import json
from decimal import Decimal
from pathlib import Path

# Choose which lender file to validate
parser = argparse.ArgumentParser()

parser.add_argument(
    "--file",
    default="data/input/pl_provident.json",
    help="Path to the lender research JSON"
)

args = parser.parse_args()

# Load lender research
with open(Path(args.file), "r", encoding="utf-8") as file:
    data = json.load(file)

product = data["products"][0]
example = product["representative_example"]


# Convert financial values into Decimal
# Missing information remains None
def money(field):
    value = example.get(field)

    if value is None:
        return None

    return Decimal(str(value))


print(f"\n=== FINANCIAL VALIDATION: {product['brand']} ===")

# CHECK 1: Reconcile disclosed borrowing costs

cost_fields = [
    "total_interest_pln",
    "origination_fee_pln",
    "preparation_fee_pln",
    "flexible_plan_fee_pln"
]

known_costs = [
    money(field)
    for field in cost_fields
    if money(field) is not None
]

calculated_cost = sum(known_costs, Decimal("0"))
published_cost = money("total_credit_cost_pln")

cost_difference = published_cost - calculated_cost

if cost_difference == 0:
    print("Borrowing costs: MATCH (known components)")
elif cost_difference > 0:
    print(f"Borrowing costs: REVIEW - unexplained PLN {cost_difference}")
else:
    print("Borrowing costs: FAIL - components exceed reported total")


# CHECK 2: Total amount repayable

calculated_repayable = (
    money("loan_amount")
    + published_cost
)

published_repayable = money("total_repayable_pln")

if calculated_repayable == published_repayable:
    print("Total repayable: PASS")
else:
    print("Total repayable: FAIL")


# CHECK 3: Instalment reconciliation

calculated_payments = (
    money("regular_payment_pln") * example["regular_payment_count"]
    + money("final_payment_pln")
)

payment_difference = published_repayable - calculated_payments

if payment_difference == 0:
    print("Instalment reconciliation: PASS")

else:
    print("Instalment reconciliation: REVIEW")
    print(f"Difference: PLN {payment_difference}")

    commission = money("origination_fee_pln")

    if commission is not None and payment_difference == commission:
        print("Difference equals disclosed commission.")
        print("Commission settlement requires verification.")


# Display remaining limitations

print(f"\nPublished APR: {example['published_apr_pct']}%")
print(f"Fee treatment: {example['contract_fee_treatment']}")

if money("monthly_admin_fee_pln") is None:
    print("Monthly administration fee: unknown")

print("Note: Missing fees are not assumed to be zero.")
print("Note: APR has not been independently recalculated.")