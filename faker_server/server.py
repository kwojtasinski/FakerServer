import logging

from fastapi import FastAPI

from query import Query, QueryExecutor, QueryResult

app = FastAPI()


@app.post("/query")
def query_fake_data(query: Query, limit: int = 1) -> QueryResult:
    logging.info(
        f"Get query (items={QueryExecutor.get_item_names(query.items)}) with limit {limit}"
    )
    executor = QueryExecutor(query, limit)

    return executor()
