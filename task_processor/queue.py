from typing import Iterable, Iterator, Callable
from task_processor.task import Task
from task_processor.exceptions import InvalidTask, ConfigError


class TaskQueue:
    """
    Очередь задач, поддерживающая итерацию, повторный обход и ленивую фильтрацию
    """

    def __init__(self, tasks: Iterable[Task] | None = None):
        """
        :param tasks: Итерируемый объект с Taskами
        """
        self._tasks = list(tasks or [])

    def __iter__(self) -> Iterator[Task]:
        """
        Возвращает новый итератор. Позволяет делать повторный обход
        """
        return iter(self._tasks)

    def __len__(self) -> int:
        """
        Возвращает количество задач в очереди
        """
        return len(self._tasks)

    def add_task(self, task: Task) -> None:
        """
        Добавляет задачу в очередь

        :param task: Task
        """
        if not isinstance(task, Task):
            raise InvalidTask(type(task).__name__)
        self._tasks.append(task)

    def by_status(self, status: str) -> Iterator[Task]:
        """
        Ленивый фильтр по статусу задачи

        :param status: Статус задачи ('created', 'in_progress' и тд)
        :return: Генератор задач с указанным статусом
        """
        equals_status = lambda t: t.status == status
        return self.filter(equals_status)

    def by_priority(self, priority: int, direct: str = 'up') -> Iterator[Task]:
        """
        Ленивый фильтр по приоритету.

        direct='up' вернет задачи с приоритетом >= priority.
        direct='down' вернет задачи с приоритетом <= priority.
        """
        if not isinstance(priority, int) or priority < 0 or priority > 10:
            raise ConfigError("priority должно быть целым числом в диапазоне 0-10")

        if direct not in ("up", "down"):
            raise ConfigError("direct должен быть up или down")

        if direct == "up":
            func = lambda t: t.priority >= priority
        else:
            func = lambda t: t.priority <= priority
        return self.filter(func)

    def filter(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """
        Универсальный ленивый фильтр

        :param predicate: Функция предикат, возвращающая булевое значение для Task
        :return: Генератор отфильтрованных задач
        """
        if not callable(predicate):
            raise ConfigError("Предикат должен быть callable")

        for task in self:
            if predicate(task):
                yield task
