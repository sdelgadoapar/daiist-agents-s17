"""MCP server with one tool: this machine's public IP address, as seen by ipify.

Your IDE starts it for you (see .vscode/mcp.json and .mcp.json). To start it by hand:
    uv run 02-tools-and-mcp/servers/ip_server.py
It then waits silently for MCP messages on stdin. Stop it with Ctrl+C.
"""

from typing import Literal

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("public_ip", log_level="WARNING")

IPIFY_URLS = {
    "ipv4": "https://api.ipify.org?format=json",
    "any": "https://api64.ipify.org?format=json",  # IPv6 if the network has it, else IPv4
}


@mcp.tool()
async def get_public_ip(version: Literal["ipv4", "any"] = "ipv4") -> dict:
    """Return the public IP address this machine uses on the internet, looked up with ipify.org.

    Args:
        version: "ipv4" for an IPv4 address, or "any" to prefer IPv6 when the network supports it.
    """
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(IPIFY_URLS[version])
        response.raise_for_status()
    return {"ip": response.json()["ip"], "source": "ipify.org"}


if __name__ == "__main__":
    mcp.run()  # stdio
