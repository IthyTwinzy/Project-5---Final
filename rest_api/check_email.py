from config import IPQS_API_KEY, IPQS_URL

from flask import current_app as app
import requests

# Converts a fraud score int into a string reperesentation
def _get_fraud_string(fraud_score: float) -> str:
    match fraud_score: 
        case None:
            return "no_data"
        case x if x >= 90:
            return "malicious"
        case x if x >= 85:
            return "high_risk"
        case x if x >= 75:
            return "suspicious"
        case x if x >= 25:
            return "neutral"
        case _:
            return "low_risk"


@app.get("/check_email/<email>")
def check_email(email: str) -> dict:
    """Returns JSON data about the risk of the specified email"""
    
    response: dict = requests.get(f"{IPQS_URL}json/email/{IPQS_API_KEY}/{email}").json()

    # Returns early if email is invalid or a problem occurs connecting to the API
    if not response.get("success") or response.get("timed_out"):
        return {"success" : False, "reason" : "No valid response from IPQS API"}
    elif response.get("overall_score") == 0:
        return {"success" : False, "reason" : "Invalid email address"}
    
    # Prepairs simplified response
    shared_keys = ["success", "disposable", "leaked", "recent_abuse", "risky_tld", "valid", "spf_record", "dmarc_record"]
    simplified_response = {x : response.get(x) for x in shared_keys}    

    simplified_response["fraud_score"] = _get_fraud_string(response.get("fraud_score"))
    simplified_response["email_address_creation_date"] = response.get("first_seen").get("human")
    simplified_response["domain_creation_date"] = response.get("domain_age").get("human")
    return simplified_response