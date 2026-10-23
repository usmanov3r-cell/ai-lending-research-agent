import json
from pathlib import Path

# Research files to process
input_files = [
    Path("data/input/pl_provident.json"),
    Path("data/input/pl_wonga.json")
]

normalized_products = []

expected_market = "PL"
expected_currency = "PLN"
expected_product_type = "unsecured_instalment_loan"

for input_file in input_files:

    with open(input_file, "r", encoding="utf-8") as file:
        raw_data = json.load(file)

    # Prevent accidentally combining different markets
    if raw_data["market"] != expected_market:
        raise ValueError(f"Wrong market in {input_file}")

    if raw_data["currency"] != expected_currency:
        raise ValueError(f"Wrong currency in {input_file}")

    if raw_data["data_origin"] != "public_lender_disclosure":
        raise ValueError(f"Unexpected data origin in {input_file}")

    for product in raw_data["products"]:

        if product["product_type"] != expected_product_type:
            raise ValueError(
                f"Wrong product type: {product['brand']}"
            )

        example = product["representative_example"]

        normalized_product = {
            "brand": product["brand"],
            "lender": product["lender"],
            "product_name": product["product_name"],
            "product_type": product["product_type"],
            "customer_type": product.get("customer_type"),

            # Pricing scenario
            "loan_amount": example["loan_amount"],
            "term_months": example["term_months"],
            "nominal_interest_rate_pct": example["nominal_interest_rate_pct"],
            "interest_rate_type": example["interest_rate_type"],
            "published_apr_pct": example["published_apr_pct"],
            "apr_status": example["apr_status"],

            # Fees
            "origination_fee_pln": example["origination_fee_pln"],
            "preparation_fee_pln": example["preparation_fee_pln"],

            "monthly_admin_fee_pln": example["monthly_admin_fee_pln"],
            "contract_fee_treatment": example["contract_fee_treatment"],
            "flexible_plan_fee_pln": example.get("flexible_plan_fee_pln"),
            # Published repayment information
            "total_interest_pln": example["total_interest_pln"],
            "total_credit_cost_pln": example["total_credit_cost_pln"],
            "total_repayable_pln": example["total_repayable_pln"],
            "regular_payment_pln": example["regular_payment_pln"],
            "regular_payment_count": example["regular_payment_count"],
            "final_payment_pln": example["final_payment_pln"],

            # Research evidence
            "promotions": product.get("promotions"),

            # Customer fee-payment options
            "fee_payment_options": product.get("fee_payment_options"),
            "commission_financing_example": example.get("commission_financing_example"),
            "payment_reconciliation_note": example.get("payment_reconciliation_note"),

            "pricing_basis": "published_representative_example",
            "source_url": product["source"]["url"],
            "source": product["source"]
        }

        normalized_products.append(normalized_product)

        print(f"Added: {product['brand']}")

# Combined dataset
normalized_data = {
    "market": expected_market,
    "product_type": expected_product_type,
    "currency": expected_currency,
    "data_origin": "public_lender_disclosure",
    "products": normalized_products
}

# Save
output_file = Path("data/normalized/pl_competitors.json")

output_file.parent.mkdir(parents=True, exist_ok=True)

with open(output_file, "w", encoding="utf-8") as file:
    json.dump(normalized_data, file, indent=2, ensure_ascii=False)

print(f"\nTotal products: {len(normalized_products)}")
print(f"Saved: {output_file}")