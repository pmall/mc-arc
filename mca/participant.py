from typing import AsyncGenerator
from mca.interfaces import Message, Summarizer, AgentAdapter, AgentResponse


class Participant:
    def __init__(self, name: str, agent: AgentAdapter, summarizer: Summarizer):
        self.name = name
        self.agent = agent
        self.summarizer = summarizer
        self.buffer: list[Message] = []

    def receive_message(self, message: Message):
        self.buffer.append(message)

    def reply(self, cumulative: bool = False) -> AsyncGenerator[str, None]:
        summary = self.summarizer(self.buffer)

        response = self.agent(summary)

        self.buffer.clear()

        return StreamingResponse(self.name, response, cumulative)

    async def _string_wrapper(self, response: str) -> AsyncGenerator[str, None]:
        yield response


class StreamingResponse:
    def __init__(self, name: str, response: AgentResponse, cumulative: bool = False):
        self.name = name
        self.response = response
        self.cumulative = cumulative
        self.full_response = ""
        self._generator = None

    async def __aenter__(self):
        self._generator = self._create_chunk_generator()
        return self._generator

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        # Ensure the response is fully consumed
        if self._generator:
            try:
                async for _ in self._generator:
                    pass
            except StopAsyncIteration:
                pass

    async def _create_chunk_generator(self) -> AsyncGenerator[tuple[str, str], None]:
        if isinstance(self.response, str):
            # Handle string case - single chunk
            self.full_response = self.response
            yield (self.name, self.response)
        else:
            # Handle async generator case
            async for chunk in self.response:
                self.full_response += chunk
                chunk_to_send = self.full_response if self.cumulative else chunk
                yield (self.name, chunk_to_send)

    def get_full_response(self) -> str:
        return self.full_response
