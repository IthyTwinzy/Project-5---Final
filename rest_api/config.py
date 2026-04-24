from dotenv import dotenv_values

IPQS_API_KEY = dotenv_values().get("IPQS_API_KEY")
IPQS_URL = "https://www.ipqualityscore.com/api/"