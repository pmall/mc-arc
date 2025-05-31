from typing import Optional
from .base import AbstractSummarizer


class OpenAISummarizer(AbstractSummarizer):
    def _generate_summary(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=self.max_output_tokens,
        )
        return response.choices[0].message.content


def create_openai_summarizer(
    model: str = "gpt-4",
    api_key: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1000,
    max_messages: int = 10,
):
    """Factory function that creates client and summarizer together."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai package not installed. Install with: pip install openai"
        )

    client = OpenAI(api_key=api_key)
    return OpenAISummarizer(model, client, temperature, max_output_tokens, max_messages)


def create_openrouter_summarizer(
    model: str,
    api_key: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1000,
    max_messages: int = 10,
):
    """Factory function for OpenRouter (uses OpenAI client with different base_url)."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai package not installed. Install with: pip install openai"
        )

    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    return OpenAISummarizer(model, client, temperature, max_output_tokens, max_messages)
