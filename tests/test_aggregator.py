import pytest

from task_processor.task import Task
from task_processor.protocol import TaskSource
from task_processor.aggregator import Aggregator


class MockSource:
    def __init__(self, tasks):
        self.tasks = tasks
    def get_tasks(self):
        yield from self.tasks


class MockInvalidSource:
    def __init__(self, tasks):
        self.tasks = tasks
    def invalid_get(self):
        yield from self.tasks


def test_aggregator_success():
    t1 = Task(id="one", payload="task 1")
    t2 = Task(id="2", payload="task 2")

    agg = Aggregator([MockSource([t1, t2])])
    tasks = list(agg.get_tasks())

    assert len(tasks) == 2
    assert tasks[0].id == "one"
    assert tasks[1].payload == "task 2"


def test_duplicate_ids():
    t1 = Task(id="1", payload="task 1")
    t2 = Task(id="2", payload="task 2")
    t3 = Task(id="1", payload="task 3")

    agg = Aggregator([MockSource([t1, t2, t3])])
    tasks = list(agg.get_tasks())

    assert len(tasks) == 2


def test_invalid_sources(caplog):
    import logging

    with caplog.at_level(logging.ERROR):
        t1 = Task(id="1", payload="task 1")
        t2 = Task(id="2", payload="task 2")

        agg = Aggregator([MockInvalidSource([t1, t2])])

        assert f"MockInvalidSource: Не соответствует протоколу TaskSource" in caplog.text
        assert len(agg._sources) == 0
