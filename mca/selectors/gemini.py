from enum import Enum
from string import Template
from google import genai
from google.genai import types
from mca.prompts import SELECTOR_PROMPT_TEMPLATE


class GeminiParticipantSelector:
    def __init__(self, model: str, client: genai.Client):
        self.model = model
        self.client = client
        self.template = Template(SELECTOR_PROMPT_TEMPLATE)

    def __call__(self, participants: list[str], messages: list[tuple[str, str]]) -> str:
        OptionalParticipantEnum = Enum("ParticipantEnum", {p: p for p in participants})

        participants = ", ".join(participants)
        conversation = "\n".join([f"{role}: {message}" for role, message in messages])

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
