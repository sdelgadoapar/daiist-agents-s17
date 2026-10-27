"""Talk to our MCP servers directly, with no language model involved.

This is what every MCP host (VS Code, Claude Code, Cursor, Gemini CLI)
does under the hood: start the server, ask for its tools, call one.

    uv run 02-tools-and-mcp/list_and_call.py
"""

import asyncio
import json
import textwrap

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVERS = {
    "time": ("02-tools-and-mcp/servers/time_server.py", "get_current_time", {"timezone": "Europe/Madrid"}),
    "public_ip": ("02-tools-and-mcp/servers/ip_server.py", "get_public_ip", {}),
}


async def inspect_server(script, tool_name, arguments):
    # Launch the server as a subprocess and talk to it over stdin/stdout.
    params = StdioServerParameters(command="uv", args=["run", script])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            info = await session.initialize()
            print(f"Connected to server {info.server_info.name!r}")

            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  tool {tool.name}: {tool.description.splitlines()[0]}")
                print("    input schema:")
                print(textwrap.indent(json.dumps(tool.input_schema, indent=2), "      "))

            result = await session.call_tool(tool_name, arguments)
            print(f"  call {tool_name}({arguments}) ->")
            print(textwrap.indent(result.content[0].text, "    "))
            print()


async def main():
    for script, tool_name, arguments in SERVERS.values():
        await inspect_server(script, tool_name, arguments)


if __name__ == "__main__":
    asyncio.run(main())
