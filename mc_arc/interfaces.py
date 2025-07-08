from dataclasses import dataclass
from typing import AsyncGenerator, Callable, Union


@dataclass
class Message:
    name: str
    content: str

    def __str__(self):
        return f"{self.name}: {self.content}"


Selector = Callable[[list[str], list[Message]], str]

Reporter = Callable[[str, list[Message]], str]

# a non cumulative stream of text is expected
AgentResponse = AsyncGenerator[str, None]

AgentAdapter = Callable[[str], AgentResponse]
