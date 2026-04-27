from config import IPQS_API_KEY, IPQS_URL

from flask import current_app as app
import requests

@app.get("/check_email/<email>")
def check_email(email: str):
    response: dict = requests.get(f"{IPQS_URL}json/email/{IPQS_API_KEY}/{email}").json()

    # Returns early if email is valid or a problem occurs connecting to the API
    if not response.get("success") or response.get("timed_out"):
        return {"success" : False, "reason" : "No valid response from IPQS API"}
    elif response.get("overall_score") == 0:
        return {"success" : False, "reason" : "Invalid email address"}
    
    # Converts fraud score into more easily readable values
    fraud_score: str
    int_score = response.get("fraud_score")
    match int_score: 
        case x if x >= 90:
            fraud_score = "malicious"
        case x if x >= 85:
            fraud_score = "high_risk"
        case x if x >= 75:
            fraud_score = "suspicious"
        case x if x >= 25:
            fraud_score = "neutral"
        case _:
            fraud_score = "low_risk"

    # Prepairs simplified response
    shared_keys = ["disposable", "leaked", "recent_abuse", "risky_tld", "valid", "spf_record", "dmarc_record"]
    simplified_response = {x : response.get(x) for x in shared_keys}    

    simplified_response["fraud_score"] = fraud_score
    simplified_response["email_address_creation_date"] = response.get("first_seen").get("human")
    simplified_response["domain_creation_date"] = response.get("domain_age").get("human")

    return simplified_response