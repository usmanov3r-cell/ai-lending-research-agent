import json
from decimal import Decimal
from pathlib import Path


def amount(value):
    """Convert a financial value to Decimal."""
    if value is None:
        return None
    return Decimal(str(value))


def validate_product(product):
    """Validate a normalized lending product."""

    # Fields required for basic reconciliation
    required = [
        "loan_amount",
        "total_credit_cost_pln",
        "total_repayable_pln",
        "regular_payment_pln",
        "regular_payment_count",
        "final_payment_pln"
    ]

    missing = [
        field for field in required
        if product.get(field) is None
    ]

    if missing:
        return {
            "status": "INCOMPLETE",
            "missing_fields": missing
        }

    # 1. Reconcile disclosed borrowing costs
    cost_fields = [
        "total_interest_pln",
        "origination_fee_pln",
        "preparation_fee_pln",
        "flexible_plan_fee_pln"
    ]

    known_costs = sum(
        (
            amount(product[field])
            for field in cost_fields
            if product.get(field) is not None
        ),
        Decimal("0")
    )

    unknown_costs = [
        field for field in cost_fields
        if product.get(field) is None
    ]

    cost_difference = (
        amount(product["total_credit_cost_pln"])
        - known_costs
    )

    # 2. Reconcile total repayable
    expected_repayable = (
        amount(product["loan_amount"])
        + amount(product["total_credit_cost_pln"])
    )

    repayable_difference = (
        amount(product["total_repayable_pln"])
        - expected_repayable
    )

    # 3. Reconcile published instalments
    instalment_total = (
        amount(product["regular_payment_pln"])
        * product["regular_payment_count"]
        + amount(product["final_payment_pln"])
    )

    payment_difference = (
        amount(product["total_repayable_pln"])
        - instalment_total
    )

    # 4. Check whether payment difference matches commission
    commission = amount(product.get("origination_fee_pln"))

    equals_commission = (
        commission is not None
        and payment_difference == commission
        and payment_difference != 0
    )
    # 5. Validate customer fee-payment options
    options = product.get("fee_payment_options") or []
    commission_loan = product.get("commission_financing_example") or {}

    option_checks = []
    upfront_explains_difference = False

    for option in options:

        option_id = option.get("option_id")

        reported_outflow = amount(
            option.get("total_customer_outflow_pln")
        )

        reported_extra_cost = amount(
            option.get("additional_financing_cost_pln")
        )

        expected_outflow = None
        expected_extra_cost = None
        structure_valid = True

        # Option A: Customer pays commission upfront
        if option_id == "upfront_payment":

            upfront = amount(option.get("upfront_payment_pln"))

            if upfront is not None:
                expected_outflow = instalment_total + upfront
                expected_extra_cost = Decimal("0")

                upfront_explains_difference = (
                    equals_commission
                    and upfront == payment_difference
                    and option.get("availability_status") == "lender_disclosed"
                )

        # Option B: Customer takes a separate commission loan
        elif option_id == "separate_commission_loan":

            count = commission_loan.get("regular_payment_count")

            regular = amount(
                commission_loan.get("regular_payment_pln")
            )

            final = amount(
                commission_loan.get("final_payment_pln")
            )

            principal = amount(
                commission_loan.get("principal_pln")
            )

            if None not in (count, regular, final, principal):

                loan_payments = regular * count + final

                expected_outflow = (
                    instalment_total + loan_payments
                )

                expected_extra_cost = (
                    loan_payments - principal
                )

                structure_valid = (
                    principal == commission
                    and loan_payments == amount(
                        commission_loan.get("total_repayable_pln")
                    )
                    and expected_extra_cost == amount(
                        commission_loan.get("total_interest_pln")
                    )
                )

        # Compare our calculations with recorded figures
        if expected_outflow is None or reported_outflow is None:
            status = "INCOMPLETE"

        elif (
            expected_outflow == reported_outflow
            and expected_extra_cost == reported_extra_cost
            and structure_valid
        ):
            status = "PASS"

        else:
            status = "REVIEW"

        option_checks.append({
            "option_id": option_id,
            "status": status,
            "calculated_outflow_pln": (
                str(expected_outflow)
                if expected_outflow is not None else None
            )
        })

    # Distinguish explained differences from unresolved ones
    if payment_difference == 0:
        instalment_status = "PASS"

    elif upfront_explains_difference:
        instalment_status = "EXPLAINED_DIFFERENCE"

    else:
        instalment_status = "REVIEW"

    return {
        "status": "CHECKED",
        "cost_components": {
            "status": "MATCH_KNOWN" if cost_difference == 0 else "REVIEW",
            "difference_pln": str(cost_difference),
            "unknown_components": unknown_costs
        },
        "total_repayable": {
            "status": "PASS" if repayable_difference == 0 else "FAIL",
            "difference_pln": str(repayable_difference)
        },
        "instalments": {
    "status": instalment_status,
    "difference_pln": str(payment_difference),
    "difference_equals_commission": equals_commission,
    "explanation_basis": (
        "lender_disclosed_fee_payment"
        if upfront_explains_difference else None
    )
},
"fee_payment_options": option_checks,
        "apr_validation": "NOT_RECALCULATED"
    }


# Run standalone tests when this file is executed directly
if __name__ == "__main__":

    path = Path("data/normalized/pl_competitors.json")

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    for product in data["products"]:

        result = validate_product(product)

        print(f"\n=== {product['brand']} ===")
        print(json.dumps(result, indent=2))