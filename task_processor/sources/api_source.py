import httpx
import logging

from typing import Iterable, Any

from task_processor.exceptions import ApiError
from task_processor.task import Task
from task_processor.descriptors import Typed, IntRange

logger = logging.getLogger(__name__)


class ApiSource:
    """Класс источника, который получает задачи из API"""
    url = Typed(str)
    timeout = IntRange(min_value=1)
    limit = IntRange(min_value=1, allow_none=True)

    def __init__(
        self,
        url: str = "https://jsonplaceholder.typicode.com/todos",
        timeout: int = 5,
        limit: int | None = None
    ):
        """
        :param url: url
        :param timeout: время ожидания задач
        :param limit: сколько задач получаем
        """
        self.url = url
        self.timeout = timeout
        self.limit = limit
        logger.debug(f"Проинициализирован ApiSource(url={self.url}, timeout={self.timeout}, limit={self.limit})")

    def _fetch_data_from_server(self) -> list[dict]:
        """
        Получение данные с сервера
        :return: список задач
        """
        params = {"_limit": self.limit} if self.limit else {}

        logger.info(f"Делаю запрос к {self.url}")
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(self.url, params=params)
            response.raise_for_status()
            return response.json()

    @staticmethod
    def _parse_item(item: Any) -> Task | None:
        """
        Преоброазование задачи из сервера в Task
        :param item: задача
        :return: Task
        """
        if isinstance(item, dict):
            task_id = item.get("id")
            if task_id is not None:
                task_id = f"api_{task_id}"
            payload = item.get("title", "") or item.get("payload", "")

            return Task(description=payload, task_id=task_id)

        logger.warning(f"Не удалось распарсить задачу, получен {type(item).__name__} вместо dict")
        return None

    def get_tasks(self) -> Iterable[Task]:
        """
        Лениво собирает данные из источника
        :return: Объекты Task
        """
        try:
            items = self._fetch_data_from_server()
            items = items if isinstance(items, list) else [items]

            if self.limit:
                items = items[:self.limit]

            logger.info(f"Получены {len(items)} данных из {self.url}")

            for item in items:
                task = self._parse_item(item)
                if task is not None:
                    yield task

        except httpx.HTTPError as e:
            raise ApiError(f"Ошибка при обращении к API: {e}")
        except Exception as e:
            raise ApiError(f"Непредвиденная ошибка при работе с API: {e}")
