import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Service configuration
# URL = "http://localhost:8080/single-email"
URL = "https://emailservice-53195221677.us-west1.run.app/single-email"
HEADERS = {'Content-Type': 'application/json'}

# Email data
payload = {
    "email": "test@example.com",
    "subject": "test email subject",
    "message": "Success! This is a test message",
    # example auth key, update key to provisioned key
    "auth_key": "sqqohokybg2bgfjga3bp7ydm9zjbjdsy"
}

try:
    response = requests.post(
        URL,
        headers=HEADERS,
        json=payload
    )
    response.raise_for_status()
    logger.info(f"Status Code: {response.status_code}")
    logger.info(f"Response: {response.json()}")
    
except requests.exceptions.RequestException as e:
    logger.error(f"Request failed: {e}")