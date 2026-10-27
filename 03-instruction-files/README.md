# Step 3. Instruction files

## What they are

An instruction file is a Markdown file that the host adds to the agent's context at the start of every session. It holds standing rules that would otherwise have to be repeated in every prompt: the project's conventions, how to run its tests, what never to do. Some agents call this **memory**.

Each host looks for its own file name at the root of the open folder:

| File | Read by |
|---|---|
| `AGENTS.md` | GitHub Copilot in VS Code (on by default, setting `chat.useAgentsMdFile`), OpenAI Codex, Cursor and others. It is the closest thing to a shared standard. |
| `CLAUDE.md` | Claude Code. VS Code can read it too (setting `chat.useClaudeMdFile`). |
| `GEMINI.md` | Gemini CLI. |
| `.github/copilot-instructions.md` | GitHub Copilot. |

To avoid keeping the same rules in several files, this repository writes them once in [AGENTS.md](../AGENTS.md), and [CLAUDE.md](../CLAUDE.md) contains a single line, `@AGENTS.md`, which tells Claude Code to import that file.

The whole file goes into the context every time, so keep it short: a long instruction file costs tokens on every request and dilutes the rules that matter. Instructions that apply only to some tasks belong in a skill (step 4).

## This repository's file

[AGENTS.md](../AGENTS.md) contains four rules. Two of them have effects you can see:

- Times must be written in 24-hour format followed by the city, for example "14:05 Madrid".
- Before answering, the agent must list each tool it called and its arguments.

## Try it

1. Start a new chat (instruction files are read when a session starts) and ask *"What time is it in New York?"*. Check that the answer follows both rules.
2. Turn the file off and repeat: in VS Code, untick `chat.useAgentsMdFile` in Settings; in Claude Code, rename `CLAUDE.md` to `CLAUDE.md.off` and start a new session. What changes? Undo it afterwards.
3. Ask the agent *"Which instructions were you given for this repository?"*. The rules are ordinary text in its context, so it can quote them.

## Exercises

1. Add a rule of your own, for example "Always answer in Spanish" or "End every answer with the UTC time". Check that a new session follows it.
2. Add two rules that contradict each other ("Always use 24-hour format" and "Always use AM/PM"). What does the agent do? What does this tell you about how instruction files work?
