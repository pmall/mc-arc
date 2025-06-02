from typing import Optional
from .base import AbstractReporter


class AnthropicReporter(AbstractReporter):
    def _generate_report(self, prompt: str, max_output_tokens: int) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_output_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text


def create_anthropic_reporter(
    model: str = "claude-3-5-sonnet-20241022",
    api_key: Optional[str] = None,
    temperature: float = 0.2,
    max_messages: int = 100,
):
    """Factory function that creates client and reporter together."""
    try:
        import anthropic
    except ImportError:
        raise ImportError(
            "anthropic package not installed. Install with: pip install anthropic"
        )

    client = anthropic.Anthropic(api_key=api_key)
    return AnthropicReporter(model, client, temperature, max_messages)
