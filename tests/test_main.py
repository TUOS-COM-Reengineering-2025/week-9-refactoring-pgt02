import unittest
import io
import contextlib

from main import CustomerManager, calculate_shipping_fee_for_fragile_items

class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)


import unittest
import io
import contextlib

from main import CustomerManager, calculate_shipping_fee_for_fragile_items


class TestCustomerManager(unittest.TestCase):

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        # Capture printed output
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)

    def test_calculate_shipping_fee_for_heavy_items(self):
        from main import calculate_shipping_fee_for_heavy_items
        purchases_heavy = [{'price': 100, 'weight': 25}]
        purchases_light = [{'price': 100, 'weight': 10}]

        self.assertEqual(calculate_shipping_fee_for_heavy_items(purchases_heavy), 50)
        self.assertEqual(calculate_shipping_fee_for_heavy_items(purchases_light), 20)

    def test_add_purchases(self):
        cm = CustomerManager()
        name = "Shreyas"
        purchases = [{'price': 100, 'item': 'laptop'}, {'price': 50, 'item': 'mouse'}]
        cm.add_purchases(name, purchases)
        self.assertIn(name, cm.customers)
        self.assertEqual(cm.customers[name], purchases)

    def test_generate_report_output(self):
        cm = CustomerManager()

        # Add a customer whose total purchase causes different branches to be hit
        cm.add_customer("Shreyas", [
            {'price': 900},  # taxed → 900 * 1.2 = 1080 (above tax threshold of 500)
            {'price': 100}  # not taxed
        ])

        cm.add_customer("Alice", [
            {'price': 300},  # taxed → 900 * 1.2 = 1080 (above tax threshold of 500)
            {'price': 10}  # not taxed
        ])
        cm.add_customer("James", [
            {'price': 1000},  # taxed → 900 * 1.2 = 1080 (above tax threshold of 500)
            {'price': 10}  # not taxed
        ])

        expected_lines = [
            "Shreyas",
            "Eligible for discount",  # 1230 > 500
            "VIP Customer!",  # 1230 > 1000
        ]
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            cm.generate_report()

        output = captured.getvalue()

        for line in expected_lines:
            self.assertIn(line, output)


if __name__ == "__main__":
    unittest.main()
