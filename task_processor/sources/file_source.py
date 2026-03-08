import json

from pathlib import Path
from typing import Iterable

from task_processor.task import Task
from task_processor.exceptions import IsNotJsonFile, PathNotFound, IncorrectFormatJson


class JsonFileSource:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self._validate()

    def _validate(self) -> None:
        if not self.path.exists():
            raise PathNotFound(self.path)

        if not self.path.is_file() or self.path.suffix != ".json":
            raise IsNotJsonFile(self.path)

    def get_tasks(self) -> Iterable[Task]:
        with open(self.path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.decoder.JSONDecodeError:
                raise IncorrectFormatJson(self.path, "Невалидный синтаксис JSON")

            if isinstance(data, dict):
                items = [data]
            elif isinstance(data, list):
                items = data
            else:
                raise IncorrectFormatJson(self.path, f"Невозможно распарсить {type(data)}")

            for item in items:
                if not isinstance(item, dict):
                    continue

                task_id = item.get("id", None)
                payload = item.get("payload", None)

                if task_id is not None and payload is not None:
                    yield Task(str(task_id), payload)
