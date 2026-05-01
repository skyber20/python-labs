import asyncio
import json
import tempfile
from typing import Iterable

from task_processor.aggregator import Aggregator
from task_processor.async_queue import AsyncTaskQueue
from task_processor.config import logger as task_processor_logger
from task_processor.executor import AsyncTaskExecutor
from task_processor.handlers import DefaultTaskHandler
from task_processor.queue import TaskQueue
from task_processor.sources.api_source import ApiSource
from task_processor.sources.file_source import JsonFileSource
from task_processor.sources.generator_source import GeneratorSource
from task_processor.task import Task


async def feed_tasks(async_queue: AsyncTaskQueue, tasks: Iterable[Task]) -> None:
    """Передает задачи из синхронного iterable в асинхронную очередь"""
    for task in tasks:
        await async_queue.put(task)


async def process_tasks(tasks: Iterable[Task]) -> None:
    """Асинхронно обрабатывает переданные задачи"""
    worker_count = 3
    async_queue = AsyncTaskQueue(maxsize=worker_count)

    async with AsyncTaskExecutor(
        async_queue,
        [DefaultTaskHandler(delay=0.01)],
        worker_count=worker_count
    ) as executor:
        producer = asyncio.create_task(feed_tasks(async_queue, tasks))
        await producer
        await executor.run()


def main() -> None:
    """Демоверсия работы Task Processor"""
    task_processor_logger.info("Запуск Task Processor Demo")

    print("Начало Task Processor Demo:\n")

    demo_data = [
        {"id": "file_1", "payload": "Описание к таске 1", "priority": 9},
        {"id": "file_1", "payload": "Дубликат id, должен быть отсеян", "priority": 9},
        {
            "payload": "Описание таски без заданного айдишника, "
            "так что будет сгенерирован через uuid",
            "priority": 4
        },
        "строка строка будет отсеяна"
    ]

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        encoding="utf-8",
        delete=False
    ) as tmp:
        json.dump(demo_data, tmp, ensure_ascii=False, indent=2)
        tmp.flush()

        sources = [
            JsonFileSource(tmp.name),
            GeneratorSource(count=3),
            ApiSource(limit=5),
        ]

        aggregator = Aggregator(sources)
        queue = TaskQueue(aggregator.get_tasks())

        print("Задачи в очереди:")
        for i, task in enumerate(queue, 1):
            print(
                f"[{i}] ID: {task.id}, Status: {task.status}, "
                f"Priority: {task.priority}, Desc: {task.description[:30]}..."
            )

        print(f"\nВсего задач в очереди: {len(queue)}")
        print(f"Задач с высоким приоритетом (>=6): {len(list(queue.by_priority(6)))}")
        print(f"Задач со статусом 'created': {len(list(queue.by_status('created')))}")
        print(f"Сумма приоритетов: {sum(task.priority for task in queue)}")

        asyncio.run(process_tasks(queue.by_priority(6)))

        print("\nСтатусы после асинхронной обработки:")
        for i, task in enumerate(queue, 1):
            print(f"[{i}] ID: {task.id}, Status: {task.status}")


if __name__ == "__main__":
    main()
