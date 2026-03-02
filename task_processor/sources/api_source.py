import httpx

from typing import Iterable

from task_processor.exceptions import NegativeValue, FailGetData
from task_processor.task import Task


class ApiSource:
    def __init__(self, url: str = "https://jsonplaceholder.typicode.com/todos", timeout: int | float = 5):
        self._url = url
        self._timeout = timeout
        self._validate()

    def _validate(self) -> None:
        if not isinstance(self._url, str):
            raise TypeError(f"{self._url}: Невалидный тип URL")

        if not isinstance(self._timeout, (int, float)):
            raise TypeError(f"{self._timeout}: Невалидный тип timeout")

        if self._timeout <= 0:
            raise NegativeValue("timeout")

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
            raise FailGetData(str(e))
