"""
CS 3250 - Software Dev. Methods and Tools
Instructor: Thyago Mota
Student: Jose_Torres
Description: Homework 09 - White-box (Unit) Testing
"""

import unittest

from src.loan import Loan


class TestLoan(unittest.TestCase):
    def setUp(self):
        self.loan = Loan(12000, 1, 0.12)

    def test_01_amount_below_minimum(self):
        with self.assertRaises(ValueError):
            Loan(Loan.MIN_LOAN_AMOUNT - 1, 1, 0.12)

    def test_02_amount_above_maximum(self):
        with self.assertRaises(ValueError):
            Loan(Loan.MAX_LOAN_AMOUNT + 1, 1, 0.12)

    def test_03_years_below_minimum(self):
        with self.assertRaises(ValueError):
            Loan(12000, Loan.MIN_YEARS - 1, 0.12)

    def test_04_years_above_maximum(self):
        with self.assertRaises(ValueError):
            Loan(12000, Loan.MAX_YEARS + 1, 0.12)

    def test_05_interest_at_minimum(self):
        with self.assertRaises(ValueError):
            Loan(12000, 1, Loan.MIN_INTEREST_RATE)

    def test_06_interest_at_maximum(self):
        with self.assertRaises(ValueError):
            Loan(12000, 1, Loan.MAX_INTEREST_RATE)

    def test_07_valid_loan_initial_state(self):
        self.assertEqual(self.loan.loan_amount, 12000)
        self.assertEqual(self.loan.years, 1)
        self.assertEqual(self.loan.interest_rate, 0.12)
        # Independently calculated for $12,000 at 1% monthly over 12 months.
        self.assertAlmostEqual(self.loan.monthly_payment, 1066.1854641401, places=8)
        self.assertEqual(self.loan.remaining_balance, 12000)
        self.assertEqual(self.loan.months_remaining, 12)

    def test_08_payment_below_monthly_payment(self):
        with self.assertRaises(ValueError):
            self.loan.make_payment(self.loan.monthly_payment - 0.01)
        self.assertEqual(self.loan.remaining_balance, 12000)
        self.assertEqual(self.loan.months_remaining, 12)

    def test_09_payment_above_remaining_balance(self):
        with self.assertRaises(ValueError):
            self.loan.make_payment(self.loan.remaining_balance + 0.01)
        self.assertEqual(self.loan.remaining_balance, 12000)
        self.assertEqual(self.loan.months_remaining, 12)

    def test_10_payment_equal_to_monthly_payment(self):
        self.loan.make_payment(self.loan.monthly_payment)
        self.assertAlmostEqual(
            self.loan.remaining_balance, 10933.8145358599, places=8
        )
        self.assertEqual(self.loan.months_remaining, 11)

    def test_11_payment_equal_to_remaining_balance(self):
        self.loan.make_payment(self.loan.remaining_balance)
        self.assertAlmostEqual(self.loan.remaining_balance, 0.0, places=8)
        self.assertEqual(self.loan.months_remaining, 0)


if __name__ == "__main__":
    unittest.main()
