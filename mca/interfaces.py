from typing import AsyncGenerator, Callable, Union

Selector = Callable[[list[str], list[tuple[str, str]]], str]

Summarizer = Callable[[list[tuple[str, str]]], str]

# a non cumulative stream of text is expected
AgentResponse = Union[str, AsyncGenerator[str, None]]

AgentAdapter = Callable[[str], AgentResponse]
