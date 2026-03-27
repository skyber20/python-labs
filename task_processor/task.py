import uuid
from datetime import datetime
from typing import Any
from task_processor.descriptors import IntRange, TaskStatus, Typed, LazySummary


class Task:
    """Доменная модель задач"""
    description = Typed((str, dict, list))
    priority = IntRange(min_value=0, max_value=10)
    status = TaskStatus()

    summary = LazySummary()

    def __init__(
        self,
        description: Any,
        priority: int = 0,
        task_id: str | None = None
    ):
        self._task_id = str(task_id) if task_id is not None else uuid.uuid4().hex
        self._created_at = datetime.now()
        self.description = description
        self.priority = priority
        self.status = "created"

    @property
    def id(self) -> str:
        return self._task_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def is_success(self) -> bool:
        return self.status == "completed"

    def __repr__(self) -> str:
        return f"Task(id={self._task_id}, status={self.status}, priority={self.priority})"
