# Personalized Multi-Agent AI-First Coding Assistant

A lightweight, extensible coding assistant that uses a **multi-agent pipeline** and a **personalization profile** so outputs match your style, stack, and priorities.

## What it does

- Uses multiple specialized agents:
  - **PlannerAgent**: turns your request into an actionable implementation plan.
  - **CoderAgent**: produces code or pseudocode from the plan.
  - **ReviewerAgent**: checks quality, tests, risks, and edge cases.
  - **CoachAgent**: explains trade-offs and next actions in your preferred style.
- Personalizes behavior using a `profile.json` file.
- Runs with either:
  - A real LLM via an OpenAI-compatible endpoint (`OPENAI_API_KEY`), or
  - A built-in deterministic fallback model (no API key required).

## Quick start

```bash
python -m assistant.main init-profile
python -m assistant.main run --task "Build a Flask endpoint with JWT auth"
```

## Personalization

Edit `profile.json` after initialization:

- `name`: your name
- `experience_level`: beginner/intermediate/advanced
- `preferred_languages`: e.g. `python`, `typescript`
- `preferred_frameworks`: e.g. `fastapi`, `react`
- `tone`: concise/mentor/deep-dive
- `priorities`: e.g. security, speed, readability, testability
- `output_preferences`: test-first, include-diagrams, include-checklists

## CLI commands

- `init-profile`: create a starter profile.
- `run --task <text>`: execute the full multi-agent workflow.
- `run --task <text> --json`: print machine-readable output.

## Environment variables

- `OPENAI_API_KEY`: enables real model calls.
- `OPENAI_BASE_URL`: optional, defaults to `https://api.openai.com/v1`.
- `OPENAI_MODEL`: optional, defaults to `gpt-4o-mini`.

## Why this is AI-first

The assistant is built around AI-native workflows rather than single-shot generation:

1. Decompose task
2. Generate implementation
3. Critique and harden
4. Coach based on user profile

This gives higher quality, more consistent outcomes than one-agent prompting.
