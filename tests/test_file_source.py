import pytest

from task_processor.task import Task
from task_processor.sources.file_source import JsonFileSource
from task_processor.exceptions import ConfigError, SourceReadError


def test_file_source_success_list(tmp_path):
    f = tmp_path / "tasks.json"
    f.write_text('[{"id": 1, "payload": "Test1"}, {"id": 2, "payload": []}]')

    file_source = JsonFileSource(path=f)
    tasks = list(file_source.get_tasks())

    assert len(tasks) == 2
    assert all(isinstance(task, Task) for task in tasks)
    assert tasks[0].id == "1"
    assert tasks[0].description == "Test1"


def test_file_source_success_single(tmp_path):
    f = tmp_path / "tasks.json"
    f.write_text('{"id": 1, "payload": "Test1"}')

    file_source = JsonFileSource(path=f)
    tasks = list(file_source.get_tasks())

    assert len(tasks) == 1
    assert isinstance(tasks[0], Task)
    assert tasks[0].id == "1"
    assert tasks[0].description == "Test1"


def test_file_source_invalid_json_format(tmp_path):
    f = tmp_path / "trash.json"
    f.write_text("123")

    file_source = JsonFileSource(f)
    with pytest.raises(SourceReadError):
        list(file_source.get_tasks())


def test_file_source_not_found():
    with pytest.raises(ConfigError):
        JsonFileSource("not_exist.json")


def test_file_source_skips_bad_items(tmp_path):
    f = tmp_path / "mixed.json"

    f.write_text('[{"id": 1, "payload": "ok"}, {"id": "two"}, "just a string"]')

    file_source = JsonFileSource(f)
    tasks = list(file_source.get_tasks())

    assert len(tasks) == 2
    assert tasks[0].id == "1"
    assert tasks[1].id == "two"


def test_file_source_invalid_json(tmp_path):
    f = tmp_path / "invalid.json"
    f.write_text('{id: 1, "payload": "task"}')

    file_source = JsonFileSource(f)
    with pytest.raises(SourceReadError) as e:
        list(file_source.get_tasks())

    assert "Невалидный формат Json" in str(e)

