from __future__ import annotations

from dataclasses import dataclass

from .agents import CoachAgent, CoderAgent, PlannerAgent, ReviewerAgent
from .llm import LLMClient
from .profile import UserProfile


@dataclass
class AssistantResult:
    plan: str
    implementation: str
    review: str
    coaching: str


class MultiAgentCodingAssistant:
    def __init__(self, llm: LLMClient) -> None:
        self.planner = PlannerAgent(
            name="PlannerAgent",
            mission="Create a clear implementation plan with milestones and tests.",
            llm=llm,
        )
        self.coder = CoderAgent(
            name="CoderAgent",
            mission="Produce a high-quality implementation draft based on the plan.",
            llm=llm,
        )
        self.reviewer = ReviewerAgent(
            name="ReviewerAgent",
            mission="Review for correctness, security, and maintainability. Suggest improvements.",
            llm=llm,
        )
        self.coach = CoachAgent(
            name="CoachAgent",
            mission="Explain next steps and learning points in the user's preferred tone.",
            llm=llm,
        )

    def run(self, profile: UserProfile, task: str) -> AssistantResult:
        plan = self.planner.run(profile=profile, task=task)
        implementation = self.coder.run(profile=profile, task=task, context=plan)
        review = self.reviewer.run(profile=profile, task=task, context=f"PLAN:\n{plan}\n\nCODE:\n{implementation}")
        coaching = self.coach.run(
            profile=profile,
            task=task,
            context=f"PLAN:\n{plan}\n\nIMPLEMENTATION:\n{implementation}\n\nREVIEW:\n{review}",
        )
        return AssistantResult(plan=plan, implementation=implementation, review=review, coaching=coaching)
