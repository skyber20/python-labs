import pytest
from typing import Iterator

from task_processor.task import Task
from task_processor.queue import TaskQueue
from task_processor.exceptions import InvalidTask, ConfigError, ValidationError


@pytest.fixture
def sample_tasks():
    t1 = Task(description="task1", priority=2)
    t2 = Task(description="task2", priority=8, task_id="high")
    t2.status = "in_progress"
    t3 = Task(description="task3", priority=9, task_id="comp")
    t3.status = "in_progress"
    t3.status = "completed"
    t4 = Task(description="task4", priority=1)
    t4.status = "failed"
    return [t1, t2, t3, t4]


@pytest.fixture
def queue(sample_tasks):
    return TaskQueue(sample_tasks)


def test_init_empty():
    queue = TaskQueue()
    assert len(queue) == 0

def test_init_iterable(sample_tasks):
    queue = TaskQueue(sample_tasks)
    assert len(queue) == 4
    assert all(isinstance(t, Task) for t in queue)


def test_iter_and_len(queue):
    tasks = list(queue)
    assert len(tasks) == 4
    assert len(queue) == 4

def test_repeat_iteration(queue):
    list1 = list(queue)
    list2 = list(queue)
    assert list1 == list2


def test_add_valid(queue):
    new_task = Task("new", priority=5)
    queue.add_task(new_task)
    assert len(queue) == 5
    assert any(task.description == "new" for task in queue)

def test_add_invalid():
    queue = TaskQueue()
    with pytest.raises(InvalidTask):
        queue.add_task("Не таска")


def test_by_status(queue):
    created = list(queue.by_status("created"))
    assert len(created) == 1
    assert created[0].priority == 2

def test_filter_priority(queue):
    high = list(queue.by_priority(5))
    assert len(high) == 2
    priorities = [t.priority for t in high]
    assert all(p >= 5 for p in priorities)


def test_filter_general_and_laziness(queue):
    def is_high_prio(t: Task):
        return t.priority >= 5
    
    filt = queue.filter(is_high_prio)
    assert isinstance(filt, Iterator)
    high = list(filt)
    assert len(high) == 2

def test_filter_invalid_predicate(queue):
    with pytest.raises(ConfigError):
        list(queue.filter("not_callable"))

def test_filter_empty(queue):
    empty = list(queue.by_status("unknown"))
    assert len(empty) == 0
