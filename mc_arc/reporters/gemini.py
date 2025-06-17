from typing import Optional
from google.genai import types
from .base import AbstractReporter


class GeminiReporter(AbstractReporter):
    def _generate_report(self, prompt: str, max_output_tokens: int) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=max_output_tokens,
            ),
        )
        return response.text


def create_gemini_reporter(
    model: str = "gemini-2.0-flash",
    api_key: Optional[str] = None,
    temperature: float = 0.2,
    max_messages: int = 100,
):
    """Factory function that creates client and reporter together."""
    try:
        from google import genai
    except ImportError:
        raise ImportError(
            "google-generativeai package not installed. Install with: pip install google-generativeai"
        )

    client = genai.Client(api_key=api_key)
    return GeminiReporter(model, client, temperature, max_messages)
