from config import IPQS_API_KEY, IPQS_URL, MockedDataDebugConfig
from flask import Flask
import requests

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Validate API key
    if not app.config.get("FAKE_DATA"):
        if IPQS_API_KEY == None or IPQS_API_KEY == "":
            raise KeyError("IPQS API Key not provided")
        elif not requests.get(IPQS_URL + "json/account/" + IPQS_API_KEY).json().get("success"):
            raise KeyError("Invalid IPQS API Key")

    # Import routes
    with app.app_context():
        import routes

    return app

if __name__ == "__main__":
    app = create_app(MockedDataDebugConfig)
    app.run()