from flask import current_app as app
import random

# Returns fake data about the email (used for a demo but should not be used for any real purposes)
def mock_check_email(email: str) -> dict:
    response: dict = {}

    good_attributes = ["Success", "valid", "spf_record", "dmarc_record"]
    bad_attributes = ["disposable", "leaked", "recent_abuse", "risky_tld"]

    # Makes email with all good attributes
    response["domain_creation_date"] = f"{random.randint(10, 20)} years ago"
    response["email_address_creation_date"] = f"{random.randint(2, 10)} years ago"
    response = response | {x : True for x in good_attributes} | {x : False for x in bad_attributes}
    
    # Determines how malicouse the email should appear
    threat_level: int = random.randint(1,5)

    # Sets certian attributes to be bad based on malicousness
    if threat_level == 1:
        response["fraud_score"] = "low_risk"
    
    if threat_level >= 2:
        response["fraud_score"] = "neutral"
            
        anti_spoofing = bool(random.randint(0,1))
        response["spf_record"] = anti_spoofing            
        response["dmarc_record"] = anti_spoofing

    if threat_level >= 3:
        response["fraud_score"] = "suspicious"
        
        risky_tld = bool(random.randint(0,1))
        response["risky_tld"] = risky_tld
        
    if threat_level >= 4:
        response["fraud_score"] = "high_risk"
        
        leaked = bool(random.randint(0,1))
        response["leaked"] = leaked
        
        disposable = bool(random.randint(0,1))
        response["disposable"] = disposable
        if disposable:
            response["email_address_creation_date"] = "Just now"

    if threat_level >= 5:
        response["fraud_score"] = "malicious"
        response["recent_abuse"] = True

    return response