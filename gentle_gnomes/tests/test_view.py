def test_index_response_200(client):
    assert client.get('/').status_code == 200
