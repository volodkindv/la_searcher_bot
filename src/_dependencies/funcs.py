import json
import logging
import os
import urllib.request
from functools import lru_cache
from typing import Any

import google.cloud.logging
from google.cloud import pubsub_v1, secretmanager

# TODO describe common deps in UV

@lru_cache
def get_secret_manager_client() -> secretmanager.SecretManagerServiceClient:
    return secretmanager.SecretManagerServiceClient()


@lru_cache
def get_project_id() -> str:
    url = 'http://metadata.google.internal/computeMetadata/v1/project/project-id'
    req = urllib.request.Request(url)
    req.add_header('Metadata-Flavor', 'Google')
    project_id = urllib.request.urlopen(req).read().decode()
    return project_id


@lru_cache  # TODO maybe cachetools/timed_lru_cache?
def get_secrets(secret_request: str) -> str:
    """Get GCP secret"""

    name = f'projects/{get_project_id()}/secrets/{secret_request}/versions/latest'
    response = get_secret_manager_client().access_secret_version(name=name)

    return response.payload.data.decode('UTF-8')


def setup_google_logging():
    logging_disabled = os.getenv('GOOGLE_LOGGING_DISABLED', False)
    if logging_disabled:
        # TODO pydantic-settings or improve parsing here.
        return

    log_client = google.cloud.logging.Client()
    log_client.setup_logging()


@lru_cache
def get_publisher() -> pubsub_v1.PublisherClient:
    return pubsub_v1.PublisherClient()


def publish_to_pubsub(topic_name: str, message: Any) -> None:
    """publish a new message to pub/sub"""

    topic_path = get_publisher().topic_path(get_project_id(), topic_name)
    message_json = json.dumps(
        {
            'data': {'message': message},
        }
    )
    message_bytes = message_json.encode('utf-8')

    try:
        publish_future = get_publisher().publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publishing succeeded
        logging.info(f'Sent pub/sub message: {str(message)}')

    except Exception as e:
        logging.error('Not able to send pub/sub message: ' + repr(e))
        logging.exception(e)

    return None
