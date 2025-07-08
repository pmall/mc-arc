from enum import Enum
from google.genai import types
from .base import AbstractParticipantSelector


class GeminiParticipantSelector(AbstractParticipantSelector):
    def _select_participant(self, participants, prompt):
        OptionalParticipantEnum = Enum("ParticipantEnum", {p: p for p in participants})

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="text/x.enum",
                response_schema=OptionalParticipantEnum,
            ),
        )

        return response.text


def create_gemini_selector(
    model: str = "gemini-2.0-flash", api_key: str | None = None, max_messages: int = 10
):
    """Factory function that creates client and selector together."""
    try:
        from google import genai
    except ImportError:
        raise ImportError(
            "google-generativeai package not installed. Install with: pip install google-generativeai"
        )

    client = genai.Client(api_key=api_key)
    return GeminiParticipantSelector(model, client, max_messages)
