import random
import contextlib
from typing import Optional
from mca.interfaces import Selector
from mca.participant import Participant


class MasterOfCeremony:
    def __init__(
        self,
        participants: list[Participant],
        selector: Selector,
        max_context_window_size: int = 10,
    ):
        self.participants = {p.name: p for p in participants}
        self.selector = selector
        self.timeline: list[tuple[str, str]] = []
        self.last_participant_name: Optional[str] = None
        self.max_context_window_size = max_context_window_size

    def add_message(self, participant_name: str, message: str):
        self.timeline.append((participant_name, message))
        self.last_participant_name = participant_name

        for name, participant in self.participants.items():
            if name != participant_name:
                participant.receive_message(participant_name, message)

    @contextlib.asynccontextmanager
    async def step(self):
        response = ""

        participant = self._select_participant()

        stream = participant.reply()

        async def chunk_generator():
            nonlocal response
            async for chunk in stream:
                response = chunk.strip()
                yield (participant.name, response)

        generator = chunk_generator()

        try:
            yield generator
        finally:
            # Ensure the stream is fully consumed
            try:
                async for _ in generator:
                    pass
            except StopAsyncIteration:
                pass

            self.add_message(participant.name, response)

    def _select_participant(self) -> Participant:
        participant_name = self._select_participant_name()

        return self.participants[participant_name]

    def _select_participant_name(self) -> str:
        available_participant_names = [
            name
            for name in self.participants.keys()
            if name != self.last_participant_name
        ]

        last_messages = (
            self.timeline[-self.max_context_window_size :]
            if self.max_context_window_size > 0
            else []
        )

        try:
            participant_name = self.selector(available_participant_names, last_messages)

            if participant_name in available_participant_names:
                return participant_name
            else:
                return self._select_fallback(available_participant_names)
        except Exception:
            return self._select_fallback(available_participant_names)

    def _select_fallback(self, available_participant_names: list[str]) -> str:
        return random.choice(available_participant_names)
