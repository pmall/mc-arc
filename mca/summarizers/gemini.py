from string import Template
from google import genai
from google.genai import types
from mca.interfaces import Summarizer
from mca.prompts import SUMMARIZER_PROMPT_TEMPLATE


class GeminiSummarizer(Summarizer):
    def __init__(
        self,
        model: str,
        client: genai.Client,
        temperature: float = 0.2,
        max_output_tokens: int = 200,
    ):
        self.model = model
        self.client = client
        self.max_output_tokens = max_output_tokens
        self.temperature = temperature
        self.template = Template(SUMMARIZER_PROMPT_TEMPLATE)

    def __call__(self, messages: list[tuple[str, str]]) -> str:
        if not messages:
            return "Produce a new message"

        conversation = "\n".join([f"{role}: {content}" for role, content in messages])

        prompt = self.template.substitute(conversation=conversation)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=self.temperature,
                max_output_tokens=self.max_output_tokens,
            ),
        )

        return response.text
