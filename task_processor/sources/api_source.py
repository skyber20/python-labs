import httpx
import logging

from typing import Iterable, Any

from task_processor.exceptions import ApiError, ConfigError
from task_processor.task import Task

logger = logging.getLogger(__name__)


class ApiSource:
    def __init__(
        self,
        url: str = "https://jsonplaceholder.typicode.com/todos",
        timeout: int | float = 5,
        limit: int | None = None
    ):
        self._url = url
        self._timeout = timeout
        self._limit = limit
        self._validate()
        logger.debug(f"Проинициализирован ApiSource(url={self._url}, timeout={self._timeout}, limit={self._limit})")

    def _validate(self) -> None:
        if not isinstance(self._url, str):
            raise ConfigError("Параметр url должен быть строковым типом")

        if not isinstance(self._timeout, (int, float)):
            raise ConfigError("Параметр timeout должен быть целочисленным или вещественным типом")

        if self._timeout <= 0:
            raise ConfigError("Параметр timeout должен быть положительным значением")

        if self._limit is not None and not isinstance(self._limit, int):
            raise ConfigError("Параметр limit должен быть целочисленным типом")

        if self._limit is not None and self._limit <= 0:
            raise ConfigError("Параметр limit должен быть положительным значением")

    def _fetch_data_from_server(self) -> list[dict]:
        params = {"_limit": self._limit} if self._limit else {}

        logger.info(f"Делаю запрос к {self._url}")
        with httpx.Client(timeout=self._timeout) as client:
            response = client.get(self._url, params=params)
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _parse_item(item: Any) -> Task | None:
        if isinstance(item, dict):
            task_id = item.get("id")
            payload = item.get("title") or item.get("payload")

            if task_id is not None and payload is not None:
                return Task(f"api_{task_id}", payload)

        logger.warning(f"Не удалось распарсить задачу, так как {type(item).__name__} != dict или невалидные поля")
        return None

    def get_tasks(self) -> Iterable[Task]:
        try:
            items = self._fetch_data_from_server()
            items = items if isinstance(items, list) else [items]

            if self._limit:
                items = items[:self._limit]

            logger.info(f"Получены {len(items)} данных из {self._url}")

            for item in items:
                task = self._parse_item(item)
                if task is not None:
                    yield task

        except httpx.HTTPError as e:
            logger.error(f"Ошибка при обращении к API: {e}")
            raise ApiError(f"Ошибка при обращении к API: {e}")
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при работе с API: {e}")
            raise ApiError(f"Непредвиденная ошибка при работе с API: {e}")
