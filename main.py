import argparse
import json
from pathlib import Path

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

# Locate our lending data file
data_file = Path("data/input/pl_personal_loans.json")

# Read the JSON file
with open(data_file, "r", encoding="utf-8") as file:
    data = json.load(file)

# Check that the selected market and product match our data
if args.country.upper() != data["market"] or args.product != data["product_type"]:
    parser.error("This dataset only supports PL / unsecured_instalment_loan")

# Display competitor information
print("\nData origin:", data["data_origin"])
print("\nCompetitors:")

for product in data["products"]:
    print(f"\nBrand: {product['brand']}")
    print(f"Legal lender: {product['lender']}")
    print(f"Nominal interest: {product['nominal_interest_rate_pct']}%")
    print(f"Origination fee: {product['origination_fee_pln']} {data['currency']}")
    # Display additional pricing information
    print(f"Interest rate type: {product['interest_rate_type']}")
    print(f"Contract fee treatment: {product['contract_fee_treatment']}")

    apr = product["published_apr_pct"]
    admin_fee = product["monthly_admin_fee_pln"]

    print(f"Published APR: {apr if apr is not None else 'unknown'}")
    print(f"Monthly admin fee: {admin_fee if admin_fee is not None else 'unknown'}")

    # Display promotional campaigns
    for promo in product["promotions"]:

        if promo["type"] == "interest_waiver":
            print(
                f"Promotion: {promo['promotional_interest_rate_pct']}% interest "
                f"for instalments {promo['start_installment']}-{promo['end_installment']}"
            )

        elif promo["type"] == "contract_fee_waiver":
            print(
                f"Promotion: contract fee reduced from "
                f"{promo['standard_fee_pln']} to "
                f"{promo['promotional_fee_pln']} PLN"
            )

        print(f"Eligibility: {promo['eligibility']}")
# Compare standard pricing between two products
products = data["products"]

comparison_result = {
    "status": "not_comparable",
    "reason": "Two products with matching amounts and terms are required"
}

if len(products) == 2:
    a = products[0]
    b = products[1]

    print("\n=== COMPETITOR PRICING COMPARISON ===")

    # Check whether the loan scenarios are comparable
    if (
        a["loan_amount"] == b["loan_amount"]
        and a["term_months"] == b["term_months"]
    ):

        rate_difference = (
            a["nominal_interest_rate_pct"]
            - b["nominal_interest_rate_pct"]
        )

        fee_difference = (
            b["origination_fee_pln"]
            - a["origination_fee_pln"]
        )
        comparison_result = {
            "status": "partial_comparison",
            "comparison_basis": "standard_pricing_only",
            "brand_a": a["brand"],
            "brand_b": b["brand"],
            "loan_amount_pln": a["loan_amount"],
            "term_months": a["term_months"],
            "nominal_rate_difference_pp": round(rate_difference, 2),
            "contract_fee_difference_pln": round(fee_difference, 2),
            "lower_rate_higher_fee_signal": (
                rate_difference > 0 and fee_difference > 0
            ),
            "limitations": [
                "Promotional campaigns excluded",
                "Total borrowing cost not calculated",
                "APR and administration fees are unknown"
            ]
        }

        print(f"Nominal rate difference (A minus B): {rate_difference:.2f} percentage points")
        print(f"Contract fee difference (B minus A): {fee_difference:.2f} PLN")

        if rate_difference > 0 and fee_difference > 0:
            print(
                "SIGNAL: Brand B offers a lower nominal rate "
                "but charges a higher standard contract fee."
            )

        print(
            "NOTE: Standard pricing only. Promotions are excluded. "
            "Total borrowing cost cannot yet be compared reliably."
        )

    else:
        print("Products have different amounts or terms.")
        print("Direct pricing comparison is not appropriate.")
# Data quality and evidence checks

print("\n=== DATA QUALITY REPORT ===")

quality_results = []

for product in data["products"]:

    issues = []

    # Check whether the information is real market evidence
    if data["data_origin"] == "synthetic":
        issues.append("Synthetic data - not verified market research")

    # Check published APR
    if product.get("published_apr_pct") is None:
        issues.append("Published APR: missing")

    # Check monthly administration fee
    if product.get("monthly_admin_fee_pln") is None:
        issues.append("Monthly administration fee: unknown")

    # Check evidence source
    if not product.get("source_url"):
        issues.append("Source: missing")

    # Check promotional validity
    for promo in product.get("promotions", []):

        if (
            promo.get("valid_from") is None
            or promo.get("valid_until") is None
        ):
            issues.append(
                f"Promotion ({promo['type']}): validity dates unknown"
            )

    # Display findings
    print(f"\n{product['brand']}")

    for issue in issues:
        print(f"- {issue}")

    print(f"Total data quality flags: {len(issues)}")
    quality_results.append({
        "brand": product["brand"],
        "issues": issues,
        "issue_count": len(issues)
    })
# Build structured research report
report = {
    "market": data["market"],
    "product_type": data["product_type"],
    "data_origin": data["data_origin"],
    "products": data["products"],
    "comparison": comparison_result,
    "data_quality": quality_results
}

# Define output location
output_file = Path("data/output/research_report.json")

# Create output directory if necessary
output_file.parent.mkdir(parents=True, exist_ok=True)

# Save report as JSON
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=2, ensure_ascii=False)

print(f"\nResearch report saved: {output_file}")