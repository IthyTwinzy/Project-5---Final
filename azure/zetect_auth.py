import os
import json
import msal

CLIENT_ID = "0c60d083-5388-427f-85ce-de767ac8b818"
AUTHORITY = "https://login.microsoftonline.com/common"
SCOPES = ["Mail.Read"]

CACHE_FILE = "token_cache.bin"


def load_cache():
    """Load saved Microsoft login token cache if it exists."""
    cache = msal.SerializableTokenCache()

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache.deserialize(f.read())

    return cache


def save_cache(cache):
    """Save Microsoft login token cache after authentication."""
    if cache.has_state_changed:
        with open(CACHE_FILE, "w") as f:
            f.write(cache.serialize())


def get_token():
    """Get a Microsoft Graph access token using cached login or device login."""
    cache = load_cache()

    app = msal.PublicClientApplication(
        CLIENT_ID,
        authority=AUTHORITY,
        token_cache=cache
    )

    accounts = app.get_accounts()
    result = None

   
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

   
    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)

        if "user_code" not in flow:
            raise ValueError(f"Device flow creation failed: {json.dumps(flow, indent=2)}")

        print(flow["message"])
        result = app.acquire_token_by_device_flow(flow)

    save_cache(cache)

    if "access_token" in result:
        return result["access_token"]

    raise RuntimeError(f"Token acquisition failed: {result}")


if __name__ == "__main__":
    token = get_token()
    print("Access token acquired.")
