from mca.response import StreamingResponse
from mca.interfaces import Message, ContextModifier, Reporter, AgentAdapter
from mca.prompts import PARTICIPANT_PROMPT_TEMPLATE


class Participant:
    def __init__(self, name: str, agent: AgentAdapter, reporter: Reporter):
        self.name = name
        self.agent = agent
        self.reporter = reporter
        self.message_buffer: list[Message] = []
        self.modifier_buffer: list[ContextModifier] = []

    def receive_message(self, message: Message):
        self.message_buffer.append(message)

    def receive_modifier(self, modifier: ContextModifier):
        self.modifier_buffer.append(modifier)

    def reply(self, cumulative: bool = False) -> StreamingResponse:
        messages = self.message_buffer
        modifiers = self.modifier_buffer

        prompt = self._prompt(messages, modifiers)

        self.message_buffer.clear()
        self.modifier_buffer.clear()

        response = self.agent(prompt)

        return StreamingResponse(self.name, response, cumulative)

    def _prompt(self, messages, modifiers) -> str:
        report = self.reporter(self.name, messages)

        return PARTICIPANT_PROMPT_TEMPLATE(report, modifiers)
