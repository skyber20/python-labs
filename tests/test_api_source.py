import httpx
import pytest

from unittest.mock import MagicMock, patch

from task_processor.task import Task
from task_processor.sources.api_source import ApiSource
from task_processor.exceptions import ApiError, ConfigError


def test_api_source_init_valid():
    source = ApiSource(url="https://test.com", timeout=10, limit=50)
    assert source._url == "https://test.com"
    assert source._timeout == 10
    assert source._limit == 50


@pytest.mark.parametrize("url, timeout, limit", [
    (123, 5, 10),
    ("http://ok.com", "5", 10),
    ("http://ok.com", -1, 10),
    ("http://ok.com", 5, "10"),
    ("http://ok.com", 5, -5),
])
def test_api_source_init_invalid(url, timeout, limit):
    with pytest.raises(ConfigError):
        ApiSource(url=url, timeout=timeout, limit=limit)


@patch("httpx.Client.get")
def test_api_source_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 1, "title": "Task 1"},
        {"id": 2, "title": "Task 2"}
    ]

    mock_get.return_value = mock_response

    api_source = ApiSource()
    tasks = list(api_source.get_tasks())

    assert len(tasks) == 2
    assert all(isinstance(task, Task) for task in tasks)
    assert tasks[0].id == "1"
    assert tasks[1].payload == "Task 2"


@patch("httpx.Client.get")
def test_api_source_limit(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"id": i, "title": f"Задача из API {i}"} for i in range(10)]

    mock_get.return_value = mock_response

    api_source = ApiSource(limit=3)
    tasks = list(api_source.get_tasks())

    assert len(tasks) == 3

    for i in range(3):
        assert tasks[i].id == str(i)
        assert tasks[i].payload == f"Задача из API {i}"


@patch("httpx.Client.get")
def test_api_source_connection_error(mock_get):
    mock_get.side_effect = httpx.ConnectError("Ошибка соединения")

    api_source = ApiSource()

    with pytest.raises(ApiError) as e:
        list(api_source.get_tasks())

    assert "Ошибка при обращении к API" in str(e.value)


@patch("httpx.Client.get")
def test_api_source_status_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=MagicMock(), response=mock_response
    )

    mock_get.return_value = mock_response

    api_source = ApiSource()
    with pytest.raises(ApiError):
        list(api_source.get_tasks())
        