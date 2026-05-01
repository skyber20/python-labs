import asyncio
import inspect
import logging
from types import TracebackType
from typing import Iterable

from task_processor.async_queue import AsyncTaskQueue
from task_processor.exceptions import ConfigError, InvalidHandler, StatusError
from task_processor.protocol import TaskHandler
from task_processor.task import Task

logger = logging.getLogger(__name__)


class AsyncTaskExecutor:
    """Асинхронный исполнитель задач с расширяемыми обработчиками"""

    def __init__(
        self,
        queue: AsyncTaskQueue,
        handlers: Iterable[TaskHandler],
        worker_count: int = 1
    ):
        """
        :param queue: Асинхронная очередь задач
        :param handlers: Обработчики, удовлетворяющие TaskHandler
        :param worker_count: Количество воркеров
        """
        if not isinstance(queue, AsyncTaskQueue):
            raise ConfigError("queue должна быть AsyncTaskQueue")

        if not isinstance(worker_count, int) or worker_count < 1:
            raise ConfigError("worker_count должно быть целым числом >= 1")

        self.queue = queue
        self.handlers = self._validate_handlers(handlers)
        self.worker_count = worker_count
        self._workers = []

    async def __aenter__(self) -> "AsyncTaskExecutor":
        """Запускает executor при входе в async with"""
        await self.start()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None
    ) -> bool:
        """Останавливает executor при выходе из async with"""
        await self.stop()
        return False

    @staticmethod
    def _validate_handlers(handlers: Iterable[TaskHandler]) -> list[TaskHandler]:
        """Проверяет, что обработчики подходят под TaskHandler"""
        valid_handlers = []

        for handler in handlers:
            if (
                not isinstance(handler, TaskHandler)
                or not inspect.iscoroutinefunction(handler.handle)
            ):
                raise InvalidHandler(type(handler).__name__)

            valid_handlers.append(handler)

        return valid_handlers

    async def start(self) -> None:
        """
        Запускает воркеры executor-а
        """
        if self._workers:
            return

        logger.info(f"Запускаю AsyncTaskExecutor, worker_count={self.worker_count}")

        for index in range(self.worker_count):
            worker = asyncio.create_task(self._worker(index + 1))
            self._workers.append(worker)

    async def stop(self) -> None:
        """
        Останавливает воркеры executor-а
        """
        if not self._workers:
            return

        for worker in self._workers:
            worker.cancel()

        await asyncio.gather(*self._workers, return_exceptions=True)
        self._workers.clear()
        logger.info("AsyncTaskExecutor остановлен")

    async def run(self) -> None:
        """
        Запускает обработку, если нужно, и ждёт завершения всех задач очереди
        """
        started_here = not self._workers

        if started_here:
            await self.start()

        try:
            await self.queue.join()
        finally:
            if started_here:
                await self.stop()

    async def _worker(self, number: int) -> None:
        """Берет задачи из очереди и передает их в обработку"""
        while True:
            task = await self.queue.get()
            try:
                await self._process_task(task)
            finally:
                self.queue.task_done()
                logger.info(f"Воркер {number} завершил задачу {task.id}")

    async def _process_task(self, task: Task) -> None:
        """Обрабатывает одну задачу и меняет ее статус"""
        handler = self._find_handler(task)

        if handler is None:
            logger.warning(f"Для задачи {task.id} не найден обработчик")
            self._mark_failed(task)
            return

        try:
            self._mark_in_progress(task)
            await handler.handle(task)
            self._mark_completed(task)
            logger.info(f"Задача {task.id} успешно обработана")
        except Exception as e:
            self._mark_failed(task)
            logger.error(f"Ошибка при обработке задачи {task.id}: {e}")

    def _find_handler(self, task: Task) -> TaskHandler | None:
        """Ищет первый подходящий обработчик для задачи"""
        for handler in self.handlers:
            try:
                if handler.can_handle(task):
                    return handler
            except Exception as e:
                logger.error(f"Ошибка проверки обработчика {type(handler).__name__}: {e}")

        return None

    @staticmethod
    def _mark_in_progress(task: Task) -> None:
        """Переводит задачу в работу"""
        if task.status == "created":
            task.status = "in_progress"
            return

        if task.status != "in_progress":
            raise StatusError(task.status, "in_progress")

    @staticmethod
    def _mark_completed(task: Task) -> None:
        """Помечает задачу выполненной"""
        if task.status == "in_progress":
            task.status = "completed"
            return

        if task.status != "completed":
            raise StatusError(task.status, "completed")

    @staticmethod
    def _mark_failed(task: Task) -> None:
        """Помечает задачу упавшей"""
        if task.status in ("created", "in_progress"):
            task.status = "failed"
