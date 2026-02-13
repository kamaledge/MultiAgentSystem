from pathlib import Path

from assistant.llm import FallbackLLM
from assistant.orchestrator import MultiAgentCodingAssistant
from assistant.profile import UserProfile, load_profile, save_profile


def test_profile_roundtrip(tmp_path: Path) -> None:
    path = tmp_path / "profile.json"
    profile = UserProfile(name="Ada")
    save_profile(path, profile)

    loaded = load_profile(path)
    assert loaded.name == "Ada"
    assert "python" in loaded.preferred_languages


def test_multi_agent_pipeline_produces_all_sections() -> None:
    assistant = MultiAgentCodingAssistant(llm=FallbackLLM())
    result = assistant.run(UserProfile(), "Create a CLI todo app")

    assert "Fallback model response" in result.plan
    assert "Fallback model response" in result.implementation
    assert "Fallback model response" in result.review
    assert "Fallback model response" in result.coaching
