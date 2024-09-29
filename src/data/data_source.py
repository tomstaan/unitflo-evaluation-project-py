# src/data/data_source.py
import random
from src.exceptions import DataProcessingError
import logging

logger = logging.getLogger(__name__)

class DataSource:
    def __init__(self, source_type='json'):
        self.source_type = source_type

    def fetch_data(self):
        try:
            if self.source_type == 'json':
                return self._fetch_json_data()
            elif self.source_type == 'csv':
                return self._fetch_csv_data()
            else:
                raise ValueError(f"Unsupported source type: {self.source_type}")
        except Exception as e:
            logger.error(f"Data fetching failed: {e}")
            raise DataProcessingError(f"Data fetching failed: {e}")

    def _fetch_json_data(self):
        # Simulate fetching JSON data with unknown structure
        data = {'value': random.random()}
        return data

    def _fetch_csv_data(self):
        # Simulate fetching CSV data with unknown columns
        data = [{'col1': random.randint(0, 100), 'col2': random.random()}]
        return data
