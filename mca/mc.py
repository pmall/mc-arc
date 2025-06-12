import random
import contextlib
from typing import Optional
from mca.participant import Participant
from mca.interfaces import Selector, Message, ContextModifier, TimelineItem


class MasterOfCeremony:
    def __init__(
        self, selector: Selector, participants: Optional[list[Participant]] = None
    ):
        self.selector = selector
        self.participants = {}
        self.last_name: Optional[str] = None
        self.timeline: list[Message] = []
        self.modifiers: dict[tuple[str, int], list[ContextModifier]] = {}
        self.offsets: dict[tuple[str, str], int]

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

    def add_modifier(self, modifier: ContextModifier):
        for participant in self.participants.values():
            self._add_modifier_for(participant, modifier)

    def add_modifier_for(self, name: str, modifier: ContextModifier):
        participant = self._select_participant(name)

        self._add_modifier_for(participant, modifier)

    def pull_timeline_of(self, name: str, subscriber: str) -> list[TimelineItem]:
        timeline: list[TimelineItem] = []

        offset = self.offsets.get((name, subscriber), 0)

        for i in range(offset, len(timeline)):
            message = self.timeline[i]
            modifiers = self.modifiers[(name, i)]
            timeline.append(TimelineItem(message, modifiers))

        self.offsets[(name, subscriber)] = len(self.timeline)

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

    def _add_modifier_for(self, participant: Participant, modifier: ContextModifier):
        index = len(self.timeline)

        self.modifiers.setdefault((participant.name, index), []).append(modifier)

        participant.receive_modifier(modifier)

    def _available_names(self) -> list[str]:
        return [name for name in self.participants.keys() if name != self.last_name]

    def _select_available_name(self) -> str:
        available_names = self._available_names()

        try:
            name = self.selector(available_names, self.timeline)

            if name in available_names:
                return name
            else:
                return self._select_fallback(available_names)
        except Exception:
            return self._select_fallback(available_names)

    def _select_available_participant(self) -> Participant:
        name = self._select_available_name()

        return self.participants[name]

    def _select_fallback(self, available_names: list[str]) -> str:
        return random.choice(available_names)
