# src/data_processor.py
import pandas as pd
import numpy as np
from src.exceptions import DataProcessingError
from data.data_source import DataSource
from services.service_a import ServiceA
from services.service_b import ServiceB
from utilities import normalize_data, detect_outliers
from validations import validate_dataframe


class DataProcessor:
    def __init__(self, source: DataSource):
        self.source = source
        self.service_a = ServiceA()
        self.service_b = ServiceB()

    def process(self):
        try:
            data = self.source.fetch_data()
            df = pd.DataFrame(data)
            validate_dataframe(df)
            df = normalize_data(df)
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
            raise DataProcessingError(f"Data processing failed: {e}")
