from typing import ClassVar, Self


class SingletonError(Exception):
    """Raised whenever a `Singleton` class constructor is called twice.
    """
    pass


class Singleton:
    """Allow simple singleton pattern, every `Singleton` class has an `INSTANCE` attribute that returns the current instance of the singleton.
    """
    INSTANCE: ClassVar[Self]

    def __new__(cls, *args, **kwargs) -> Self:
        """Assure only one instance of the class exists at any given time.
        """
        if hasattr(cls, "INSTANCE"):
            raise SingletonError(f"An instance of {cls.__name__} allready exists")
        else:
            cls.INSTANCE = super().__new__(cls)
            return cls.INSTANCE
