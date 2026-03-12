import logging

from typing import Iterable, Any

from task_processor.protocol import TaskSource
from task_processor.task import Task
from task_processor.exceptions import InvalidSource, TaskProcessorError

logger = logging.getLogger(__name__)


class Aggregator:
    def __init__(self, sources: Iterable[Any] | None = None):
        """
        Агрегатор для сбора задач из различных источников, которые удовлетворяют протоколу TaskSource
        :param sources: Источники задач
        """
        self._sources = self._filter_protocol_sources(sources or [])

    @staticmethod
    def _filter_protocol_sources(sources: Iterable[Any]) -> Iterable[TaskSource]:
        """
        Фильтрация источников
        :param sources: Все переданные источники
        :return: Источники, удовлетворяющие TaskSource
        """
        protocol_sources = []
        for source in sources:
            if isinstance(source, TaskSource):
                protocol_sources.append(source)
            else:
                error = InvalidSource(type(source).__name__)
                logger.error(error)
        return protocol_sources

    def get_tasks(self) -> Iterable[Task]:
        """
        Лениво собирает данные из всех источников, прошедших валидацию
        :return: Объекты Task
        """
        ids = set()
        for source in self._sources:
            try:
                for task in source.get_tasks():
                    if not isinstance(task, Task):
                        logger.warning(f"Задача скипнута, так как {type(task).__name__} != {Task.__name__}")
                        continue

                    if task.id in ids:
                        logger.warning(f"Задача скипнута, так как {task.id} уже был")
                        continue

                    ids.add(task.id)
                    yield task
            except TaskProcessorError as e:
                logger.error(f"Ошибка TaskProcessor: {e}")
            except Exception as e:
                logger.error(f"Непредвиденная ошибка: {e}")
