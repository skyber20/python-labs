import pytest
from pathlib import Path
from task_processor.descriptors import Typed, IntRange, TaskStatus, ExistingFile
from task_processor.exceptions import ValidationError, StatusError, ConfigError


class MockEntity:
    t_field = Typed(int, allow_none=True)
    r_field = IntRange(min_value=1, max_value=10)
    status = TaskStatus()
    file = ExistingFile()


def test_typed_descriptor():
    obj = MockEntity()
    obj.t_field = 10
    assert obj.t_field == 10
    obj.t_field = None
    assert obj.t_field is None
    with pytest.raises(ValidationError):
        obj.t_field = "string"


def test_int_range_boundaries():
    obj = MockEntity()
    obj.r_field = 5
    with pytest.raises(ValidationError):
        obj.r_field = 0
    with pytest.raises(ValidationError):
        obj.r_field = 11


def test_task_status_transitions():
    obj = MockEntity()
    obj.status = "created"
    obj.status = "in_progress"
    obj.status = "completed"

    with pytest.raises(StatusError):
        obj.status = "created"

    with pytest.raises(ValidationError):
        obj.status = "unknown_status"


def test_existing_file_descriptor(tmp_path):
    obj = MockEntity()
    f = tmp_path / "test.txt"
    f.write_text("content")

    obj.file = str(f)
    assert Path(obj.file).name == "test.txt"

    with pytest.raises(ConfigError):
        obj.file = "non_existent_file.json"
