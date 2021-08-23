import unittest
from questions3 import gross_income, income_tax, net_income, super_rate

class  TestQuestion(unittest.TestCase):

    def test_gross_income(self):
        self.assertEqual(gross_income(32400), 2700)

    def test_income_tax(self):
        self.assertEqual(income_tax(32400), 38556)

    def test_net_income(self):
        self.assertEqual(net_income(2700, 38556), -35856)

    def test_super_rate(self):
        self.assertEqual(super_rate(2700, 2), 5400)

if __name__ == "__main__":
    unittest.main() 