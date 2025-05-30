from typing import AsyncGenerator
from mca.interfaces import Summarizer, AgentAdapter


class Participant:
    def __init__(self, name: str, agent: AgentAdapter, summarizer: Summarizer):
        self.name = name
        self.agent = agent
        self.summarizer = summarizer
        self.buffer: list[tuple[str, str]] = []

    def receive_message(self, sender_name: str, message: str):
        self.buffer.append((sender_name, message))

    def reply(self) -> AsyncGenerator[str, None]:
        summary = self.summarizer(self.buffer)

        response = self.agent(summary)

        self.buffer.clear()

        return response

    async def _string_wrapper(self, response: str) -> AsyncGenerator[str, None]:
        yield response
