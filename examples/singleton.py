from contextlib import suppress

from python_additions import Singleton, SingletonError


def main() -> None:
    # the class inherits from Singleton
    class UniqueObject(Singleton):
        _name: str

        def __init__(self, name: str) -> None:
            self._name = name

        def get_name(self) -> str:
            return self._name

    # first constructor call
    uo = UniqueObject("Unique Object")

    with suppress(SingletonError):
        # calling the constructor more than once will raise a SingletonError
        _ = UniqueObject("Unique Object2")

    # use the reference directly or get it from the "INSTANCE" attribute of the class
    assert uo.get_name() == UniqueObject.INSTANCE.get_name()


if __name__ == "__main__":
    main()
