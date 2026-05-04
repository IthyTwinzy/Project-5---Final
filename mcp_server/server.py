from azure.zetect_detect import get_emails_and_analysis

from mcp.server.fastmcp import FastMCP
import requests
import sys

SERVER_ADDRESS = "http://127.0.0.1:5000/"

mcp = FastMCP("Email and Phishing Detection Server")

@mcp.tool()
def get_recent_emails() -> dict:
    """Fetches recent emails, checks if they seem like scam, and return a dict with the emails and scam analysis."""
    return get_emails_and_analysis()

@mcp.tool()
def email_address_threat_checker(email_address: str) -> dict:
    "Returns data indicating if a specified email address is likely to be malicious"
    return requests.get(f"{SERVER_ADDRESS}check_email/{email_address}").json()

if __name__ == "__main__":
    try:
        sys.stderr.write("server started\n")
        mcp.run()
    except KeyboardInterrupt:
        sys.stderr.write("server stopped\n")