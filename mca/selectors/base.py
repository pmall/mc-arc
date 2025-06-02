from abc import ABC, abstractmethod
from typing import Any
from string import Template
from mca.interfaces import Selector
from mca.prompts import SELECTOR_PROMPT_TEMPLATE


class AbstractParticipantSelector(ABC, Selector):
    def __init__(self, model: str, client: Any, max_messages: int = 10):
        self.model = model
        self.client = client
        self.max_messages = max_messages
        self.template = Template(SELECTOR_PROMPT_TEMPLATE)

    def __call__(self, participants: list[str], messages: list[Any]) -> str:
        buffer = messages[-self.max_messages :] if self.max_messages > 0 else []
        participants_str = ", ".join(participants)
        conversation = "\n".join([f"- {message}" for message in buffer])

        prompt = self.template.substitute(
            participants=participants_str, conversation=conversation
        )

        return self._select_participant(participants, prompt)

    @abstractmethod
    def _select_participant(self, participants: list[str], prompt: str) -> str:
        pass
