import random
import contextlib
from mc_arc.participant import Participant
from mc_arc.interfaces import Selector, Message


class MasterOfCeremony:
    def __init__(
        self,
        selector: Selector | None = None,
        participants: list[Participant] | None = None,
    ):
        self.selector = selector
        self.participants: dict[str, Participant] = {}
        self.last_name: str | None = None
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

        for participant in self.participants.values():
            participant.receive_message(message)

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

        if not self.selector:
            return self._select_fallback(available_names)

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
