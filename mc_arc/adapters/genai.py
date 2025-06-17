from google import genai
from google.genai import types
from typing import Optional
from mc_arc.interfaces import AgentResponse


class GenaiAdapter:
    def __init__(
        self, model: str, system_prompt: str, api_key: Optional[str] = None, tools=None
    ):
        client = genai.Client(api_key=api_key)

        self.chat = client.aio.chats.create(
            model=model,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=tools or [],
            ),
        )

    def __call__(self, message_summary: str) -> AgentResponse:
        return self._stream_response(message_summary)

    async def _stream_response(self, message_summary: str):
        stream = await self.chat.send_message_stream(message_summary)

        async for chunk in stream:
            yield chunk.text or ""
