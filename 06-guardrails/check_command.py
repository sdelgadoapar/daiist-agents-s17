"""Claude Code PreToolUse hook: blocks shell commands that send data to the network.

Claude Code runs it before every Bash tool call (see the settings in 06-guardrails/README.md)
and passes the call as JSON on stdin. Exit code 0 lets the call run; exit code 2 blocks it,
and whatever is written to stderr is sent back to the model as the reason.
To test it by hand:
    echo '{"tool_name": "Bash", "tool_input": {"command": "curl example.com"}}' | uv run 06-guardrails/check_command.py
"""

import json
import re
import sys

BLOCKED = re.compile(r"\b(curl|wget|nc|ssh|scp)\b")

call = json.load(sys.stdin)
command = call.get("tool_input", {}).get("command", "")

if BLOCKED.search(command):
    print(f"Blocked by 06-guardrails/check_command.py: network commands are not allowed ({command!r}).", file=sys.stderr)
    sys.exit(2)

sys.exit(0)
