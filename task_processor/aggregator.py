from typing import Iterable

from task_processor.protocol import TaskSource


class Aggregator:
    def __init__(self, sources: Iterable[TaskSource]):
        self._sources = sources

    def get_tasks(self):
        task_ids = set()

        for source in self._sources:
            if not isinstance(source, TaskSource):
                print(f"{source}: Не соответствует протоколу TaskSource")
                continue

            try:
                for task in source.get_tasks():
                    task_id = task.id

                    if task_id in task_ids:
                        print(f"ID {task_id} уже есть в задачах")
                        continue

                    task_ids.add(task_id)
                    yield task
            except Exception as e:
                print(e)
