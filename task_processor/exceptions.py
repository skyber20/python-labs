class TaskProcessorError(Exception):
    pass


class ConfigError(TaskProcessorError):
    pass


class SourceReadError(TaskProcessorError):
    pass


class ApiError(SourceReadError):
    pass


class InvalidSource(TaskProcessorError):
    # def __init__(self, source:):
    pass



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

