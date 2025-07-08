from .base import AbstractReporter


class OpenAIReporter(AbstractReporter):
    def _generate_report(self, prompt: str, max_output_tokens: int) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            max_tokens=max_output_tokens,
        )
        return response.choices[0].message.content


def create_openai_reporter(
    model: str = "gpt-4",
    api_key: str | None = None,
    temperature: float = 0.2,
    max_messages: int = 100,
):
    """Factory function that creates client and reporter together."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai package not installed. Install with: pip install openai"
        )

    client = OpenAI(api_key=api_key)
    return OpenAIReporter(model, client, temperature, max_messages)


def create_openrouter_reporter(
    model: str,
    api_key: str | None = None,
    temperature: float = 0.2,
    max_messages: int = 100,
):
    """Factory function for OpenRouter (uses OpenAI client with different base_url)."""
    try:
        from openai import OpenAI
    except ImportError:
        raise ImportError(
            "openai package not installed. Install with: pip install openai"
        )

    client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
    return OpenAIReporter(model, client, temperature, max_messages)
