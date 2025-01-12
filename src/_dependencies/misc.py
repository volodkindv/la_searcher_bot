import google.auth.transport.requests
import google.cloud.logging
import google.oauth2.id_token
import requests

from _dependencies.funcs import publish_to_pubsub


def notify_admin(message) -> None:
    """send the pub/sub message to Debug to Admin"""

    publish_to_pubsub('topic_notify_admin', message)


def make_api_call(function: str, data: dict) -> dict:
    """makes an API call to another Google Cloud Function"""

    # function we're turing to "title_recognize"
    endpoint = f'https://europe-west3-lizaalert-bot-01.cloudfunctions.net/{function}'

    # required magic for Google Cloud Functions Gen2 to invoke each other
    audience = endpoint
    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)
    headers = {'Authorization': f'Bearer {id_token}', 'Content-Type': 'application/json'}

    r = requests.post(endpoint, json=data, headers=headers)
    content = r.json()

    return content
