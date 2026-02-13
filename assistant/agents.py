from __future__ import annotations

from dataclasses import dataclass

from .llm import LLMClient
from .profile import UserProfile


@dataclass
class Agent:
    name: str
    mission: str
    llm: LLMClient

    def run(self, profile: UserProfile, task: str, context: str = "") -> str:
        system_prompt = (
            f"You are {self.name}. Mission: {self.mission}. "
            "Give concrete coding-focused output with steps, examples, and risks."
        )
        user_prompt = (
            f"{profile.to_prompt_block()}\n\n"
            f"Primary task:\n{task}\n\n"
            f"Prior context from previous agents:\n{context or '(none)'}"
        )
        return self.llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)


class PlannerAgent(Agent):
    pass


class CoderAgent(Agent):
    pass


class ReviewerAgent(Agent):
    pass


class CoachAgent(Agent):
    pass
