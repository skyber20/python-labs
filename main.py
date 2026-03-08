import logging

import task_processor.config

from task_processor.sources.file_source import JsonFileSource
from task_processor.sources.generator_source import GeneratorSource
from task_processor.sources.api_source import ApiSource
from task_processor.aggregator import Aggregator

logger = logging.getLogger(__name__)


def main():
    print("Начало Task Processor Demo:\n")

    sources = [
        JsonFileSource("data/good_with_bad_tasks.json"),
        GeneratorSource(count=3),
        ApiSource(limit=5),
        "Я не источник, я просто строка для теста валидации"
    ]

    aggregator = Aggregator(sources)

    print("Начинаю сбор задач...\n")

    task_count = 0
    for task in aggregator.get_tasks():
        task_count += 1
        print(f"[{task_count}] ID: {task.id} | Payload: {task.payload}\n")

    print(f"\nУспешно обработано уникальных задач: {task_count}\n")
    print("Конец Task Processor Demo")


if __name__ == "__main__":
    main()
