import asyncio

import pytest

from task_processor.async_queue import AsyncTaskQueue
from task_processor.exceptions import ConfigError, InvalidHandler
from task_processor.executor import AsyncTaskExecutor
from task_processor.handlers import DefaultTaskHandler
from task_processor.protocol import TaskHandler
from task_processor.task import Task


async def fill_queue(queue: AsyncTaskQueue, tasks: list[Task]) -> None:
    for task in tasks:
        await queue.put(task)


class FakeHandler:
    def __init__(
        self,
        can_handle: bool = True,
        delay: float = 0.0,
        fail_description: str | None = None
    ):
        self.available = can_handle
        self.delay = delay
        self.fail_description = fail_description
        self.tasks = []

    def can_handle(self, task: Task) -> bool:
        return self.available

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(self.delay)
        if task.description == self.fail_description:
            raise RuntimeError("boom")

        self.tasks.append(task.id)


class SyncHandler:
    def can_handle(self, task: Task) -> bool:
        return True

    def handle(self, task: Task) -> None:
        return None


def test_default_handler_satisfies_protocol():
    handler = DefaultTaskHandler()

    assert isinstance(handler, TaskHandler)


def test_default_handler_rejects_invalid_delay():
    with pytest.raises(ConfigError):
        DefaultTaskHandler(delay=-1)


def test_executor_rejects_invalid_handler():
    queue = AsyncTaskQueue()

    with pytest.raises(InvalidHandler):
        AsyncTaskExecutor(queue, [object()])

    with pytest.raises(InvalidHandler):
        AsyncTaskExecutor(queue, [SyncHandler()])


def test_executor_rejects_invalid_worker_count():
    queue = AsyncTaskQueue()

    with pytest.raises(ConfigError):
        AsyncTaskExecutor(queue, [DefaultTaskHandler()], worker_count=0)


def test_executor_completes_tasks():
    async def runner():
        tasks = [
            Task("one", task_id="one"),
            Task("two", task_id="two"),
        ]
        queue = AsyncTaskQueue()
        handler = FakeHandler()

        async with AsyncTaskExecutor(queue, [handler], worker_count=2) as executor:
            await fill_queue(queue, tasks)
            await executor.run()

        assert [task.status for task in tasks] == ["completed", "completed"]
        assert sorted(handler.tasks) == ["one", "two"]

    asyncio.run(runner())


def test_executor_marks_failed_and_continues(caplog):
    async def runner():
        bad_task = Task("bad", task_id="bad")
        good_task = Task("good", task_id="good")
        queue = AsyncTaskQueue()
        handler = FakeHandler(fail_description="bad")

        async with AsyncTaskExecutor(queue, [handler], worker_count=2) as executor:
            await fill_queue(queue, [bad_task, good_task])
            await executor.run()

        assert bad_task.status == "failed"
        assert good_task.status == "completed"
        assert handler.tasks == ["good"]

    asyncio.run(runner())

    assert "Ошибка при обработке задачи bad" in caplog.text


def test_executor_marks_failed_when_no_handler(caplog):
    async def runner():
        task = Task("unknown", task_id="unknown")
        queue = AsyncTaskQueue()

        async with AsyncTaskExecutor(queue, [FakeHandler(can_handle=False)]) as executor:
            await fill_queue(queue, [task])
            await executor.run()

        assert task.status == "failed"

    asyncio.run(runner())

    assert "не найден обработчик" in caplog.text
