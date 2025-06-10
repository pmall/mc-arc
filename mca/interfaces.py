from dataclasses import dataclass
from typing import AsyncGenerator, Callable, Optional, Union, Literal


@dataclass
class Message:
    name: str
    content: str

    def __str__(self):
        return f"{self.name}: {self.content}"


@dataclass
class ContextModifier:
    type: Literal[
        "narrator_event",
        "internal_monologue",
    ]

    content: str

    def __str__(self):
        return f"{self.content}"


@dataclass
class TimelineItem:
    message: Message
    modifiers: list[ContextModifier]


Selector = Callable[[list[str], list[Message]], str]

Reporter = Callable[[str, list[Message]], Optional[str]]

# a non cumulative stream of text is expected
AgentResponse = Union[str, AsyncGenerator[str, None]]

AgentAdapter = Callable[[str], AgentResponse]
