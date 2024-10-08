import unittest
import pandas as pd
from src.validations import validate_dataframe
from src.exceptions import ValidationError


class TestValidations(unittest.TestCase):

    def test_validate_dataframe_success(self):
        df = pd.DataFrame({'A': [1, 2]})
        validate_dataframe(df)

    def test_validate_dataframe_failure_empty(self):
        df = pd.DataFrame()
        with self.assertRaises(ValidationError):
            validate_dataframe(df)

    def test_validate_dataframe_failure_not_dataframe(self):
        with self.assertRaises(ValidationError):
            validate_dataframe(None)


if __name__ == '__main__':
    unittest.main()
