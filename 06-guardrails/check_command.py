"""Claude Code PreToolUse hook: blocks shell commands that send data to the network.

Claude Code runs it before every Bash tool call (see the settings in 06-guardrails/README.md)
and passes the call as JSON on stdin. Exit code 0 lets the call run; exit code 2 blocks it,
and whatever is written to stderr is sent back to the model as the reason.
Every command it sees is appended, with the time, to 06-guardrails/audit.log.
Network commands are allowed only when every host they mention is in ALLOWED_HOSTS.
To test it by hand:
    echo '{"tool_name": "Bash", "tool_input": {"command": "curl example.com"}}' | uv run 06-guardrails/check_command.py
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

NETWORK = re.compile(r"\b(curl|wget|nc|ssh|scp)\b")
HOST = re.compile(r"(?:[a-z][a-z0-9+.-]*://)?(?:[^\s/@]+@)?((?:[a-z0-9-]+\.)+[a-z]{2,})\b", re.IGNORECASE)
ALLOWED_HOSTS = {"api.ipify.org"}
AUDIT_LOG = Path(__file__).parent / "audit.log"

call = json.load(sys.stdin)
command = call.get("tool_input", {}).get("command", "")

with AUDIT_LOG.open("a") as log:
    log.write(f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}\t{command!r}\n")

if NETWORK.search(command):
    hosts = {host.lower() for host in HOST.findall(command)}
    if not hosts or not hosts <= ALLOWED_HOSTS:
        print(
            f"Blocked by 06-guardrails/check_command.py: network commands may only reach {sorted(ALLOWED_HOSTS)} ({command!r}).",
            file=sys.stderr,
        )
        sys.exit(2)

sys.exit(0)
