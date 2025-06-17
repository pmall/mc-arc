import json
from typing import Optional
from .base import AbstractParticipantSelector


class OpenAIParticipantSelector(AbstractParticipantSelector):
    def _select_participant(self, participants, prompt):
        schema = {
            "type": "object",
            "properties": {
                "selected_participant": {"type": "string", "enum": participants}
            },
            "required": ["selected_participant"],
        }

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={
                "type": "json_schema",
                "json_schema": {"name": "participant_selection", "schema": schema},
            },
        )

        result = json.loads(response.choices[0].message.content)
        return result["selected_participant"]


def create_openai_selector(
    model: str = "gpt-4", api_key: Optional[str] = None, max_messages: int = 10
):
    """Factory function that creates client and selector together."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai package not installed. Install with: pip install openai"
        )

    client = OpenAI(api_key=api_key)
    return OpenAIParticipantSelector(model, client, max_messages)


def create_openrouter_selector(
    model: str, api_key: Optional[str] = None, max_messages: int = 10
):
    """Factory function for OpenRouter (uses OpenAI client with different base_url)."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai package not installed. Install with: pip install openai"
        )

    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    return OpenAIParticipantSelector(model, client, max_messages)
