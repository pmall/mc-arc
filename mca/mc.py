import random
import contextlib
from typing import Optional
from mca.participant import Participant
from mca.interfaces import Selector, Message, ModifierType, ContextModifier


class MasterOfCeremony:
    def __init__(
        self, selector: Selector, participants: Optional[list[Participant]] = None
    ):
        self.stepn = 0
        self.selector = selector
        self.participants: dict[str, Participant] = {}
        self.last_name: Optional[str] = None
        self.timeline: list[Message] = []
        self.offsets: dict[str, int] = {}

        for participant in participants or []:
            self.add_participant(participant)

    def add_participant(self, participant: Participant):
        if self.participants.get(participant.name):
            raise ValueError(f"Participant named {participant.name} already exists.")

        self.participants[participant.name] = participant

    def add_message(self, sender: str, content: str):
        message = Message(sender, content)

        self.timeline.append(message)
        self.last_name = sender

        for name, participant in self.participants.items():
            if name != sender:
                participant.receive_message(message)

    def add_modifier(self, type: ModifierType, content: str):
        for participant in self.participants.values():
            participant.receive_modifier(ContextModifier(type, content))

    def add_modifier_to(self, name: str, type: ModifierType, content: str):
        participant = self._select_participant(name)

        participant.receive_modifier(ContextModifier(type, content))

    def pull_timeline_as(self, subscriber: str) -> list[Message]:
        start = self.offsets.get(subscriber, 0)

        timeline = self.timeline[start:]

        self.offsets[subscriber] = len(self.timeline)

        return timeline

    @contextlib.asynccontextmanager
    async def step(self, cumulative: bool = False):
        participant = self._select_available_participant()

        response = participant.reply(cumulative)

        async with response as generator:
            try:
                yield generator
            finally:
                self.add_message(participant.name, response.get_full_response())

    def _select_participant(self, name: str) -> Participant:
        participant = self.participants.get(name)

        if participant:
            return participant

        raise ValueError(f"No participant named {name}.")

    def _select_available_participant(self) -> Participant:
        available_names = [
            name for name in self.participants.keys() if name != self.last_name
        ]

        try:
            name = self.selector(available_names, self.timeline)

            if name in available_names:
                return self.participants[name]
            else:
                return self._select_fallback(available_names)
        except Exception:
            return self._select_fallback(available_names)

    def _select_fallback(self, available_names: list[str]) -> Participant:
        name = random.choice(available_names)

        return self.participants[name]
