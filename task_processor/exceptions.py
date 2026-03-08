class TaskProcessorError(Exception):
    pass


class ConfigError(TaskProcessorError):
    pass


class SourceReadError(TaskProcessorError):
    pass


class ApiError(SourceReadError):
    pass


class InvalidSource(TaskProcessorError):
    def __init__(self, source: str):
        super().__init__(f"{source}: Не соответствует протоколу TaskSource")
