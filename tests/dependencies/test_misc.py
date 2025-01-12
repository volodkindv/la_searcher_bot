from _dependencies import misc


def test_notify_admin(patch_pubsub_client):
    data = 'some message'

    misc.notify_admin(data)
    publish_call_args = patch_pubsub_client.return_value.method_calls[1].kwargs
    assert data in publish_call_args['data'].decode()


def test_make_api_call():
    # TODO mock requests
    misc.make_api_call('test', {'a: 1'})
