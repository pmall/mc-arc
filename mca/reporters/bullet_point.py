class BulletPointReporter:
    def __call__(self, _, messages):
        return "\n".join([f"- {message}" for message in messages])


def create_bullet_point_reporter():
    return BulletPointReporter()
