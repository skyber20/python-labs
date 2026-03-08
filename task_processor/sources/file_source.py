import json

from pathlib import Path
from typing import Iterable, Any

from task_processor.task import Task
from task_processor.exceptions import ConfigError, SourceReadError



class JsonFileSource:
    def __init__(self, path: str | Path):
        self._path = Path(path)
        self._validate()

    def _validate(self) -> None:
        if not self._path.is_file():
            raise ConfigError(f"{self._path}: Путь не существует или не является файлом")

    @staticmethod
    def _parse_item(item: Any) -> Task | None:
        if isinstance(item, dict):
            task_id = item.get("id")
            payload = item.get("payload")

            if task_id is not None and payload is not None:
                return Task(str(task_id), payload)

        return None

    def get_tasks(self) -> Iterable[Task]:
        try:
            with open(self._path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except OSError as e:
            raise SourceReadError(f"{self._path}: Системная ошибка при попытке прочитать файл: {e}")
        except json.decoder.JSONDecodeError as e:
            raise SourceReadError(f"{self._path}: Невалидный формат Json: {e}")

        items = data if isinstance(data, list) else [data]

        for item in items:
            task = self._parse_item(item)
            if task is not None:
                yield task
