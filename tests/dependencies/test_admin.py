from _dependencies import admin


def test_notify_admin(patch_pubsub_client):
    data = 'some message'

    admin.notify_admin(data)
    publish_call_args = patch_pubsub_client.return_value.method_calls[1].kwargs
    assert data in publish_call_args['data'].decode()
