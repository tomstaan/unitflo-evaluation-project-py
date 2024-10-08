# src/validations.py
import pandas as pd
from src.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

def validate_dataframe(df: pd.DataFrame):
    if not isinstance(df, pd.DataFrame):  # Ensure the input is a DataFrame
        logger.error("Input is not a DataFrame.")
        raise ValidationError("Input is not a DataFrame.")
    
    if df.empty:
        logger.error("DataFrame is empty.")
        raise ValidationError("DataFrame is empty.")

