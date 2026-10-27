"""MCP server with one tool: the current date and time in any time zone.

Your IDE starts it for you (see .vscode/mcp.json and .mcp.json). To start it by hand:
    uv run 02-tools-and-mcp/servers/time_server.py
It then waits silently for MCP messages on stdin. Stop it with Ctrl+C.
"""

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from mcp.server.mcpserver import MCPServer

mcp = MCPServer("time", log_level="WARNING")


@mcp.tool()
def get_current_time(timezone: str = "UTC") -> dict:
    """Return the current date and time of this machine's clock in the given time zone.

    Args:
        timezone: IANA time zone name, for example "Europe/Madrid" or "America/New_York".
    """
    try:
        now = datetime.now(ZoneInfo(timezone))
    except ZoneInfoNotFoundError:
        raise ValueError(f"Unknown time zone {timezone!r}. Use an IANA name such as 'Europe/Madrid'.")
    return {
        "timezone": timezone,
        "iso": now.isoformat(timespec="seconds"),
        "weekday": now.strftime("%A"),
        "utc_offset": now.strftime("%z"),
    }


if __name__ == "__main__":
    mcp.run()  # stdio
