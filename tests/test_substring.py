
# Make sure the test finds the application code
import os
import sys
sys.path.insert(0, os.path.abspath('.'))

import unittest
from app import string_utils

class TestSubstring(unittest.TestCase):

    def test_equal_substrings(self):
        score:float = string_utils.calculate_match_degree("software engineering","software engineering")
        self.assertEqual(score, 1)    
        
    def test_partial_substrings(self):
        score:float = string_utils.calculate_match_degree("software engineering","building engineering")
        self.assertEqual(score, 0.6)

if __name__ == "__main__":
    unittest.main()