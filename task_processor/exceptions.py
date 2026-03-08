from pathlib import Path
from typing import Any


class TaskProcessorError(Exception):
    pass


class ConfigError(TaskProcessorError):
    pass


class ConfigTypeError(ConfigError):
    def __init__(self, param: str, type_param: Any, need_type: str):
        msg = f"Параметр '{param}' должен быть {need_type}, а не {type_param}"
        super().__init__(msg)


class ConfigValueError(ConfigError):
    def __init__(self, param: str, reason: str):
        msg = f"Значение параметра '{param}' недопустимо: {reason}"
        super().__init__(msg)


class PathNotFound(ConfigError):
    def __init__(self, path: Path | str):
        super().__init__(f"{path}: Путь не найден")


class IsNotJsonFile(ConfigError):
    def __init__(self, path: Path | str):
        super().__init__(f"{path}: Это не JSON файл")


class NegativeValue(ConfigError):
    def __init__(self, param: str):
        super().__init__(f"Значение {param} должно быть больше 0")


class DataSourceError(TaskProcessorError):
    pass


class IncorrectFormatJson(DataSourceError):
    def __init__(self, path: Path | str, reason: str):
        super().__init__(f"{path}: {reason}")


class ApiError(DataSourceError):
    def __init__(self, reason: str):
        super().__init__(f"Не получилось получить задачи по API: {reason}")






#
#
# class InvalidSource(Exception):
#     def __init__(self, source: Any):
#         super().__init__(f"{source}: Не прошел протокол TaskSource")
#
#
# class DuplicateIds(Exception):
#     def __init__(self, task_id: str):
#         super().__init__(self, f"{task_id}: Айдишники совпали")

