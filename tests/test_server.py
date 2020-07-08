from fastapi.testclient import TestClient

from faker_server.server import app

client = TestClient(app)


def test_server_should_respond_with_password():
    response = client.post("query", json={"items": [{"name": "password"}]}).json()

    assert "results" in response
    assert not response.get("errors")
    assert "password" in response.get("results")[0]


def test_server_should_respond_with_errors():
    response = client.post("query", json={"items": [{"name": "NONEXISTENT"}]}).json()

    assert not response.get("items")
    assert response.get("errors")[0].get("name") == "NONEXISTENT"


def test_server_should_generate_pair_of_items():
    response = client.post(
        "query", json={"items": [{"name": "name"}, {"name": "email"}]}
    ).json()

    for result in response.get("results"):
        assert "name" in result
        assert "email" in result
        assert isinstance(result.get("name"), str)
        assert isinstance(result.get("email"), str)


def test_query_executor_should_support_item_params():
    response = client.post(
        "query", json={"items": [{"name": "pyint", "params": {"max_value": 100}}]}
    ).json()

    for result in response.get("results"):
        assert result.get("pyint") <= 100

    assert not response.get("errors")
