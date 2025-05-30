from google import genai
from google.genai import types
from enum import Enum


class GeminiParticipantSelector:
    def __init__(self, model: str, client: genai.Client):
        self.model = model
        self.client = client

    def __call__(self, participants: list[str], messages: list[tuple[str, str]]) -> str:
        OptionalParticipantEnum = Enum("ParticipantEnum", {p: p for p in participants})

        conversation = "\n".join([f"{role}: {message}" for role, message in messages])

        prompt = (
            f"Given the following conversation history and a list of available participants, "
            f"select the name of the next participant who should speak. "
            f"You MUST choose one of the following participants: {', '.join(participants)}.\n"
            f"Do NOT provide any additional text or explanation, just the participant's name.\n\n"
            f"Conversation History:\n{conversation}\n\n"
            f"Available Participants: {', '.join(participants)}\n"
            f"Next Participant:"
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
