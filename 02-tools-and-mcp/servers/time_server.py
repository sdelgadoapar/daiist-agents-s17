"""MCP server with two tools: the current date and time in any time zone, and time zone conversion.

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


@mcp.tool()
def convert_time(time: str, from_timezone: str, to_timezone: str) -> dict:
    """Convert a time of day (today's date in from_timezone) from one time zone to another.

    Args:
        time: Time of day in 24-hour format, for example "15:00".
        from_timezone: IANA time zone name the time is in, for example "Europe/Madrid".
        to_timezone: IANA time zone name to convert to, for example "America/New_York".
    """
    zones = {}
    for name in (from_timezone, to_timezone):
        try:
            zones[name] = ZoneInfo(name)
        except ZoneInfoNotFoundError:
            raise ValueError(f"Unknown time zone {name!r}. Use an IANA name such as 'Europe/Madrid'.")
    try:
        hour, minute = (int(part) for part in time.split(":"))
        source = datetime.now(zones[from_timezone]).replace(hour=hour, minute=minute, second=0, microsecond=0)
    except ValueError:
        raise ValueError(f"Invalid time {time!r}. Use 24-hour HH:MM, for example '15:00'.")
    target = source.astimezone(zones[to_timezone])
    return {
        "from": {"timezone": from_timezone, "iso": source.isoformat(timespec="minutes")},
        "to": {"timezone": to_timezone, "iso": target.isoformat(timespec="minutes"), "weekday": target.strftime("%A")},
    }


if __name__ == "__main__":
    mcp.run()  # stdio
