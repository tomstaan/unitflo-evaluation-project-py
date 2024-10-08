# tests/test_data_processor.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.data_processor import DataProcessor
from src.data.data_source import DataSource
from src.exceptions import DataProcessingError
import logging

# Configure logging for the tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestDataProcessor(unittest.TestCase):

    def test_process_success(self):
        with patch('src.data_processor.ServiceB') as mock_service_b_class, \
             patch('src.data_processor.ServiceA') as mock_service_a_class, \
             patch('src.data_processor.normalize_data') as mock_normalize_data, \
             patch('src.data_processor.detect_outliers') as mock_detect_outliers, \
             patch('src.data_processor.DataSource') as mock_data_source_class:

            # Mock DataSource
            mock_data_source = MagicMock()
            mock_data_source.fetch_data.return_value = {'col1': [1, 2], 'col2': [3, 4]}
            mock_data_source_class.return_value = mock_data_source

            # Mock normalize_data
            mock_normalize_data.return_value = pd.DataFrame({'col1': [0.1, 0.2], 'col2': [0.3, 0.4]})

            # Mock detect_outliers
            mock_detect_outliers.return_value = []

            # Mock ServiceA and ServiceB
            mock_service_a = MagicMock()
            mock_service_a.enrich_data.return_value = pd.DataFrame({'col1': [0.1, 0.2], 'col2': [0.3, 0.4], 'enriched': [0.4, 0.6]})
            mock_service_a_class.return_value = mock_service_a

            mock_service_b = MagicMock()
            mock_service_b.transform_data.return_value = pd.DataFrame({'col1': [0.1, 0.2], 'col2': [0.3, 0.4], 'enriched': [0.4, 0.6], 'transformed': [0.8, 1.2]})
            mock_service_b_class.return_value = mock_service_b

            data_source = DataSource()
            processor = DataProcessor(data_source)
            result = processor.process()
            self.assertIn('transformed', result.columns)

    def test_process_failure(self):
        data_source = MagicMock()
        data_source.fetch_data.side_effect = Exception("Data fetch failed")
        processor = DataProcessor(data_source)
        with self.assertRaises(DataProcessingError):
            processor.process()

    def test_process_nan_dataframe(self):
        data_source = MagicMock()
        data_source.fetch_data.return_value = {'col1': [float('nan'), float('nan')]}
        processor = DataProcessor(data_source)
        with self.assertRaises(DataProcessingError):
            processor.process()


if __name__ == '__main__':
    unittest.main()
