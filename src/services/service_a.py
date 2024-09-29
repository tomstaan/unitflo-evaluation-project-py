# src/services/service_a.py
from exceptions import ServiceError
import logging

logger = logging.getLogger(__name__)

class ServiceA:
    def enrich_data(self, df):
        try:
            # Simulate data enrichment
            df['enriched'] = df.apply(lambda x: x.sum(), axis=1)
            return df
        except Exception as e:
            logger.error(f"Data enrichment failed: {e}")
            raise ServiceError(f"Data enrichment failed: {e}")
