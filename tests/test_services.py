import unittest
import pandas as pd
from src.services.service_a import ServiceA
from src.services.service_b import ServiceB
from src.exceptions import ServiceError


class TestServiceA(unittest.TestCase):

    def test_enrich_data_success(self):
        df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
        service_a = ServiceA()
        result = service_a.enrich_data(df)
        self.assertIn('enriched', result.columns)

    def test_enrich_data_failure(self):
        service_a = ServiceA()
        with self.assertRaises(ServiceError):
            service_a.enrich_data(None)


class TestServiceB(unittest.TestCase):

    def test_transform_data_success(self):
        df = pd.DataFrame({'enriched': [4, 6]})
        service_b = ServiceB()
        result = service_b.transform_data(df)
        self.assertIn('transformed', result.columns)

    def test_transform_data_failure(self):
        df = pd.DataFrame({'A': [1, 2]})
        service_b = ServiceB()
        with self.assertRaises(ServiceError):
            service_b.transform_data(df)

    def test_transform_data_missing_enriched_column(self):
        df = pd.DataFrame({'A': [1, 2]})
        service_b = ServiceB()
        with self.assertRaises(ServiceError):
            service_b.transform_data(df)


if __name__ == '__main__':
    unittest.main()
