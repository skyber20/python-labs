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


class ValidationError(TaskProcessorError):
    """Валидационные исключения от дескрипторов"""
    pass


class StatusError(ValidationError):
    """Ошибка при переходе из одного статуса в другой"""
    def __init__(self, cur, value):
        super().__init__(f"Недопустимый переход: нельзя изменить статус из '{cur}' в '{value}'")
