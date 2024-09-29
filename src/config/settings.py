# src/config/settings.py
import os

class Settings:
    API_ENDPOINT = os.getenv('API_ENDPOINT', 'https://api.example.com')
    API_USERNAME = os.getenv('API_USERNAME', 'user')
    API_PASSWORD = os.getenv('API_PASSWORD', 'pass')
    TIMEOUT = int(os.getenv('TIMEOUT', '30'))

    if TIMEOUT <= 0:
        raise ValueError("TIMEOUT must be a positive integer")
