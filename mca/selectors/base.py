from abc import ABC, abstractmethod
from typing import Any
from mca.interfaces import Message
from mca.prompts import SELECTOR_PROMPT_TEMPLATE


class AbstractParticipantSelector(ABC):
    def __init__(self, model: str, client: Any, max_messages: int = 10):
        self.model = model
        self.client = client
        self.max_messages = max_messages
        self.template = SELECTOR_PROMPT_TEMPLATE

    def __call__(self, participants: list[str], messages: list[Message]) -> str:
        last_messages = messages[-self.max_messages :] if self.max_messages > 0 else []

        prompt = self.template(participants, last_messages)

        return self._select_participant(participants, prompt)

    @abstractmethod
    def _select_participant(self, participants: list[str], prompt: str) -> str:
        pass
