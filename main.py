import tempfile
import json
import logging

from task_processor.sources.file_source import JsonFileSource
from task_processor.sources.generator_source import GeneratorSource
from task_processor.sources.api_source import ApiSource
from task_processor.aggregator import Aggregator
from task_processor.queue import TaskQueue

logger = logging.getLogger(__name__)


def main():
    """Демоверсия работы Task Processor"""

    print("Начало Task Processor Demo:\n")

    demo_data = [
        {"id": "file_1", "payload": "Описание к таске 1"},
        {"id": "file_1", "payload": "Дубликат id, должен быть отсеян"},
        {"payload": "Описание таски без заданного айдишника, так что будет сгенерирован через uuid"},
        "строка строка будет отсеяна"
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=False) as tmp:
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
            print(f"[{i}] ID: {task.id}, Status: {task.status}, Priority: {task.priority}, Desc: {task.description[:30]}...")

        print(f"\nВсего задач в очереди: {len(queue)}")
        print(f"Задач с высоким приоритетом (>=5): {len(list(queue.high_priority(3)))}")
        print(f"Задач со статусом 'created': {len(list(queue.by_status('created')))}")
        print(f"Сумма приоритетов: {sum(task.priority for task in queue)}")

if __name__ == "__main__":
    main()
