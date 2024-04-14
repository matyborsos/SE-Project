#! /usr/bin/env python

import unittest
import warnings
from wdc import * # Imported the wdc library

class TestWDC(unittest.TestCase):
    def setUp(self):
        self.dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        self.dco = Datacube(self.dbc)

    def test_avg(self):
        # Define test cases to verify specific functionality of your library, for evemple the average functionality
        # For example:
        result = self.dco.avg(53.08, 8.80)
        self.assertEqual(result, '15.052493472894033')

    def test_min(self):
        # A test case to test the min functionality
        # For example:
        result = self.dco.min(53.08, 8.80)
        self.assertEqual(result, '2.2834647')

    def test_max(self):
        # A test case to test the max functionality
        # For example:
        result = self.dco.max(53.08, 8.80)
        self.assertEqual(result, '25.984251')

    def test_subset1(self):
        # A test case to test the subset functionality
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ResourceWarning)
            result, query = self.dco.subset("S2_L2A_32631_B12_20m", "2021-04-09", 679966, 710000, 4990230, 5015220)
        self.assertEqual(result.status_code, 200)
        expected_query = """
for $c in (S2_L2A_32631_B12_20m)
return
 encode(
$c[ansi("2021-04-09"), E(679966:710000),N(4990230:5015220)],
  "image/png" )"""
        self.assertEqual(query.strip(), expected_query.strip())

    def test_subset2(self):
        # Another test case to test the subset functionality
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=ResourceWarning)
            result, query = self.dco.subset("S2_L2A_32631_B01_60m", "2021-04-09", 669960, 729960, 4990200, 5015220)
        self.assertEqual(result.status_code, 200)
        expected_query = """
for $c in (S2_L2A_32631_B01_60m)
return
 encode(
$c[ansi("2021-04-09"), E(669960:729960),N(4990200:5015220)],
  "image/png" )"""
        self.assertEqual(query.strip(), expected_query.strip())

if __name__ == '__main__':
    unittest.main()

