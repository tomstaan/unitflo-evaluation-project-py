import unittest
import pandas as pd
import numpy as np
from src.utilities import normalize_data, detect_outliers, preprocess_input
from src.exceptions import UtilityError
import logging

# Configure logging for the tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestUtilities(unittest.TestCase):

    def test_normalize_data_success(self):
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = normalize_data(df)
        self.assertIsInstance(result, pd.DataFrame)
        logger.info(f"Normalized DataFrame:\n{result}")

    def test_normalize_data_failure(self):
        with self.assertRaises(UtilityError):
            normalize_data(None)

    def test_detect_outliers_success(self):
        # Test data where 100 in column 'A' should be detected as an outlier
        df = pd.DataFrame({'A': [1, 2, 100], 'B': [4, 5, 6]})
        logger.info("Running outlier detection test...")

        # Expect index 2 (value 100 in column 'A') to be detected as an outlier
        result = detect_outliers(df, threshold=3.5)  # Using default threshold

        # Ensure index 2 is detected as an outlier
        self.assertIn(2, result, msg=f"Outliers detected: {result}")

    def test_detect_outliers_no_outliers(self):
        # Test with data that has no outliers
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        result = detect_outliers(df)
        self.assertEqual(result, [], msg=f"Unexpected outliers detected: {result}")

    def test_detect_outliers_failure(self):
        # Test with invalid input
        with self.assertRaises(UtilityError):
            detect_outliers(None)

    def test_preprocess_input_success_dict(self):
        input_data = {'a': 1, 'b': 2}
        result = preprocess_input(input_data)
        self.assertIsInstance(result, np.ndarray)
        logger.info(f"Preprocessed input from dict: {result}")

    def test_preprocess_input_success_list(self):
        input_data = [1, 2, 3]
        result = preprocess_input(input_data)
        self.assertIsInstance(result, np.ndarray)
        logger.info(f"Preprocessed input from list: {result}")

    def test_preprocess_input_failure(self):
        with self.assertRaises(UtilityError):
            preprocess_input(123)


if __name__ == '__main__':
    unittest.main()
