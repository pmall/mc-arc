from abc import ABC, abstractmethod
from typing import Any
from string import Template
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
        self.template = Template(REPORTER_PROMPT_TEMPLATE)

    def __call__(self, participant: str, messages: list[Message]) -> str:
        if not messages:
            return "Produce a new message"

        buffer = messages[-self.max_messages :] if self.max_messages > 0 else []
        messages_str = "\n".join([f"- {message}" for message in buffer])
        prompt = self.template.substitute(
            participant=participant, messages=messages_str
        )

        return self._generate_report(prompt, max_output_tokens=len(messages_str))

    @abstractmethod
    def _generate_report(self, prompt: str, max_output_tokens: int) -> str:
        pass
