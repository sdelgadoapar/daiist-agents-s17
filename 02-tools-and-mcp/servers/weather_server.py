"""MCP server with one tool: the current weather in a city, from Open-Meteo (free, no API key).

Your IDE starts it for you (see .vscode/mcp.json and .mcp.json). To start it by hand:
    uv run 02-tools-and-mcp/servers/weather_server.py
It then waits silently for MCP messages on stdin. Stop it with Ctrl+C.
"""

import httpx
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("weather", log_level="WARNING")

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


@mcp.tool()
async def get_current_weather(city: str) -> dict:
    """Return the current temperature, wind speed and precipitation in a city, looked up with open-meteo.com.

    Args:
        city: City name in English, for example "Madrid" or "New York".
    """
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(GEOCODING_URL, params={"name": city, "count": 1})
        response.raise_for_status()
        matches = response.json().get("results")
        if not matches:
            raise ValueError(f"Unknown city {city!r}. Try the English name of a larger city nearby.")
        place = matches[0]
        response = await client.get(
            FORECAST_URL,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,wind_speed_10m,precipitation",
                "timezone": "auto",
            },
        )
        response.raise_for_status()
    current = response.json()["current"]
    return {
        "city": place["name"],
        "country": place.get("country"),
        "local_time": current["time"],
        "temperature_c": current["temperature_2m"],
        "wind_speed_kmh": current["wind_speed_10m"],
        "precipitation_mm": current["precipitation"],
        "source": "open-meteo.com",
    }


if __name__ == "__main__":
    mcp.run()  # stdio
