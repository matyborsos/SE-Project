#! /usr/bin/env python
import unittest
import warnings
import matplotlib.pyplot as plt
from wdc import * # Import the wdc library

# Define a test class
class TestWDC(unittest.TestCase):
    def setUp(self):
        # Set up the DatabaseConnection and Datacube instances
        self.dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        self.dco = Datacube(self.dbc)
                 
    def test_basic(self):
        # Test the basic functionality
        result=self.dco.basic() 
        self.assertEqual(result, '1') 
    
    def test_1d_subset(self):
        # Test the Celsius function
        result=self.dco.get_1d_subset(53.08, 8.80)
        expected_result = '2.834646,4.488189,11.10236,20.19685,21.02362,21.29921,25.98425,24.33071,22.12598,16.06299,8.897637,2.283465'
        self.assertEqual(result, expected_result)
       
    def test_avg(self):
        # Test the Average functionality
        result = self.dco.avg(53.08, 8.80)
        self.assertEqual(result, '15.052493472894033')

    def test_min(self):
        # Test the average functionality
        result = self.dco.min(53.08, 8.80)
        self.assertEqual(result, '2.2834647')

    def test_max(self):
        # Test the maximum functionality
        result = self.dco.max(53.08, 8.80)
        self.assertEqual(result, '25.984251')
        
    def text_more_than(self):
        result = self.dco.when_temp_more_than_15(53.08, 8.80)
        self.assertEqual(result, '7')
        
    def test_subset1(self):
        # Test the subset functionality with the first image
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
        # Test the subset functionality with the second image
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

