from mca.interfaces import Message


class BulletPointReporter:
    def __call__(self, participant: str, messages: list[Message]) -> str:
        replace = lambda p: "You" if p == participant else p

        return "\n".join(
            [f"- {replace(message.name)}: {message.content}" for message in messages]
        )


def create_bullet_point_reporter():
    return BulletPointReporter()
