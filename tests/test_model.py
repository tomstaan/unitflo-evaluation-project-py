# tests/test_model.py
import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from src.model import Model
from src.exceptions import ModelError

class TestModel(unittest.TestCase):
    @patch('src.model.importlib.import_module')
    @patch('src.model.preprocess_input')
    def test_predict_success(self, mock_preprocess_input, mock_import_module):
        mock_model_module = MagicMock()
        mock_model = MagicMock()
        mock_model.predict.return_value = [0]
        mock_model_module.load_model.return_value = mock_model
        mock_import_module.return_value = mock_model_module

        mock_preprocess_input.return_value = np.array([1, 2, 3])

        model = Model('test_model')
        result = model.predict([1, 2, 3])
        self.assertEqual(result, [0])

    @patch('src.model.importlib.import_module')
    def test_model_load_failure(self, mock_import_module):
        mock_import_module.side_effect = ImportError("Module not found")
        with self.assertRaises(ModelError):
            Model('non_existent_model')

if __name__ == '__main__':
    unittest.main()
