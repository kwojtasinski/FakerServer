from fastapi.testclient import TestClient

from faker_server.server import app, API_PATH

client = TestClient(app)


def test_server_should_respond_with_password():
    response = client.post(
        API_PATH.format("query"), json={"items": [{"name": "password"}]}
    ).json()

    results = response.get("results")

    assert isinstance(results[0].get("password"), str)
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

    results = response.get("results")

    assert isinstance(results[0].get("name"), str)
    assert isinstance(results[0].get("email"), str)
    assert not response.get("errors")


def test_server_should_support_item_params():
    response = client.post(
        API_PATH.format("query"),
        json={"items": [{"name": "pyint", "params": {"max_value": 100}}]},
    ).json()

    results = response.get("results")

    assert results[0].get("pyint") <= 100
    assert not response.get("errors")


def test_server_should_support_locale():
    response = client.post(
        API_PATH.format("query"),
        json={"items": [{"name": "password"}], "settings": {"locale": "pl_PL"}},
    ).json()

    results = response.get("results")

    assert isinstance(results[0].get("password"), str)
    assert not response.get("errors")


def test_query_executor_should_omit_incorrect_params():
    response = client.post(
        API_PATH.format("query"),
        json={"items": [{"name": "name", "params": {"INCORRECT": True}}]},
    ).json()

    results = response.get("results")
    errors = response.get("errors")

    assert isinstance(results[0].get("name"), str)
    assert errors[0].get("item").get("name") == "name"
    assert errors[0].get("item").get("params") == {"INCORRECT": True}
    assert "params" in errors[0].get("reason")


def test_query_executor_should_support_get_single_item():
    response = client.get(API_PATH.format("password"),).json()

    results = response.get("results")

    assert isinstance(results[0].get("password"), str)
    assert not response.get("errors")


def test_query_executor_should_support_flatten_with_get_single_item():
    params = {"limit": 5, "flatten": True}
    response = client.get(API_PATH.format("password"), params=params).json()

    results = response.get("results")

    assert all([isinstance(result, str) for result in results])
    assert not response.get("errors")
