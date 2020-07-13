import logging
from typing import Dict, Optional, List, Union

from faker import Faker
from pydantic import BaseModel


class QueryItem(BaseModel):
    name: str
    params: Optional[Dict]


class QueryItemError(BaseModel):
    item: QueryItem
    reason: str


class QueryResult(BaseModel):
    results: List[Dict]
    errors: Optional[List[QueryItemError]]


class QuerySettings(BaseModel):
    locale: Optional[Union[str, List]]
    seed: Optional[int]


class Query(BaseModel):
    items: List[QueryItem]
    settings: Optional[QuerySettings]


class QueryExecutor:
    def __init__(self, query: Query, limit: int):
        self.query = query
        self.limit = limit

        if self.query.settings:
            settings_dict = self.query.settings.dict()
            self.faker = Faker(settings_dict.get("locale"))
            Faker.seed(settings_dict.get("seed"))
        else:
            self.faker = Faker()

    @staticmethod
    def get_item_names(items: List[QueryItem]) -> str:
        return ",".join([item.name for item in items])

    def _check_params_validity(self, item: QueryItem) -> bool:
        if not item.params:
            return True

        try:
            getattr(self.faker, item.name)(**item.params)
            return True
        except Exception:
            return False

    def _prepare_errors(
        self, correct_items: List[QueryItem]
    ) -> Optional[List[QueryItemError]]:

        errors = []

        incorrect_name_items = [
            item for item in self.query.items if not hasattr(self.faker, item.name)
        ]

        incorrect_params_items = [
            item for item in correct_items if not self._check_params_validity(item)
        ]

        if incorrect_name_items:
            logging.warning(
                f"Found incorrect item names: {self.get_item_names(incorrect_name_items)}"
            )
            errors.extend(
                QueryItemError(item=item, reason=f"{item.name} item not available",)
                for item in incorrect_name_items
            )

        if incorrect_params_items:
            for item in incorrect_params_items:
                query_error = QueryItemError(
                    item=item,
                    reason=f"Item {item.name} does not support params ({item.params}). Ommiting params.",
                )
                logging.warning(query_error.reason)
                errors.append(query_error)

        return errors

    def process(self) -> QueryResult:
        correct_items = [
            item for item in self.query.items if hasattr(self.faker, item.name)
        ]

        results = []
        errors = self._prepare_errors(correct_items)

        for _ in range(self.limit):
            if correct_items:
                result = {}
                for item in correct_items:
                    if item.params and self._check_params_validity(item):
                        result[item.name] = getattr(self.faker, item.name)(
                            **item.params
                        )
                    else:
                        result[item.name] = getattr(self.faker, item.name)()

                results.append(result)

        return QueryResult(results=results, errors=errors)

    def __call__(self) -> QueryResult:
        return self.process()
