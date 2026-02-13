from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .llm import build_llm_from_env
from .orchestrator import MultiAgentCodingAssistant
from .profile import UserProfile, load_profile, save_profile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Personalized multi-agent AI-first coding assistant")
    parser.add_argument("command", choices=["init-profile", "run"])
    parser.add_argument("--profile", default="profile.json", help="Path to profile JSON")
    parser.add_argument("--task", help="Coding task to solve")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    return parser


def cmd_init_profile(profile_path: Path) -> None:
    if profile_path.exists():
        print(f"Profile already exists: {profile_path}")
        return
    save_profile(profile_path, UserProfile())
    print(f"Created profile at {profile_path}")


def cmd_run(profile_path: Path, task: str, as_json: bool) -> None:
    profile = load_profile(profile_path)
    llm = build_llm_from_env()
    assistant = MultiAgentCodingAssistant(llm=llm)
    result = assistant.run(profile=profile, task=task)

    if as_json:
        print(json.dumps(asdict(result), indent=2))
        return

    print("\n=== PLAN ===\n")
    print(result.plan)
    print("\n=== IMPLEMENTATION ===\n")
    print(result.implementation)
    print("\n=== REVIEW ===\n")
    print(result.review)
    print("\n=== COACHING ===\n")
    print(result.coaching)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    profile_path = Path(args.profile)

    if args.command == "init-profile":
        cmd_init_profile(profile_path)
        return

    if not args.task:
        raise SystemExit("--task is required when command is 'run'")
    cmd_run(profile_path=profile_path, task=args.task, as_json=args.json)


if __name__ == "__main__":
    main()
