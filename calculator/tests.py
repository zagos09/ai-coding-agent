import unittest
from pkg.calculator import Calculator

class TestCalculator(unittest.TestCase):
    """
    Unit tests for the Calculator class.
    
    These tests ensure that:
    1. Basic arithmetic operations work correctly.
    2. Operator precedence is respected (e.g., multiplication before addition).
    3. Errors (invalid inputs, empty strings) are handled gracefully.
    """

    def setUp(self):
        """Initializes a new Calculator instance before each test."""
        self.calculator = Calculator()

    def test_addition(self):
        """Tests basic addition."""
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        """Tests basic subtraction."""
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        """Tests basic multiplication."""
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        """Tests basic division."""
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        """
        Tests operator precedence.
        Expected: 3 * 4 = 12, then 12 + 5 = 17.
        """
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        """
        Tests a mix of operators to ensure correct evaluation order.
        Calculation: (2*3) - (8/2) + 5  =>  6 - 4 + 5  =>  7
        """
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        """Tests that an empty input returns None (and doesn't crash)."""
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        """Tests that invalid symbols raise a ValueError."""
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        """Tests malformed expressions (e.g., operator without enough numbers)."""
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")


if __name__ == "__main__":
    unittest.main()