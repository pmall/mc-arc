from mc_arc.interfaces import Message


class BulletPointReporter:
    def __call__(self, _: str, messages: list[Message]) -> str:
        return "\n".join([f"- {message}" for message in messages])


def create_bullet_point_reporter():
    return BulletPointReporter()
