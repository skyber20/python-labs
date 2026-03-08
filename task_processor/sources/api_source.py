import httpx

from typing import Iterable

from task_processor.exceptions import ApiError, ConfigTypeError, ConfigValueError
from task_processor.task import Task


class ApiSource:
    def __init__(self, url: str = "https://jsonplaceholder.typicode.com/todos", timeout: int | float = 5, limit: int | None = None):
        self._url = url
        self._timeout = timeout
        self._limit = limit
        self._validate()

    def _validate(self) -> None:
        if not isinstance(self._url, str):
            raise ConfigTypeError("url", type(self._url), "str")

        if not isinstance(self._timeout, (int, float)):
            raise ConfigTypeError("timeout", type(self._timeout), "int | float")

        if not isinstance(self._limit, (None, int)):
            raise ConfigTypeError("limit", type(self._limit), "int")

        if self._timeout <= 0:
            raise ConfigValueError("timeout", "должно быть положительное значение")

        if self._limit is not None and self._limit <= 0:
            raise ConfigValueError("limit", "должно быть положительное значение")

    @property
    def url(self) -> str:
        return self._url

    def _fetch_data_from_server(self) -> list[dict]:
        with httpx.Client(timeout=self._timeout) as client:
            response = client.get(self._url)
            response.raise_for_status()
            return response.json()


    def get_tasks(self) -> Iterable[Task]:
        try:
            items = self._fetch_data_from_server()
            items = items if isinstance(items, list) else [items]

            for item in items:
                if not isinstance(item, dict):
                    continue

                task_id = item.get("id", None)
                payload = item.get("title", None)

                if task_id is not None and payload is not None:
                    yield Task(f"api_{task_id}", payload)

        except httpx.HTTPError as e:
            raise ApiError(str(e))
