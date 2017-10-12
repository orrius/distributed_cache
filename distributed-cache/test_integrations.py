import pytest
import server
import client


@pytest.fixture()
def client_1():
    return client.Client('test-server-1')

@pytest.fixture()
def client_2():
    return client.Client('test-server-2')


def test_set_and_get(client_1, client_2):
    client_1.set('testkey', 'testvalue')

    assert client_1.get('testkey') == 'testvalue'

    assert client_2.get('testkey') == 'testvalue'
