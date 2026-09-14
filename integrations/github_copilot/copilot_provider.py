"""Provider interface for coding-assistant integrations.

FishyLLAMA deliberately uses an adapter boundary rather than bundling or
reimplementing proprietary GitHub Copilot internals.
"""

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class CodeContext:
    language: str
    code: str
    filename: str | None = None
    repository_context: str | None = None


class CodingProvider(Protocol):
    name: str

    async def complete(self, prompt: str, context: CodeContext) -> str: ...
    async def explain(self, code: str, context: CodeContext) -> str: ...
    async def review(self, diff: str, repository_context: str = "") -> str: ...
    async def generate_tests(self, code: str, context: CodeContext) -> str: ...


class CopilotAdapter:
    """Adapter placeholder for an approved Copilot integration.

    Keep authentication and requests inside this adapter so the Fishy Core
    remains provider-agnostic. Add an official GitHub-supported API/CLI
    transport here when credentials and endpoint requirements are configured.
    """

    name = "github-copilot"

    def __init__(self, enabled: bool = False):
        self.enabled = enabled

    async def complete(self, prompt: str, context: CodeContext) -> str:
        raise RuntimeError(
            "GitHub Copilot adapter is not configured. Configure an approved "
            "GitHub integration before enabling this provider."
        )

    async def explain(self, code: str, context: CodeContext) -> str:
        raise RuntimeError("GitHub Copilot adapter is not configured.")

    async def review(self, diff: str, repository_context: str = "") -> str:
        raise RuntimeError("GitHub Copilot adapter is not configured.")

    async def generate_tests(self, code: str, context: CodeContext) -> str:
        raise RuntimeError("GitHub Copilot adapter is not configured.")
