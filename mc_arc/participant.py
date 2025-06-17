from mc_arc.response import StreamingResponse
from mc_arc.interfaces import Message, ContextModifier, Reporter, AgentAdapter
from mc_arc.prompts import (
    PARTICIPANT_PROMPT_TEMPLATE,
    PARTICIPANT_PROMPT_TEMPLATE_EMPTY,
    PARTICIPANT_PROMPT_TEMPLATE_MESSAGES_ONLY,
    PARTICIPANT_PROMPT_TEMPLATE_MODIFIERS_ONLY,
)


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
        if not messages and not modifiers:
            return PARTICIPANT_PROMPT_TEMPLATE_EMPTY()

        if not messages and modifiers:
            return PARTICIPANT_PROMPT_TEMPLATE_MODIFIERS_ONLY(modifiers)

        report = self.reporter(self.name, messages)

        if messages and not modifiers:
            return PARTICIPANT_PROMPT_TEMPLATE_MESSAGES_ONLY(report)

        return PARTICIPANT_PROMPT_TEMPLATE(report, modifiers)
