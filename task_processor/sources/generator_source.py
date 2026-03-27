import uuid
import logging
import random

from typing import Iterable

from task_processor.task import Task
from task_processor.descriptors import IntRange, Typed

logger = logging.getLogger(__name__)


class GeneratorSource:
    """Класс источника, который генерирует данные типа Task"""
    count = IntRange(min_value=1)
    payload_default = Typed(str)

    def __init__(self, count: int, payload_default: str = "Payload number"):
        """
        :param count: Количество задач, которые нужно сгенерить
        :param payload_default: Описание задачи по дэфолту
        """
        self.count = count
        self.payload_default = payload_default
        logger.debug(f"Проинициализирован GeneratorSource(count={self.count}, payload_default={self.payload_default})")

    def get_tasks(self) -> Iterable[Task]:
        """
        Лениво собирает данные из источника
        :return: Объекты Task
        """
        logger.info(f"Генерирую задачи ({self.count})")
        for i in range(self.count):
            task_id = uuid.uuid4().hex
            payload = f"{self.payload_default} #{i + 1}"
            priority = random.randint(1, 10)

            yield Task(payload, priority, task_id)
