from mcp.server.fastmcp import FastMCP
import sys
from testReturn import testJsonReturn

from user_prompts import email_threat_checker

mcp = FastMCP("Email and Phishing Detection Server")
mcp.add_tool(email_threat_checker)
mcp.add_tool(testJsonReturn)
if __name__ == "__main__":
    try:
        sys.stderr.write("server started\n")
        mcp.run()
    except KeyboardInterrupt:
        sys.stderr.write("server stopped\n")