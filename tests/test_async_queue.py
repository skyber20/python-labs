import asyncio

import pytest

from task_processor.async_queue import AsyncTaskQueue
from task_processor.exceptions import ConfigError, InvalidTask
from task_processor.task import Task


def test_async_queue_put_get_join():
    async def runner():
        queue = AsyncTaskQueue()
        task = Task("async task", priority=3)

        await queue.put(task)

        assert queue.qsize() == 1
        assert queue.empty() is False

        result = await queue.get()

        assert result is task
        assert queue.empty() is True

        queue.task_done()
        await queue.join()

    asyncio.run(runner())


def test_async_queue_rejects_invalid_task():
    async def runner():
        queue = AsyncTaskQueue()

        with pytest.raises(InvalidTask):
            await queue.put("not task")

    asyncio.run(runner())


def test_async_queue_rejects_invalid_maxsize():
    with pytest.raises(ConfigError):
        AsyncTaskQueue(maxsize=-1)
