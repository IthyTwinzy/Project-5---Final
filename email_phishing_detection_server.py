from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("Email and Phishing Detection Server")


if __name__ == "__main__":
    try:
        sys.stderr.write("server started\n")
        mcp.run()
    except KeyboardInterrupt:
        sys.stderr.write("server stopped\n")