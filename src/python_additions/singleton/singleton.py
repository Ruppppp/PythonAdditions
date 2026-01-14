from typing import ClassVar, Final, Self

_INSTANCE_VAR_NAME: Final = "INSTANCE"


class SingletonError(Exception):
    """Raised whenever a `Singleton` class constructor is called twice."""


class SingletonMeta(type):
    """Metaclass that protects the `INSTANCE` attribute of singletons."""

    def __setattr__(cls, name, value):
        """Prevents `INSTANCE` from being rewritten."""
        if name == _INSTANCE_VAR_NAME and hasattr(cls, _INSTANCE_VAR_NAME):
            raise SingletonError(f"An instance of {cls.__name__} already exists.")
        super().__setattr__(name, value)


class Singleton(metaclass=SingletonMeta):
    """Allow simple singleton pattern, every `Singleton` class has an `INSTANCE` attribute that returns the current instance of the singleton."""

    INSTANCE: ClassVar[Self]

    def __new__(cls, *args, **kwargs) -> Self:
        cls.INSTANCE = super().__new__(cls)
        return cls.INSTANCE

    @classmethod
    def has_instance(cls) -> bool:
        return hasattr(cls, _INSTANCE_VAR_NAME)
