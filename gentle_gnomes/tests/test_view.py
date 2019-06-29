def test_hello_world(client, app):
    assert client.get('/').status_code == 200
