# src/utilities.py

import pandas as pd
import numpy as np
from src.exceptions import UtilityError
import logging

logger = logging.getLogger(__name__)

def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    try:
        logger.info(f"Starting normalization for dataframe:\n{df}")
        normalized_df = (df - df.mean()) / df.std()
        logger.info(f"Normalization successful. Result:\n{normalized_df}")
        return normalized_df
    except Exception as e:
        logger.error(f"Data normalization failed: {e}")
        raise UtilityError(f"Data normalization failed: {e}")

def detect_outliers(df: pd.DataFrame, threshold: float = 3.5) -> list:
    """
    Detects outliers in a DataFrame using the Modified Z-Score method.
    Parameters:
        - df: pandas DataFrame
        - threshold: The Modified Z-Score threshold. Default is 3.5.
    Returns:
        - List of indices where outliers are detected.
    """
    try:
        if not isinstance(df, pd.DataFrame):
            logger.error(f"Input is not a DataFrame: {df}")
            raise UtilityError("Input must be a DataFrame")

        logger.info(f"Starting outlier detection for dataframe:\n{df}")

        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if numeric_cols.empty:
            logger.warning("No numeric columns found in dataframe.")
            return []

        outlier_indices = []
        for col in numeric_cols:
            data = df[col]
            median = data.median()
            mad = np.median(np.abs(data - median))
            if mad == 0:
                mad = np.finfo(float).eps  # Prevent division by zero
            modified_z_scores = 0.6745 * (data - median) / mad
            logger.info(f"Column: {col}, Median: {median}, MAD: {mad}")
            logger.info(f"Modified Z-Scores for column '{col}':\n{modified_z_scores}")
            col_outliers = data[np.abs(modified_z_scores) > threshold].index.tolist()
            logger.info(f"Outliers detected in column '{col}': {col_outliers}")
            outlier_indices.extend(col_outliers)

        unique_outliers = list(set(outlier_indices))
        logger.info(f"Total unique outliers detected: {unique_outliers}")
        return unique_outliers
    except Exception as e:
        logger.error(f"Outlier detection failed: {e}")
        raise UtilityError(f"Outlier detection failed: {e}")

def preprocess_input(input_data):
    try:
        logger.info(f"Preprocessing input: {input_data}")
        if isinstance(input_data, dict):
            processed_input = np.array(list(input_data.values()))
        elif isinstance(input_data, list):
            processed_input = np.array(input_data)
        elif isinstance(input_data, np.ndarray):
            processed_input = input_data
        else:
            raise ValueError("Unsupported input data type.")
        logger.info(f"Preprocessed input result: {processed_input}")
        return processed_input
    except Exception as e:
        logger.error(f"Input preprocessing failed: {e}")
        raise UtilityError(f"Input preprocessing failed: {e}")
