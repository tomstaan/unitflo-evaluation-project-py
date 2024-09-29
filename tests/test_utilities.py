# tests/test_utilities.py
import unittest
import pandas as pd
import numpy as np
from src.utilities import normalize_data, detect_outliers, preprocess_input
from src.exceptions import UtilityError

class TestUtilities(unittest.TestCase):
    def test_normalize_data_success(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = normalize_data(df)
        self.assertTrue(isinstance(result, pd.DataFrame))

    def test_normalize_data_failure(self):
        with self.assertRaises(UtilityError):
            normalize_data(None)

    def test_detect_outliers_success(self):
        df = pd.DataFrame({'A': [1, 2, 100], 'B': [4, 5, 6]})
        result = detect_outliers(df)
        self.assertIn(2, result)

    def test_preprocess_input_success(self):
        input_data = {'a': 1, 'b': 2}
        result = preprocess_input(input_data)
        self.assertTrue(isinstance(result, np.ndarray))

    def test_preprocess_input_failure(self):
        with self.assertRaises(UtilityError):
            preprocess_input(123)

if __name__ == '__main__':
    unittest.main()
