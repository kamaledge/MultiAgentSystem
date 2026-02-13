from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class LLMClient:
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError


class FallbackLLM(LLMClient):
    """Deterministic local fallback to keep the workflow usable without API keys."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        seed = user_prompt[:200].strip().replace("\n", " ")
        return (
            "[Fallback model response]\n"
            f"System goal: {system_prompt[:120]}...\n"
            "Actionable output:\n"
            f"- Interpreted task: {seed}\n"
            "- Suggested approach: break work into small tested increments.\n"
            "- Key risks: edge cases, error handling, and missing tests.\n"
        )


class OpenAICompatibleLLM(LLMClient):
    def __init__(self, api_key: str, base_url: str, model: str) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url=f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(f"LLM request failed: {exc}") from exc

        return data["choices"][0]["message"]["content"]


def build_llm_from_env() -> LLMClient:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return FallbackLLM()

    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return OpenAICompatibleLLM(api_key=api_key, base_url=base_url, model=model)
