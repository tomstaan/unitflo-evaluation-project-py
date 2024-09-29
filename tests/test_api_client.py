# tests/test_api_client.py
import unittest
from unittest.mock import patch, MagicMock
from src.api_client import APIClient
from src.exceptions import APIClientError

class TestAPIClient(unittest.TestCase):
    @patch('src.api_client.requests.get')
    def test_get_resource_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {'id': 1, 'name': 'Test Resource'}
        mock_get.return_value = mock_response

        client = APIClient()
        response = client.get_resource(1)
        self.assertEqual(response, {'id': 1, 'name': 'Test Resource'})

    @patch('src.api_client.requests.get')
    def test_get_resource_failure(self, mock_get):
        mock_get.side_effect = Exception("Request failed")
        client = APIClient()
        with self.assertRaises(APIClientError):
            client.get_resource(1)

if __name__ == '__main__':
    unittest.main()
