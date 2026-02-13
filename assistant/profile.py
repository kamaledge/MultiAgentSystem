from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class UserProfile:
    name: str = "Your Name"
    experience_level: str = "intermediate"
    preferred_languages: list[str] = field(default_factory=lambda: ["python"])
    preferred_frameworks: list[str] = field(default_factory=lambda: ["fastapi"])
    tone: str = "mentor"
    priorities: list[str] = field(default_factory=lambda: ["readability", "security", "testability"])
    output_preferences: list[str] = field(default_factory=lambda: ["test-first", "checklist"])

    def to_prompt_block(self) -> str:
        return (
            f"User profile:\n"
            f"- Name: {self.name}\n"
            f"- Experience: {self.experience_level}\n"
            f"- Languages: {', '.join(self.preferred_languages)}\n"
            f"- Frameworks: {', '.join(self.preferred_frameworks)}\n"
            f"- Tone: {self.tone}\n"
            f"- Priorities: {', '.join(self.priorities)}\n"
            f"- Output preferences: {', '.join(self.output_preferences)}"
        )


def load_profile(path: Path) -> UserProfile:
    if not path.exists():
        raise FileNotFoundError(f"Profile not found: {path}")
    data: dict[str, Any] = json.loads(path.read_text())
    return UserProfile(**data)


def save_profile(path: Path, profile: UserProfile) -> None:
    path.write_text(json.dumps(asdict(profile), indent=2) + "\n")
