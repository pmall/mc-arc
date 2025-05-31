from enum import Enum
from string import Template
from google import genai
from google.genai import types
from mca.prompts import SELECTOR_PROMPT_TEMPLATE
from mca.interfaces import Message, Selector


class GeminiParticipantSelector(Selector):
    def __init__(self, model: str, client: genai.Client, max_messages: int = 10):
        self.model = model
        self.client = client
        self.max_messages = max_messages
        self.template = Template(SELECTOR_PROMPT_TEMPLATE)

    def __call__(self, participants: list[str], messages: list[Message]) -> str:
        OptionalParticipantEnum = Enum("ParticipantEnum", {p: p for p in participants})

        buffer = messages[-self.max_messages :] if self.max_messages > 0 else []

        participants = ", ".join(participants)
        conversation = "\n".join([f"- {message}" for message in buffer])

        prompt = self.template.substitute(
            participants=participants, conversation=conversation
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=OptionalParticipantEnum,
            ),
        )

        return response.text
