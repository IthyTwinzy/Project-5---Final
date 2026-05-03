from config import IPQS_API_KEY, IPQS_URL
from flask import Flask
import requests

def create_app(debug = False, use_fake_data = False):
    app = Flask(__name__)

    # Validate API key
    if not use_fake_data:
        if IPQS_API_KEY == None or IPQS_API_KEY == "":
            raise KeyError("IPQS API Key not provided")
        elif not requests.get(IPQS_URL + "json/account/" + IPQS_API_KEY).json().get("success"):
            raise KeyError("Invalid IPQS API Key")


    # Import routes
    with app.app_context():
        if use_fake_data:
            import mock_check_email
        else:
            import check_email

    app.config["DEBUG"] = debug

    return app

if __name__ == "__main__":
    app = create_app(debug=True, use_fake_data= True)
    app.run()