import asyncio

from task_processor.exceptions import ConfigError, InvalidTask
from task_processor.task import Task


class AsyncTaskQueue:
    """Асинхронная очередь задач"""

    def __init__(self, maxsize: int = 0):
        """
        :param maxsize: Максимальный размер очереди
        """
        if not isinstance(maxsize, int) or maxsize < 0:
            raise ConfigError("maxsize должно быть целым числом >= 0")

        self._queue = asyncio.Queue(maxsize=maxsize)

    @staticmethod
    def _validate_task(task: Task) -> None:
        if not isinstance(task, Task):
            raise InvalidTask(type(task).__name__)

    async def put(self, task: Task) -> None:
        """
        Асинхронно добавляет задачу в очередь

        :param task: Task
        """
        self._validate_task(task)
        await self._queue.put(task)

    async def get(self) -> Task:
        """
        Асинхронно забирает задачу из очереди
        """
        return await self._queue.get()

    def task_done(self) -> None:
        """
        Сообщает очереди, что ранее полученная задача обработана
        """
        self._queue.task_done()

    async def join(self) -> None:
        """
        Ожидает, пока все добавленные задачи будут обработаны
        """
        await self._queue.join()

    def qsize(self) -> int:
        """
        Возвращает текущее количество задач в очереди
        """
        return self._queue.qsize()

    def empty(self) -> bool:
        """
        Проверяет, пуста ли очередь
        """
        return self._queue.empty()
