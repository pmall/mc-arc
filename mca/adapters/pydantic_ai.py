from pydantic_ai import Agent
from mca.interfaces import AgentResponse


class PydanticAiAdapter:
    def __init__(self, agent: Agent):
        self.agent = agent
        self.message_history = []

    def __call__(self, message_summary: str) -> AgentResponse:
        return self._stream_response(message_summary)

    async def _stream_response(self, message_summary: str):
        response = self.agent.run_stream(
            message_summary, message_history=self.message_history
        )

        offset = 0
        async with response as result:
            async for chunk in result.stream():
                yield chunk[offset:]
                offset = len(chunk)
            self.message_history = result.all_messages()
