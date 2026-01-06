from typing import ClassVar, Self


class SingletonError(Exception):
    pass


class Singleton:
    INSTANCE: ClassVar[Self]

    def __new__(cls, *args, **kwargs):
        if hasattr(cls, "INSTANCE"):
            raise SingletonError(f"An instance of {cls.__name__} allready exists")
        else:
            cls.INSTANCE = super().__new__(cls)
            return cls.INSTANCE
