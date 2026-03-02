from pathlib import Path
from typing import Any


class PathNotFound(Exception):
    def __init__(self, path: Path):
        super().__init__(f"{path}: Путь не найден")


class IsNotJsonFile(Exception):
    def __init__(self, path: Path):
        super().__init__(f"{path}: Это не JSON файл")


class IncorrectFormatJson(Exception):
    def __init__(self, path: Path, msg: str):
        super().__init__(f"{path}: {msg}")


class NegativeValue(Exception):
    def __init__(self, param: str):
        super().__init__(f"Значение {param} должно быть больше 0")


class FailGetData(Exception):
    def __init__(self, msg: str):
        super().__init__(f"Не получилось получить задачи: {msg}")

