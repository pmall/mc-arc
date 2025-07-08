from .base import AbstractParticipantSelector


class AnthropicParticipantSelector(AbstractParticipantSelector):
    def _select_participant(self, participants, prompt):
        tool = {
            "name": "select_participant",
            "description": "Select a participant",
            "input_schema": {
                "type": "object",
                "properties": {
                    "selected_participant": {"type": "string", "enum": participants}
                },
                "required": ["selected_participant"],
            },
        }

        response = self.client.messages.create(
            model=self.model,
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
            tools=[tool],
            tool_choice={"type": "tool", "name": "select_participant"},
        )

        for content in response.content:
            if content.type == "tool_use":
                return content.input["selected_participant"]

        return participants[0]  # fallback


def create_anthropic_selector(
    model: str = "claude-3-5-sonnet-20241022",
    api_key: str | None = None,
    max_messages: int = 10,
):
    """Factory function that creates client and selector together."""
    try:
        from anthropic import Anthropic
    except ImportError:
        raise ImportError(
            "anthropic package not installed. Install with: pip install anthropic"
        )

    client = Anthropic(api_key=api_key)
    return AnthropicParticipantSelector(model, client, max_messages)
