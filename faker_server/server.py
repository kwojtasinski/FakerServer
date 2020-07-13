import logging

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from query import Query, QueryExecutor, QueryResult

API_PATH = "/api/v1/{}"

app = FastAPI()

@app.get("/")
def home():
    """ Redirects to docs """
    return RedirectResponse("/docs")


@app.post(API_PATH.format("query"))
def query_fake_data(query: Query, limit: int = 1) -> QueryResult:
    logging.info(
        f"Get query (items={QueryExecutor.get_item_names(query.items)}) with limit {limit}"
    )
    executor = QueryExecutor(query, limit)

    return executor()
