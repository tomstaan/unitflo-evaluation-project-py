# src/exceptions.py
class DataProcessingError(Exception):
    pass

class APIClientError(Exception):
    pass

class ModelError(Exception):
    pass

class UtilityError(Exception):
    pass

class ServiceError(Exception):
    pass

class ValidationError(Exception):
    pass
