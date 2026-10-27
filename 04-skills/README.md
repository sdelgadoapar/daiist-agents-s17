# Step 4. Skills

## What a skill is

A skill is a folder containing a `SKILL.md` file with instructions that teach an agent how to do one kind of task, optionally with scripts, templates or reference documents next to it. Where a tool gives the agent a new ability, a skill gives it know-how: how your team writes release notes, how to fill in a slide template, which checks to run before a deployment.

Anthropic introduced skills in October 2025 and published the format as an open standard ([agentskills.io](https://agentskills.io)), which other agents such as GitHub Copilot, OpenAI Codex and Gemini CLI also read.

## Progressive disclosure

The difference between a skill and an instruction file (step 3) is when its content enters the context. A skill is loaded in three levels:

1. **Always:** only the `name` and `description` from the top of `SKILL.md`. A few dozen tokens per skill.
2. **When a task matches the description:** the agent reads the rest of `SKILL.md`.
3. **Only if the instructions point to them:** the extra files in the folder.

So an agent can have dozens of skills installed at almost no cost, and the description decides whether a skill is ever used: like a tool's description, it is the only thing the model matches the request against.

## This repository's skill

[.claude/skills/meeting-time-planner/](../.claude/skills/meeting-time-planner/) has two files:

- [SKILL.md](../.claude/skills/meeting-time-planner/SKILL.md): the steps for finding a meeting slot across time zones. It uses the `get_current_time` tool from step 2, so a skill can build on tools.
- [office-hours.md](../.claude/skills/meeting-time-planner/office-hours.md): each office's working hours. The agent reads it only when step 1 of the skill tells it to (level 3).

```markdown
---
name: meeting-time-planner
description: Find a meeting time that works for people in different cities. Use when the user wants to schedule a call or meeting across time zones.
---

# Meeting time planner

1. Read office-hours.md to get each office's working hours. ...
2. Call `get_current_time` once for each city's time zone. ...
```

The folder `.claude/skills/` is read by both Claude Code and VS Code. VS Code also looks in `.github/skills/` and `.agents/skills/`. The `name` must match the folder name and use only lowercase letters, numbers and hyphens.

## Try it

1. Start a new chat and ask *"Find a 1-hour slot tomorrow for a call between Madrid, New York and Tokyo."* Watch the chat: the agent should read `SKILL.md`, then `office-hours.md`, then call `get_current_time` three times.
2. Check the answer against the skill: does it respect the Madrid lunch break and Tokyo's later start? Without the skill, the agent could not know either.
3. Ask *"What time is it in Tokyo?"*. The skill should not load, because the question does not match its description.
4. In VS Code, type `/` in the chat: skills also appear as slash commands, so you can run one by name.

## Exercises

1. Change the description to something vague, such as "Helps with time." Start a new chat and repeat question 1. Does the skill still load?
2. Add a Dubai participant to question 1. Does the agent apply Dubai's shorter Friday?
3. Write a skill of your own for a task you repeat, for example "turn meeting notes into a summary email" with a template file next to `SKILL.md`.

## Further reading

- Agent Skills format: <https://agentskills.io>
- Skills in VS Code: <https://code.visualstudio.com/docs/copilot/customization/agent-skills>
- Skills in Claude Code: <https://docs.claude.com/en/docs/claude-code/skills>
