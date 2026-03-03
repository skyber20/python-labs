from typing import runtime_checkable, Iterable, Any

from task_processor.protocol import TaskSource
from task_processor.exceptions import InvalidSource, DuplicateIds


def validate_source(source: Any):
    if not isinstance(source, TaskSource):
        raise InvalidSource(source)


class Aggregator:
    def __init__(self, sources: Iterable[TaskSource]):
        self._sources = sources

    def get_tasks(self):
        task_ids = set()

        for source in self._sources:
            try:
                validate_source(source)

                for task in source.get_tasks():
                    task_id = task.id

                    if task_id in task_ids:
                        continue
                        raise DuplicateIds(task_id)
                    task_ids.add(task_id)
                    yield task
            except (InvalidSource, DuplicateIds) as e:
                print(e)
