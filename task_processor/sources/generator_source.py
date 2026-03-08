import uuid
import logging

from typing import Iterable

from task_processor.task import Task
from task_processor.exceptions import ConfigError

logger = logging.getLogger(__name__)


class GeneratorSource:
    def __init__(self, count: int, payload_default: str = "Payload number"):
        self._count = count
        self._payload_default = payload_default
        self._validate()
        logger.debug(f"Проинициализирован GeneratorSource(count={self._count}, payload_default={self._payload_default})")

    def _validate(self):
        if not isinstance(self._count, int):
            raise ConfigError("Параметр count должен быть целочисленным типом")

        if self._count <= 0:
            raise ConfigError("Параметр count должен быть положительным значением")

        if not isinstance(self._payload_default, str):
            raise ConfigError("Параметр payload_default должен быть строковым типом")

    def get_tasks(self) -> Iterable[Task]:
        logger.info(f"Генерирую задачи ({self._count})")
        for i in range(self._count):
            task_id = uuid.uuid4().hex
            payload = f"{self._payload_default} #{i + 1}"

            yield Task(task_id, payload)
