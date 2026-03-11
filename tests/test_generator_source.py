import pytest

from task_processor.sources.generator_source import GeneratorSource
from task_processor.task import Task
from task_processor.exceptions import ConfigError


def test_generator_source_success():
    cnt = 5
    prefix = "Test task"
    generator = GeneratorSource(cnt, prefix)

    tasks = list(generator.get_tasks())

    assert len(tasks) == cnt
    assert all(isinstance(task, Task) for task in tasks)
    assert tasks[0].payload.startswith(prefix)

    # Проверка на уникальность айдишников
    assert len(set(task.id for task in tasks)) == cnt


@pytest.mark.parametrize("invalid_count", [0, -1, "5", 10.4])
def test_generator_source_invalid_count(invalid_count):
    with pytest.raises(ConfigError):
        GeneratorSource(count=invalid_count)


@pytest.mark.parametrize("invalid_payload", [123, 123.5])
def test_generator_source_invalid_payload(invalid_payload):
    with pytest.raises(ConfigError):
        GeneratorSource(count=5, payload_default=invalid_payload)
