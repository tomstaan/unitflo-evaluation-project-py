# src/services/service_b.py
from src.exceptions import ServiceError
import logging

logger = logging.getLogger(__name__)

class ServiceB:
    def transform_data(self, df):
        try:
            # Simulate data transformation with unknown edge cases
            df['transformed'] = df['enriched'] * 2
            return df
        except KeyError as e:
            logger.error(f"Data transformation failed: {e}")
            raise ServiceError(f"Data transformation failed: {e}")
