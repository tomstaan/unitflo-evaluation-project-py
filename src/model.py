import importlib
import numpy as np
from src.exceptions import ModelError
from src.utilities import preprocess_input
import logging

logger = logging.getLogger(__name__)

class Model:
    def __init__(self, model_name):
        try:
            model_module = importlib.import_module(f"models.{model_name}")
            self.model = model_module.load_model()
        except ImportError as e:
            logger.error(f"ImportError: {e}")
            raise ModelError(f"Model {model_name} could not be loaded: {e}")

    def predict(self, input_data):
        try:
            processed_data = preprocess_input(input_data)
            if np.isnan(processed_data).any():
                raise ValueError("Input data contains NaN values.")
            predictions = self.model.predict(processed_data)
            return predictions
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise ModelError(f"Prediction failed: {e}")
