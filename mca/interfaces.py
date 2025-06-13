from dataclasses import dataclass
from typing import AsyncGenerator, Callable, Literal


@dataclass
class Message:
    name: str
    content: str

    def __str__(self):
        return f"{self.name}: {self.content}"


ModifierType = Literal[
    "narrator_event",
    "internal_monologue",
]


@dataclass
class ContextModifier:
    type: ModifierType

    content: str

    def __str__(self):
        return f"{self.content}"


Selector = Callable[[list[str], list[Message]], str]

Reporter = Callable[[str, list[Message]], str]

# a non cumulative stream of text is expected
AgentResponse = AsyncGenerator[str, None]

AgentAdapter = Callable[[str], AgentResponse]
