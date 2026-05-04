from check_email import check_email
from mock_check_email import mock_check_email
from flask import current_app as app

# Routs check email to the apropriate function depending on whether real data is being used
@app.get("/check_email/<email>")
def check_email_address(email):
    """Returns JSON data about the risk of the specified email address"""
    
    if app.config.get("FAKE_DATA"):
        return mock_check_email(email)
    else:
        return check_email(email)