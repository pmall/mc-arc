from abc import ABC, abstractmethod
from typing import Any
from string import Template
from mca.interfaces import Summarizer, Message
from mca.prompts import SUMMARIZER_PROMPT_TEMPLATE


class AbstractSummarizer(Summarizer, ABC):
    def __init__(
        self,
        model: str,
        client: Any,
        temperature: float = 0.2,
        max_output_tokens: int = 1000,
        max_messages: int = 10,
    ):
        self.model = model
        self.client = client
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens
        self.max_messages = max_messages
        self.template = Template(SUMMARIZER_PROMPT_TEMPLATE)

    def __call__(self, messages: list[Message]) -> str:
        if not messages:
            return "Produce a new message"

        buffer = messages[-self.max_messages :] if self.max_messages > 0 else []
        conversation = "\n".join([f"- {message}" for message in buffer])
        prompt = self.template.substitute(conversation=conversation)

        return self._generate_summary(prompt)

    @abstractmethod
    def _generate_summary(self, prompt: str) -> str:
        pass
