import unittest
import sys
import os
import ast
import pandas as pd

test_dir = os.path.dirname(os.path.abspath(__file__))
# append relative directory of package being tested
sys.path.append(os.path.abspath(os.path.join(test_dir, '..', '..')))
# after all that tosh I can now nicely import my module :)
from pyCheckout import Shopping

# test definitions
test_csv = 'shop_tests.csv'
exclude_col_lst = ['notes']

class ShoppingTests(unittest.TestCase):
    def __init__(self, 
                 testName,
                 testmethodName,
                 expected_output,
                 **kwargs):
        """
        A class used to define generic tests for the Shopping class in shop.py
        :param testName: A descriptive name given to the test for debugging purposes
        :param testmethodName: The method being used for the test
        :param expected_output: Any type used to directly compare against the test output
        :param kwargs: All required Shopping inputs
        """
        super(ShoppingTests, self).__init__(testmethodName)
        self.testName = testName
        self.expected_output = expected_output
        self.kwargs = kwargs

    def setUp(self):
        """setUp for {}""".format(self.testName)
        print("test: {}".format(self.testName))

    def test_check_cart_pass(self):
        """checks the output of the cart dictionary keys equals expected output"""
        self.Cart = Shopping(**self.kwargs)
        self.assertEqual(sorted(list(self.Cart.cart_dict.keys())),
                         self.expected_output)

    def test_check_discounts_pass(self):
        """checks the output of the cart discounts dictionary keys equals expected output"""
        self.Cart = Shopping(**self.kwargs)
        self.assertEqual(sorted(list(self.Cart.cart_savings_dict.keys())),
                         self.expected_output)

    def test_check_cart_fail(self):
        """checks the output of the cart dictionary keys fails against an expected output"""
        self.Cart = Shopping(**self.kwargs)
        self.assertNotEqual(sorted(list(self.Cart.cart_dict.keys())),
                            self.expected_output)

    def test_sys_exit(self):
        """checks a sys.exit has been raised with an expected output if provided"""
        with self.assertRaises(SystemExit) as cm:
            Shopping(**self.kwargs)
        # sometimes there aren't error codes
        if self.expected_output:
            self.assertEqual(cm.exception.code, self.expected_output)

    def test_cart_subtotal_pass(self):
        """checks the carts subtotal price against an expected output"""
        self.Cart = Shopping(**self.kwargs)
        self.assertEqual(self.Cart.cart_subtotal, self.expected_output)

    def test_cart_discount_pass(self):
        """checks the carts discount price against an expected output"""
        self.Cart = Shopping(**self.kwargs)
        self.assertEqual(self.Cart.cart_discount, self.expected_output)

    def test_cart_total_pass(self):
        """checks the carts total price against an expected output"""
        self.Cart = Shopping(**self.kwargs)
        self.assertEqual(self.Cart.cart_total, self.expected_output)


# make an empty test suite
suite = unittest.TestSuite()
# read test cases csv
test_cases = pd.read_csv(os.path.join(test_dir, test_csv))

for test_num, row in test_cases.iterrows():
    # loop over the test csv to build up a dictionary of inputs
    test_inputs = {}
    for k, v in row.dropna().to_dict().items():
        if k not in exclude_col_lst:
            try:
                test_inputs[k] = ast.literal_eval(v)
            except ValueError:
                test_inputs[k] = v
    # determine the test method to use base off the testName
    testNameSplit = test_inputs['testName'].split('-')
    test_inputs['testmethodName'] = testNameSplit[0]
    test_inputs['testName'] = ''.join(testNameSplit[1:])
    # add the test to the test suite
    if test_inputs['testmethodName']:
        suite.addTest(ShoppingTests(**test_inputs))


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)
