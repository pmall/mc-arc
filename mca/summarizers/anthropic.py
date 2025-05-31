from typing import Optional
from .base import AbstractSummarizer


class AnthropicSummarizer(AbstractSummarizer):
    def _generate_summary(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_output_tokens,
            temperature=self.temperature,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text


def create_anthropic_summarizer(
    model: str = "claude-3-5-sonnet-20241022",
    api_key: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1000,
    max_messages: int = 10,
):
    """Factory function that creates client and summarizer together."""
    try:
        import anthropic
    except ImportError:
        raise ImportError(
            "anthropic package not installed. Install with: pip install anthropic"
        )

    client = anthropic.Anthropic(api_key=api_key)
    return AnthropicSummarizer(
        model, client, temperature, max_output_tokens, max_messages
    )
