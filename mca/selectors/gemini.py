from enum import Enum
from string import Template
from google import genai
from google.genai import types

PROMPT_TEMPLATE = """
You are managing a multi-character conversation. Based on the recent messages and the current situation, choose the next participant who should speak. Consider who has the most reason to respond, take initiative, clarify something, or move the discussion forward.

Available participants:
$participants

Recent messages:
$conversation

Rules:
- Always select exactly one participant from the list.
- Choose the one whose voice is most needed right now.
- Do not explain your choice or provide any commentary.

Return the name of the selected participant only, exactly as it appears in the list.
 """.strip()


class GeminiParticipantSelector:
    def __init__(self, model: str, client: genai.Client):
        self.model = model
        self.client = client

    def __call__(self, participants: list[str], messages: list[tuple[str, str]]) -> str:
        OptionalParticipantEnum = Enum("ParticipantEnum", {p: p for p in participants})

        participants = ", ".join(participants)
        conversation = "\n".join([f"{role}: {message}" for role, message in messages])

        prompt = Template(PROMPT_TEMPLATE).substitute(
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
