from mc_arc.response import StreamingResponse
from mc_arc.interfaces import Message, Reporter, AgentAdapter
from mc_arc.prompts import PARTICIPANT_PROMPT_TEMPLATE


class Participant:
    def __init__(
        self, name: str, agent: AgentAdapter, reporter: Reporter | None = None
    ):
        self.name = name
        self.agent = agent
        self.reporter = reporter
        self.message_buffer: list[Message] = []

    def receive_message(self, message: Message):
        if not self.name == message.name:
            self.message_buffer.append(message)

    def reply(self, cumulative: bool = False) -> StreamingResponse:
        prompt = self._prompt(self.message_buffer)

        response = self.agent(prompt)

        self.message_buffer.clear()

        return StreamingResponse(self.name, response, cumulative)

    def _prompt(self, messages) -> str:
        if not messages:
            return "You are the first to speak"

        report = (
            self.reporter(self.name, messages)
            if self.reporter
            else self._fallback_reporter(messages)
        )

        return PARTICIPANT_PROMPT_TEMPLATE(report)

    def _fallback_reporter(self, messages: list[Message]):
        return "\n".join([f"- {message}" for message in messages])
