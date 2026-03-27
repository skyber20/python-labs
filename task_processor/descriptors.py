from typing import Any
from pathlib import Path

from task_processor.exceptions import ValidationError, StatusError, ConfigError


class BaseDescriptor:
    """Базовый дескриптор"""
    def __set_name__(self, owner: Any, name: str):
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self

        return getattr(instance, self.private_name, None)


class Typed(BaseDescriptor):
    """Дескриптор для проверки на соотвествие типов"""
    def __init__(self, expected_type: type | tuple[type, ...], allow_none: bool = False):
        self.expected_type = expected_type
        self.allow_none = allow_none

    def validate(self, value: Any):
        if value is None:
            if not self.allow_none:
                raise ValidationError(f"Поле {self.private_name[1:]} не может быть None")
            return

        if not isinstance(value, self.expected_type):
            raise ValidationError(
                f"Поле {self.private_name[1:]} должно быть {self.expected_type}, "
                f"а не {type(value).__name__}"
            )

    def __set__(self, instance: Any, value: Any):
        self.validate(value)
        object.__setattr__(instance, self.private_name, value)


class IntRange(Typed):
    """Дескриптор для проверки на соблюдение диапазона"""
    def __init__(self, min_value: int | None = None, max_value: int | None = None, allow_none: bool = False):
        super().__init__(int, allow_none)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any):
        super().validate(value)

        if value is None:
            return

        if self.min_value is not None and value < self.min_value:
            raise ValidationError(f"Значение {value} меньше минимума {self.min_value}")

        if self.max_value is not None and value > self.max_value:
            raise ValidationError(f"Значение {value} больше максимума {self.max_value}")


class TaskStatus(Typed):
    """Дескриптор для проверки на корректность переходов из статуса в другой статус"""
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

    _TRANSITIONS = {
        CREATED: [IN_PROGRESS, FAILED],
        IN_PROGRESS: [COMPLETED, FAILED],
        COMPLETED: [],
        FAILED: []
    }

    def __init__(self):
        super().__init__(str)

    def validate(self, value: Any):
        super().validate(value)
        if value not in self._TRANSITIONS:
            raise ValidationError(f"Неизвестный статус: {value}. Допустимые: {self._TRANSITIONS.keys()}")

    def __set__(self, instance: Any, value: Any):
        self.validate(value)

        current_status = getattr(instance, self.private_name, None)

        if current_status is not None:
            allowed_next_states = self._TRANSITIONS.get(current_status, [])
            if value not in allowed_next_states:
                raise StatusError(current_status, value)

        object.__setattr__(instance, self.private_name, value)


class ExistingFile(Typed):
    """Дескриптор для проверки существования пути"""
    def __init__(self):
        super().__init__((str, Path))

    def validate(self, value: Any):
        super().validate(value)

        if not Path(value).is_file():
            raise ConfigError(f"Путь '{value}' не существует или не является файлом")


class LazySummary(BaseDescriptor):
    """Non data дескриптор для ленивых вычислений и их кэширования. Обрезает payload"""
    def __get__(self, instance: Any, owner: Any) -> str:
        if instance is None:
            return self

        task_id = instance.id
        payload = instance.description

        short_payload = (payload[:20] + '...') if len(payload) > 20 else payload
        result = f"id={task_id}, payload={short_payload}"

        object.__setattr__(instance, self.private_name[1:], result)
        return result
