import requests


def email_threat_checker(email: str) -> dict:
    response = requests.get(f"http://127.0.0.1:5000/check_email/{email}").json()
    return response



"""def user_quality(email: dict) -> bool:
    userScore = spam_trap_score(email)
    if userScore.get('valid') == True:
        if userScore.get('disposable') == False:
            if userScore.get('fraud_score') < 90:
                return True
    return False

def flagged(email: dict) -> int:
    count = 0
    if user_quality(email) == False:
        count += 1
    if strickest_marketing(email) == False:
        count += 1
    if stricter_marketing(email) == False:
        count += 1


def flagged_count(email: dict) -> int:
    count = 0
    if is_valid(email) == False:
        count += 1
    if is_disposable(email) == False:
        count += 1
    if is_timed_out(email) == False:
        count += 1
    if catch_all_emails(email) == False:
        count += 1
    if leaked_emails(email) == False:
        count += 1 """
