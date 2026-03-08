from typing import Iterable

from task_processor.protocol import TaskSource


class Aggregator:
    def __init__(self, sources: Iterable[TaskSource]):
        self._sources = sources

    def _filter_protocol_sources(self):
        pass
