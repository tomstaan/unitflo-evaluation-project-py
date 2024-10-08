import unittest
from unittest.mock import patch, MagicMock
from src.api_client import APIClient
from src.exceptions import APIClientError
import requests


class TestAPIClient(unittest.TestCase):

    def test_get_resource_success(self):
        with patch('src.api_client.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_response.json.return_value = {'id': 1, 'name': 'Test Resource'}
            mock_get.return_value = mock_response

            client = APIClient()
            response = client.get_resource(1)
            self.assertEqual(response, {'id': 1, 'name': 'Test Resource'})

    def test_get_resource_failure(self):
        with patch('src.api_client.requests.get') as mock_get:
            # Simulate a requests exception
            mock_get.side_effect = requests.exceptions.RequestException("Request failed")

            client = APIClient()
            with self.assertRaises(APIClientError):
                client.get_resource(1)

    def test_get_resource_unexpected_status_code(self):
        with patch('src.api_client.requests.get') as mock_get:
            # Mock a response with an unexpected status code
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
            mock_get.return_value = mock_response

            client = APIClient()
            with self.assertRaises(APIClientError):
                client.get_resource(1)


if __name__ == '__main__':
    unittest.main()
