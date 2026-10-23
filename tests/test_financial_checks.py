import copy
import json
import unittest
from pathlib import Path

from financial_checks import validate_product


class TestFinancialChecks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        file_path = Path("data/normalized/pl_competitors.json")

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        cls.products = {
            product["brand"]: product
            for product in data["products"]
        }

    # TEST 1: Provident repayment schedule
    def test_provident_instalments(self):

        product = self.products["Provident"]

        result = validate_product(product)

        self.assertEqual(
            result["instalments"]["status"],
            "PASS"
        )

        self.assertEqual(
            result["total_repayable"]["status"],
            "PASS"
        )

    # TEST 2: Wonga fee-payment options
    def test_wonga_fee_options(self):

        product = self.products["Wonga"]

        result = validate_product(product)

        self.assertEqual(
            result["instalments"]["status"],
            "EXPLAINED_DIFFERENCE"
        )

        for option in result["fee_payment_options"]:
            self.assertEqual(option["status"], "PASS")

        self.assertEqual(
            len(result["fee_payment_options"]),
            2
        )

    # TEST 3: Detect an incorrect financial figure
    def test_detect_incorrect_customer_outflow(self):

        product = copy.deepcopy(self.products["Wonga"])

        # Introduce an intentional error
        product["fee_payment_options"][1][
            "total_customer_outflow_pln"
        ] = 99999

        result = validate_product(product)

        financing_option = result["fee_payment_options"][1]

        self.assertEqual(
            financing_option["status"],
            "REVIEW"
        )


if __name__ == "__main__":
    unittest.main()