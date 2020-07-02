import logging
from typing import Dict, Optional, List

from faker import Faker
from pydantic import BaseModel


class QueryItem(BaseModel):
    name: str
    params: Optional[Dict]


class QueryResult(BaseModel):
    results: List[Dict]
    errors: Optional[List]


class Query(BaseModel):
    items: List[QueryItem]


class QueryExecutor:
    def __init__(self, query: Query, limit: int):
        self.query = query
        self.limit = limit
        self.faker = Faker()

    @staticmethod
    def get_item_names(items: List[QueryItem]):
        return ",".join([item.name for item in items])

    def process(self) -> QueryResult:
        correct_items = [
            item for item in self.query.items if hasattr(self.faker, item.name)
        ]
        incorrect_items = [
            item for item in self.query.items if not hasattr(self.faker, item.name)
        ]

        if incorrect_items:
            logging.warning(
                f"Found incorrect item names: {self.get_item_names(incorrect_items)}"
            )

        results = []
        errors = [{"name": item.name} for item in incorrect_items]

        for _ in range(self.limit):
            if correct_items:
                result = {}
                for item in correct_items:
                    if item.params:
                        result[item.name] = getattr(self.faker, item.name)(
                            **item.params
                        )
                    else:
                        result[item.name] = getattr(self.faker, item.name)()

                results.append(result)

        return QueryResult(results=results, errors=errors)

    def __call__(self) -> QueryResult:
        return self.process()
