from _dependencies.funcs import publish_to_pubsub


def notify_admin(message) -> None:
    """send the pub/sub message to Debug to Admin"""

    publish_to_pubsub('topic_notify_admin', message)
