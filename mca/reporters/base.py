from abc import ABC, abstractmethod
from typing import Any
from mca.interfaces import Message
from mca.prompts import REPORTER_PROMPT_TEMPLATE


class AbstractReporter(ABC):
    def __init__(
        self,
        model: str,
        client: Any,
        temperature: float = 0.2,
        max_messages: int = 100,
    ):
        self.model = model
        self.client = client
        self.temperature = temperature
        self.max_messages = max_messages
        self.template = REPORTER_PROMPT_TEMPLATE

    def __call__(self, participant: str, messages: list[Message]) -> str:
        if not messages:
            return ""

        last_messages = messages[-self.max_messages :] if self.max_messages > 0 else []

        prompt = self.template(participant, last_messages)

        max_output_tokens = sum([len(str(m)) for m in last_messages])

        return self._generate_report(prompt, max_output_tokens=max_output_tokens)

    @abstractmethod
    def _generate_report(self, prompt: str, max_output_tokens: int) -> str:
        pass
