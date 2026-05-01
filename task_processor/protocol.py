from typing import Protocol, runtime_checkable, Iterable
from task_processor.task import Task


@runtime_checkable
class TaskSource(Protocol):
    def get_tasks(self) -> Iterable[Task]: ...


@runtime_checkable
class TaskHandler(Protocol):
    def can_handle(self, task: Task) -> bool: ...

    async def handle(self, task: Task) -> None: ...
