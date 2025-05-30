from pydantic_ai import Agent
from mca.interfaces import AgentAdapter, AgentResponse


class PydanticAiAdapter(AgentAdapter):
    def __init__(self, pydantic_agent: Agent):
        self.agent = pydantic_agent

    def __call__(self, message_summary: str) -> AgentResponse:
        if hasattr(self.agent, "run_stream"):
            return self._stream_response(message_summary)
        else:
            result = self.agent.run(message_summary)
            return result.data

    async def _stream_response(self, message_summary: str):
        async with self.agent.run_stream(message_summary) as result:
            async for chunk in result.stream_text():
                yield chunk
