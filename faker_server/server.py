from fastapi import FastAPI

from query import Query, QueryExecutor, QueryResult, QueryItem

API_PATH = "/api/v1/{}"

app = FastAPI(docs_url="/")


@app.get(API_PATH.format("{name}"))
def get_single_item(name: str, limit: int = 1, flatten: bool = False) -> QueryResult:
    query = Query(items=[QueryItem(name=name)])
    executor = QueryExecutor(query, limit)

    return executor.process(flatten)


@app.post(API_PATH.format("query"))
def query_fake_data(query: Query, limit: int = 1) -> QueryResult:
    executor = QueryExecutor(query, limit)
    return executor()
