import requests
from requests.auth import HTTPBasicAuth
from src.exceptions import APIClientError
from src.config.settings import Settings
import logging

logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self):
        self.base_url = Settings.API_ENDPOINT
        self.auth = HTTPBasicAuth(Settings.API_USERNAME, Settings.API_PASSWORD)

    def get_resource(self, resource_id):
        try:
            response = requests.get(
                f"{self.base_url}/resources/{resource_id}",
                auth=self.auth,
                timeout=Settings.TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTPError: {e}")
            raise APIClientError(f"API request failed: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"RequestException: {e}")
            raise APIClientError(f"API request failed: {e}")
