from typing import AsyncGenerator, Callable, Union


class NarratorMessage:
    def __init__(self, content):
        self.name = None
        self.content = content

    def __str__(self):
        return f"{self.content}"

    def __repr__(self):
        return f"NarratorMessage(name='{self.name}', age={self.content})"


class ParticipantMessage:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self):
        return f"{self.name}: {self.content}"

    def __repr__(self):
        return f"ParticipantMessage(name='{self.name}', age={self.content})"


Message = Union[NarratorMessage, ParticipantMessage]

Selector = Callable[[list[str], list[Message]], str]

Summarizer = Callable[[list[Message]], str]

# a non cumulative stream of text is expected
AgentResponse = Union[str, AsyncGenerator[str, None]]

AgentAdapter = Callable[[str], AgentResponse]
