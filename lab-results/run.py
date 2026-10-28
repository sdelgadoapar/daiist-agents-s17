"""Run one fresh Claude Code session and summarise its tool calls and final answer.

usage: uv run lab-results/run.py NAME PROMPT [cwd=DIR] [allow=TOOL] [extra claude args...]
The raw stream is saved next to this file in runs/NAME.jsonl (not committed)."""
import json, subprocess, sys, pathlib
name, prompt, extra = sys.argv[1], sys.argv[2], sys.argv[3:]
out = pathlib.Path(__file__).parent / "runs" / f"{name}.jsonl"
out.parent.mkdir(exist_ok=True)
allowed = "Read Glob Grep Skill Agent mcp__time__get_current_time mcp__time__convert_time mcp__public_ip__get_public_ip mcp__weather__get_current_weather"
cwd = None
if extra and extra[0].startswith("cwd="): cwd, extra = extra[0][4:], extra[1:]
allowed += "".join(" " + a[6:] for a in extra if a.startswith("allow="))
extra = [a for a in extra if not a.startswith("allow=")]
cmd = ["claude", "-p", prompt, "--output-format", "stream-json", "--verbose", "--allowedTools", allowed, "--permission-mode", "default", *extra]
p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=cwd)
out.write_text(p.stdout + p.stderr)
lines = [f"### {name}", f"prompt: {prompt}", f"args: {' '.join(extra)}"]
denied = []
for line in p.stdout.splitlines():
    try: ev = json.loads(line)
    except ValueError: continue
    if ev.get("type") == "assistant":
        for c in ev["message"]["content"]:
            if c.get("type") == "tool_use":
                who = "subagent" if ev.get("parent_tool_use_id") else "main"
                lines.append(f"  [{who}] {c['name']}({json.dumps(c['input'])[:200]})")
    if ev.get("type") == "result":
        denied = ev.get("permission_denials", [])
        lines.append(f"  denied: {[d.get('tool_name') for d in denied]}")
        u = ev.get("usage", {})
        lines.append(f"  turns={ev.get('num_turns')} cost=${ev.get('total_cost_usd', 0):.3f} main-context input tokens={u.get('input_tokens',0)+u.get('cache_read_input_tokens',0)+u.get('cache_creation_input_tokens',0)}")
        lines.append("  answer:\n" + "\n".join("    " + l for l in str(ev.get("result")).splitlines()))
print("\n".join(lines))
