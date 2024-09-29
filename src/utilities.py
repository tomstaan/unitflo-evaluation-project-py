# src/utilities.py
import pandas as pd
import numpy as np
from src.exceptions import UtilityError
import logging

logger = logging.getLogger(__name__)

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        return (df - df.mean()) / df.std()
    except Exception as e:
        logger.error(f"Data normalization failed: {e}")
        raise UtilityError(f"Data normalization failed: {e}")

def detect_outliers(df: pd.DataFrame) -> list:
    try:
        z_scores = np.abs((df - df.mean()) / df.std())
        outliers = np.where(z_scores > 3)
        return list(set(outliers[0]))
    except Exception as e:
        logger.error(f"Outlier detection failed: {e}")
        raise UtilityError(f"Outlier detection failed: {e}")

def preprocess_input(input_data):
    try:
        # Handle unknown data formats
        if isinstance(input_data, dict):
            return np.array(list(input_data.values()))
        elif isinstance(input_data, list):
            return np.array(input_data)
        else:
            raise ValueError("Unsupported input data type.")
    except Exception as e:
        logger.error(f"Input preprocessing failed: {e}")
        raise UtilityError(f"Input preprocessing failed: {e}")
