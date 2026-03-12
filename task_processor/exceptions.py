class TaskProcessorError(Exception):
    """Общий класс исключений"""


class ConfigError(TaskProcessorError):
    """Ошибка при передаче некорректных параметров"""


class SourceReadError(TaskProcessorError):
    """Ошибка, возникающая в процессе чтения данных из источника"""


class ApiError(SourceReadError):
    """Ошибка при взаимодействии с API"""


class InvalidSource(TaskProcessorError):
    """Исключение при несоотвествии источника протоколу TaskSource"""
    def __init__(self, source: str):
        super().__init__(f"{source}: Не соответствует протоколу TaskSource")
