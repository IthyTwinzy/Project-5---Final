from dotenv import dotenv_values

IPQS_API_KEY = dotenv_values().get("IPQS_API_KEY")
IPQS_URL = "https://www.ipqualityscore.com/api/"

# Stores configuration presets for flask
class MockedDataDebugConfig:
    DEBUG: str = True
    FAKE_DATA: str = True

class IPQSDebugConfig:
    DEBUG: str = True
    FAKE_DATA: str = False