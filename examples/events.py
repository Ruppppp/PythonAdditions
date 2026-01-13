from python_additions import DataEvent, Event


def main() -> None:

    # ---------- Events ----------

    def func1() -> None:
        print("Hello World! (from func1)")

    def func2() -> int:
        print("Hello World! (from func2)")
        return 2

    event = Event()  # basic event
    event.subscribe(func1)  # subscribe methods to event
    event += func2  # subscriptions also works with +=
    result = event.invoke()  # this will call func1 and func2
    assert result == [
        None,
        2,
    ]  # corresponds to every returned object of every subscribed method, in order of subscription

    event.unsubscribe(func2)  # event -= func2 also works
    event.invoke()  # this will only call func1

    event.clear()  # unsubscribe all
    event.invoke()  # this will do nothing

    # ---------- DataEvents ----------

    def func3(message: str) -> None:
        print(f"{message} (from func3)")

    data_event = DataEvent[str]()  # event that will return data, here a str
    data_event += func3
    data_event += func1  # subscription also works for methods that takes no arguments
    data_event.invoke("Hello!")


if __name__ == "__main__":
    main()
