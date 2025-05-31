import random
import contextlib
from typing import Optional
from mca.participant import Participant
from mca.interfaces import Message, ParticipantMessage, NarratorMessage, Selector


class MasterOfCeremony:
    def __init__(self, participants: list[Participant], selector: Selector):
        self.participants = {p.name: p for p in participants}
        self.selector = selector
        self.timeline: list[Message] = []
        self.last_participant_name: Optional[str] = None

    def add_message(self, participant_name: str, content: str):
        message = ParticipantMessage(participant_name, content)

        self.timeline.append(message)
        self.last_participant_name = participant_name

        for name, participant in self.participants.items():
            if name != participant_name:
                participant.receive_message(message)

    def add_narrator_message(self, content: str):
        message = NarratorMessage(content)

        self.timeline.append(message)

        for name, participant in self.participants.items():
            participant.receive_message(message)

    @contextlib.asynccontextmanager
    async def step(self, cumulative: bool = False):
        participant = self._select_participant()

        response = participant.reply(cumulative)

        async with response as generator:
            try:
                yield generator
            finally:
                self.add_message(participant.name, response.get_full_response())

    def _available_participant_names(self) -> str:
        return [
            name
            for name in self.participants.keys()
            if name != self.last_participant_name
        ]

    def _select_participant(self) -> Participant:
        participant_name = self._select_participant_name()

        return self.participants[participant_name]

    def _select_participant_name(self) -> str:
        available_participant_names = self._available_participant_names()

        try:
            participant_name = self.selector(available_participant_names, self.timeline)

            if participant_name in available_participant_names:
                return participant_name
            else:
                return self._select_fallback(available_participant_names)
        except Exception:
            return self._select_fallback(available_participant_names)

    def _select_fallback(self, available_participant_names: list[str]) -> str:
        return random.choice(available_participant_names)
