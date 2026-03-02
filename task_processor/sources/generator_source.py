import uuid

from typing import Any, Iterable

from task_processor.task import Task
from task_processor.exceptions import NegativeValue


class GeneratorSource:
    def __init__(self, count: int, payload_default: Any = "Payload number"):
        if count <= 0:
            raise NegativeValue("count")

        self.count = count
        self.payload_default = payload_default

    def get_tasks(self) -> Iterable[Task]:
        for i in range(self.count):
            task_id = uuid.uuid4().hex
            payload = self.payload_default + f" {i + 1}"
            yield Task(task_id, payload)
