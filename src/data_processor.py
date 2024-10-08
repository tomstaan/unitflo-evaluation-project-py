# src/data_processor.py

import pandas as pd
import numpy as np
from src.exceptions import DataProcessingError
from src.data.data_source import DataSource
from src.services.service_a import ServiceA
from src.services.service_b import ServiceB
from src.utilities import normalize_data, detect_outliers
from src.validations import validate_dataframe
import logging

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self, source: DataSource):
        self.source = source
        self.service_a = ServiceA()
        self.service_b = ServiceB()

    def process(self):
        try:
            data = self.source.fetch_data()

            # Ensure data is in correct format for DataFrame
            if isinstance(data, dict) and all(isinstance(v, (int, float)) for v in data.values()):
                data = {k: [v] for k, v in data.items()}  # Convert scalar values to lists

            df = pd.DataFrame(data)
            validate_dataframe(df)
            df = normalize_data(df)

            # Check for DataFrame with only NaN values
            if df.isnull().all().all():
                logger.error("DataFrame contains only NaN values.")
                raise DataProcessingError("DataFrame contains only NaN values.")

            unknown_values = df.isnull().sum()
            if unknown_values.any():
                df = df.fillna(method='ffill').fillna(method='bfill')

            outliers = detect_outliers(df)
            if outliers:
                df = df.drop(outliers)
            df = self.service_a.enrich_data(df)
            df = self.service_b.transform_data(df)
            return df
        except Exception as e:
            logger.error(f"Data processing failed: {e}")
            raise DataProcessingError(f"Data processing failed: {e}")
