import pytest

from task_processor.task import Task
from task_processor.aggregator import Aggregator
from task_processor.exceptions import TaskProcessorError


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


class NoTasks:
    def get_tasks(self):
        return "строка строка"


class ExceptSource:
    def __init__(self, error_type):
        self.error_type = error_type
    def get_tasks(self):
        if self.error_type == 'task_proc':
            raise TaskProcessorError("Ошибка TaskProcessorError")
        raise Exception("Ошибка Exception")


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
    t1 = Task(id="1", payload="task 1")
    t2 = Task(id="2", payload="task 2")

    agg = Aggregator([MockInvalidSource([t1, t2])])

    assert f"MockInvalidSource: Не соответствует протоколу TaskSource" in caplog.text
    assert len(agg._sources) == 0


def test_aggregator_no_tasks(caplog):
    agg = Aggregator([NoTasks()])
    tasks = list(agg.get_tasks())

    assert "str != Task" in caplog.text
    assert len(tasks) == 0


def test_raise_exceptions(caplog):
    agg = Aggregator([ExceptSource("task_proc"), ExceptSource("else exception")])
    tasks = list(agg.get_tasks())

    assert len(tasks) == 0
    assert "Ошибка TaskProcessorError" in caplog.text
    assert "Ошибка Exception" in caplog.text
