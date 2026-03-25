from typing import Any

from task_processor.exceptions import ValidationError


class BaseDescriptor:
    def __set_name__(self, owner: Any, name: str):
        self.private_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self

        return getattr(instance, self.private_name, None)


class Typed(BaseDescriptor):
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
