import json
import logging

from pathlib import Path
from typing import Iterable, Any

from task_processor.task import Task
from task_processor.exceptions import SourceReadError
from task_processor.descriptors import ExistingFile

logger = logging.getLogger(__name__)


class JsonFileSource:
    """Класс источника, который получает данные из файла"""
    path = ExistingFile()

    def __init__(self, path: str | Path):
        """
        :param path: Путь к файлу
        """
        self.path = path
        logger.debug(f"Проинициализирован JsonFileSource(path={self.path})")

    @staticmethod
    def _parse_item(item: Any) -> Task | None:
        """
        Преобразование задач из файла в Task
        :param item: задача из файла
        :return: Task
        """
        if isinstance(item, dict):
            task_id = item.get("id")
            payload = item.get("payload", "")
            priority = item.get("priority", 0)

            return Task(payload, priority, task_id)

        logger.warning(f"Не удалось распарсить задачу, получен {type(item).__name__} вместо dict")
        return None

    def get_tasks(self) -> Iterable[Task]:
        """
        Лениво собирает данные из источника
        :return: Объекты Task
        """
        try:
            logger.info(f"Читаю файл по пути {self.path}")
            with open(self.path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, (list, dict)):
                    raise SourceReadError(f"Содержание Json должно быть списком или словарем, получено: {type(data).__name__}")
        except OSError as e:
            raise SourceReadError(f"{self.path}: Системная ошибка при попытке прочитать файл: {e}")
        except json.decoder.JSONDecodeError as e:
            raise SourceReadError(f"{self.path}: Невалидный формат Json: {e}")

        items = data if isinstance(data, list) else [data]

        logger.info(f"Получены {len(items)} данных из {self.path}")

        for item in items:
            task = self._parse_item(item)
            if task is not None:
                yield task
