from fastapi.testclient import TestClient

from faker_server.server import app, API_PATH

client = TestClient(app)


def test_server_should_respond_with_password():
    response = client.post(
        API_PATH.format("query"), json={"items": [{"name": "password"}]}
    ).json()

    for result in response.get("results"):
        assert isinstance(result.get("password"), str)

    assert not response.get("errors")


def test_server_should_respond_with_errors():
    response = client.post(
        API_PATH.format("query"), json={"items": [{"name": "NONEXISTENT"}]}
    ).json()

    assert response.get("errors")[0]["item"]["name"] == "NONEXISTENT"
    assert not response.get("items")


def test_server_should_generate_pair_of_items():
    response = client.post(
        API_PATH.format("query"), json={"items": [{"name": "name"}, {"name": "email"}]}
    ).json()

    for result in response.get("results"):
        assert isinstance(result.get("name"), str)
        assert isinstance(result.get("email"), str)

    assert not response.get("errors")


def test_server_should_support_item_params():
    response = client.post(
        API_PATH.format("query"),
        json={"items": [{"name": "pyint", "params": {"max_value": 100}}]},
    ).json()

    for result in response.get("results"):
        assert result.get("pyint") <= 100

    assert not response.get("errors")


def test_server_should_support_locale():
    response = client.post(
        API_PATH.format("query"),
        json={"items": [{"name": "name"}], "settings": {"locale": "pl_PL"}},
    ).json()

    for result in response.get("results"):
        assert isinstance(result.get("name"), str)

    assert not response.get("errors")


def test_query_executor_should_omit_incorrect_params():
    response = client.post(
        API_PATH.format("query"),
        json={"items": [{"name": "name", "params": {"INCORRECT": True}}]},
    ).json()

    for result in response.get("results"):
        assert isinstance(result.get("name"), str)

    errors = response.get("errors")

    assert errors[0].get("item").get("name") == "name"
    assert errors[0].get("item").get("params") == {"INCORRECT": True}
    assert "params" in errors[0].get("reason")
