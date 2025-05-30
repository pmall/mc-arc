from typing import AsyncGenerator, Callable, Union

Selector = Callable[[list[str], list[tuple[str, str]]], str]

Summarizer = Callable[[list[tuple[str, str]]], str]

AgentResponse = Union[str, AsyncGenerator[str, None]]

AgentAdapter = Callable[[str], AgentResponse]
