import json, smtplib, ssl, logging
from flask import Flask, request, jsonify
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from time import sleep
from dotenv import load_dotenv
import os

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Log environment variables
logger.info(f"Environment AUTH_KEY: {os.getenv('AUTH_KEY')}")
logger.info(f"Environment loaded from: {os.getenv('DOTENV_FILE')}")

# After load_dotenv()
logger.info("Environment variables loaded:")
logger.info(f"AUTH_KEY from env: '{os.getenv('AUTH_KEY')}'")
logger.info(f"SMTP_SERVER from env: '{os.getenv('SMTP_SERVER')}'")

# Add debug logging
logger.debug(f"AUTH_KEY from env: {os.getenv('AUTH_KEY')}")

# Email Configuration
SMTP_SERVER = os.getenv("SMTP_SERVER").strip('"')
SMTP_PORT = os.getenv("SMTP_PORT")
SENDER_EMAIL = os.getenv("SENDER_EMAIL").strip('"')
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD").strip('"')
AUTH_KEY = os.getenv("AUTH_KEY").strip('"')  # Remove quotes

# Add debug logging
logger.info(f"Sanitized AUTH_KEY: {AUTH_KEY}")

# Service Configuration
DELAY = 2
HOST = '0.0.0.0'  # Allow external connections
PORT = 8080

app = Flask(__name__)

@app.route("/single-email", methods=["POST"])
def sendSingleEmail():
    sleep(DELAY)
    
    try:
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415
            
        data = request.get_json()
        logger.info(f"Processing POST request with data: {data}")
        
        # Extract parameters from JSON body
        recipient_email = data.get("email")
        subject = data.get("subject", "No Subject")
        message = data.get("message", "Empty Message")
        auth_key = data.get("auth_key")

        if not recipient_email:
            return jsonify({"error": "Email recipient required"}), 400

        if not subject:
            return jsonify({"error": "Email subject required"}), 400

        if not message: 
            return jsonify({"error": "Email message required"}), 400

        logger.debug(f"Received auth_key: {auth_key}")
        logger.debug(f"Expected AUTH_KEY: {AUTH_KEY}")

        if not auth_key: 
            return jsonify({"error": "Authentication parameter required"}), 400

        # Sanitize received key
        auth_key = data.get("auth_key").strip()
        
        logger.debug(f"Sanitized received key: {auth_key}")
        logger.debug(f"Sanitized expected key: {AUTH_KEY}")

        if auth_key != AUTH_KEY:
            logger.error(f"Auth failed. Received: '{auth_key}', Expected: '{AUTH_KEY}'")
            return jsonify({"error": "Authentication failed"}), 401


        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)

            server.send_message(msg)
            
        logger.info(f"Email sent successfully to {recipient_email}")
        return jsonify({"message": f"Email sent to {recipient_email}"}), 200
        
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)