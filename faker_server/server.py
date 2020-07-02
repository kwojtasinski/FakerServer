import logging

from fastapi import FastAPI

from query import Query, QueryExecutor, QueryResult

app = FastAPI()

@app.post("/query")
def query_fake_data(query: Query, limit: int = 1) -> QueryResult:
    names = ",".join([item.name for item in query.items])
    logging.info(f"Get query (items={names}) with limit {limit}")
    executor = QueryExecutor(query, limit)

    return executor()
