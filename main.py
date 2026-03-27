import logging
import tempfile
import json
import task_processor.config

from task_processor.sources.file_source import JsonFileSource
from task_processor.sources.generator_source import GeneratorSource
from task_processor.sources.api_source import ApiSource
from task_processor.aggregator import Aggregator

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

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", encoding="utf-8", delete=True) as tmp:
        json.dump(demo_data, tmp, ensure_ascii=False, indent=2)
        tmp.flush()

        sources = [
            JsonFileSource(tmp.name),
            GeneratorSource(count=3),
            ApiSource(limit=5),
            "Я не источник, я просто строка для теста валидации"
        ]

        aggregator = Aggregator(sources)

        print("Начинаю сбор задач...\n")

        task_count = 0
        for task in aggregator.get_tasks():
            task_count += 1

            print(f"\n[{task_count}]")
            print(f"ID:         {task.id}")
            print(f"Desc:       {task.description}")
            print(f"Priority:   {task.priority}")
            print(f"Status:     {task.status}")
            print(f"Created at: {task.created_at}")
            print(f"Summary:    {task.summary}")
            print("-" * 40 + '\n')

        print(f"\nУспешно обработано уникальных задач: {task_count}\n")

    print("Конец Task Processor Demo")


if __name__ == "__main__":
    main()
