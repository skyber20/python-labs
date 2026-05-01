import asyncio

from task_processor.exceptions import ConfigError
from task_processor.task import Task


class DefaultTaskHandler:
    """Обработчик по умолчанию для любых задач"""

    def __init__(self, delay: float = 0.0):
        """
        :param delay: Неблокирующая задержка для демонстрации async обработки
        """
        if not isinstance(delay, (int, float)) or delay < 0:
            raise ConfigError("delay должно быть числом >= 0")

        self.delay = delay

    def can_handle(self, task: Task) -> bool:
        """
        Базовый обработчик принимает любую задачу
        """
        return isinstance(task, Task)

    async def handle(self, task: Task) -> None:
        """
        Демонстрирует неблокирующую обработку задачи
        """
        await asyncio.sleep(self.delay)
