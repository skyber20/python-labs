import pytest
from datetime import datetime
from task_processor.task import Task
from task_processor.exceptions import ValidationError, StatusError


def test_task_initialization():
    task = Task(description="Test", priority=5, task_id="t_id")
    assert task.id == "t_id"
    assert task.priority == 5
    assert task.status == "created"
    assert task.is_success is False


def test_task_default_values():
    task = Task(description="Просто таска")
    assert task.priority == 0
    assert len(task.id) == 32
    assert task.status == "created"


def test_task_read_only_properties():
    task = Task(description="Test")

    with pytest.raises(AttributeError):
        task.id = "new_id"

    with pytest.raises(AttributeError):
        task.created_at = datetime.now()


def test_task_priority_validation():
    task = Task(description="Test")
    task.priority = 10

    with pytest.raises(ValidationError):
        task.priority = -1

    with pytest.raises(ValidationError):
        task.priority = 111


def test_task_status_transitions():
    task = Task(description="Test")

    task.status = "in_progress"
    assert task.status == "in_progress"

    task.status = "completed"
    assert task.status == "completed"
    assert task.is_success is True

    with pytest.raises(StatusError):
        task.status = "created"


def test_task_summary_lazy_loading():
    task = Task(description="Дофига длиннннннноооооооеееее описааааанииииииеее тааски", task_id="777")

    s = task.summary
    assert "id=777" in s
    assert "ииииеее тааски" not in s
