from typing import Optional
from google.genai import types
from .base import AbstractSummarizer


class GeminiSummarizer(AbstractSummarizer):
    def _generate_summary(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            ),
        )
        return response.text


def create_gemini_summarizer(
    model: str = "gemini-2.0-flash",
    api_key: Optional[str] = None,
    temperature: float = 0.2,
    max_output_tokens: int = 1000,
    max_messages: int = 10,
):
    """Factory function that creates client and summarizer together."""
    try:
        from google import genai
    except ImportError:
        raise ImportError(
            "google-generativeai package not installed. Install with: pip install google-generativeai"
        )

    client = genai.Client(api_key=api_key)
    return GeminiSummarizer(model, client, temperature, max_output_tokens, max_messages)
