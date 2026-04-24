from config import IPQS_API_KEY, IPQS_URL
from flask import Flask
import requests

app = Flask(__name__)

# Validate API key
if IPQS_API_KEY == None or IPQS_API_KEY == "":
    raise KeyError("IPQS API Key not provided")
elif not requests.get(IPQS_URL + "json/account/" + IPQS_API_KEY).json().get("success"):
    raise KeyError("Invalid IPQS API Key")


# Import routes
with app.app_context():
    # Put imports to any routes here
    pass

if __name__ == "__main__":
    app.run(debug=True)