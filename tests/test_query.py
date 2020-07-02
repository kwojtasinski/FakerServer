from faker_server.query import QueryExecutor, Query, QueryItem


def test_query_executor_should_generate_random_password():
    query = Query(items=[QueryItem(name="password")])
    executor = QueryExecutor(query, 10)
    query_result = executor()

    for result in query_result.results:
        assert "password" in result
        assert isinstance(result["password"], str)


def test_query_executor_should_return_errors():
    query = Query(items=[QueryItem(name="NONEXISTENT")])
    executor = QueryExecutor(query, 10)
    query_result = executor()

    assert not query_result.results
    assert query_result.errors[0].get("name") == "NONEXISTENT"


def test_query_executor_should_generate_pair_of_items():
    query = Query(items=[QueryItem(name="name"), QueryItem(name="email")])
    executor = QueryExecutor(query, 10)
    query_result = executor()
    for result in query_result.results:
        assert "name" in result
        assert "email" in result
        assert isinstance(result.get("name"), str)
        assert isinstance(result.get("email"), str)
