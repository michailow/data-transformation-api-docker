import pytest

from webserver.api import createApp


@pytest.fixture
def client():
    app = createApp()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_square(client):
    rv = client.get("/")
    assert 'App started' == rv.data
