import random


class RandomParticipantSelector:
    def __call__(self, participants, _):
        return random.choice(participants)


def create_random_selector():
    return RandomParticipantSelector()
