import uuid
import json
import logging

from pathlib import Path
from typing import Iterable, Any

from task_processor.task import Task
from task_processor.exceptions import ConfigError, SourceReadError

logger = logging.getLogger(__name__)


class JsonFileSource:
    def __init__(self, path: str | Path):
        """
        Класс источника, который получает данные из файла
        :param path: Путь к файлу
        """
        self._path = Path(path)
        self._validate()
        logger.debug(f"Проинициализирован JsonFileSource(path={self._path})")

    def _validate(self) -> None:
        """Валидация данных при создании экзампляра"""
        if not self._path.is_file():
            raise ConfigError(f"{self._path}: Путь не существует или не является файлом")

    @staticmethod
    def _parse_item(item: Any) -> Task | None:
        """
        Преобразование задач из файла в Task
        :param item: задача из файла
        :return: Task
        """
        if isinstance(item, dict):
            task_id = item.get("id")
            if task_id is None:
                task_id = uuid.uuid4().hex
            payload = item.get("payload", "")

            return Task(f"{task_id}", payload)

        logger.warning(f"Не удалось распарсить задачу, получен {type(item).__name__} вместо dict")
        return None

    def get_tasks(self) -> Iterable[Task]:
        """
        Лениво собирает данные из источника
        :return: Объекты Task
        """
        try:
            logger.info(f"Читаю файл по пути {self._path}")
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, (list, dict)):
                    raise SourceReadError(f"Содержание Json должно быть списком или словарем, получено: {type(data).__name__}")
        except OSError as e:
            raise SourceReadError(f"{self._path}: Системная ошибка при попытке прочитать файл: {e}")
        except json.decoder.JSONDecodeError as e:
            raise SourceReadError(f"{self._path}: Невалидный формат Json: {e}")

        items = data if isinstance(data, list) else [data]

        logger.info(f"Получены {len(items)} данных из {self._path}")

        for item in items:
            task = self._parse_item(item)
            if task is not None:
                yield task
