from typing import Generic, TypeVar, Callable, Self, Any, Iterator
import inspect

_T = TypeVar("_T")


class BaseEvent(Generic[_T]):
    """Base class that handles data or no data
    """
    _subscribers: list[Callable]
    _lastSentData: Any

    def __init__(self, defaultData: Any = None) -> None:
        """`defaultData` is the value returned by `getLastSentData` if `invoke` was never called (`None` by default).
        """
        self._subscribers = []
        self._lastSentData = defaultData

    def __iadd__(self, other: Callable, /) -> Self:
        """Similar to `subscribe`
        """
        self.subscribe(other)
        return self

    def __isub__(self, other: Callable, /) -> Self:
        """Similar to `unsubscribe`
        """
        self.unsubscribe(other)
        return self

    def __iter__(self) -> Iterator[Callable]:
        """Iterate through subscribers
        """
        return iter(self._subscribers)

    def _callSubscriber(self, subscriber: Callable, data: Any) -> Any:
        """Provides security while calling subscribers, since they can have one input or no input.
        """
        sig = inspect.signature(subscriber)
        try:
            sig.bind(data)
        except TypeError:
            return subscriber()
        return subscriber(data)

    def invoke(self, data: Any, /) -> list:
        """Call every subscribed callbacks with the provided `data`, returns a list of all the objects returned by the callback functions by order of subscription
        """
        return [self._callSubscriber(subscriber, data) for subscriber in self]

    def subscribe(self, callback: Callable, /) -> None:
        """Subscribe a callback to the event
        """
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable, /) -> None:
        """Unsubscribe a callback from the event
        """
        self._subscribers.remove(callback)

    def clear(self) -> None:
        """Clear all subsribers of the event
        """
        self._subscribers = []

    def getLastSentData(self) -> Any:
        """Get the value of the last sent data, if the event has never been called, the `defaultData` provided in the constructor is returned
        """
        return self._lastSentData

    def getSubsribers(self) -> list[Callable]:
        """Get the list of all subscribers
        """
        return self._subscribers


class Event(BaseEvent[None]):
    """Allow easy event management, when an event is invoked, every subscribed callback function will be called automatically
    """
    _subscribers: list[Callable[[], Any]]
    _lastSentData: None

    def __init__(self) -> None:
        """
        """
        super().__init__()

    def __iadd__(self, other: Callable[[], Any], /) -> Self:
        return super().__iadd__(other)

    def __isub__(self, other: Callable[[], Any], /) -> Self:
        return super().__isub__(other)

    def __iter__(self) -> Iterator[Callable[[], Any]]:
        return super().__iter__()

    def invoke(self, data: None = None, /) -> list[Any]:
        """Call every subscribed callbacks, returns a list of all the objects returned by the callback functions by order of subscription
        """
        return super().invoke(None)

    def subscribe(self, callback: Callable[[], Any], /) -> None:
        return super().subscribe(callback)

    def unsubscribe(self, callback: Callable[[], Any], /) -> None:
        return super().unsubscribe(callback)

    def getLastSentData(self) -> None:
        """Will allways return `None`, used in DataEvent
        """
        return None

    def getSubsribers(self) -> list[Callable[[], Any]]:
        return super().getSubsribers()


class DataEvent(BaseEvent[_T]):
    """Allow easy event management, when an event is invoked, every subscribed callback function will be called automatically. Also transfers data to callback functions
    """
    _subscribers: list[Callable[[_T], None]]
    _lastSentData: _T | None

    def __init__(self, defaultData: _T | None = None) -> None:
        super().__init__(defaultData)

    def __iadd__(self, other: Callable[[_T], Any] | Callable[[], Any], /) -> Self:
        return super().__iadd__(other)

    def __isub__(self, other: Callable[[_T], Any] | Callable[[], Any], /) -> Self:
        return super().__isub__(other)

    def __iter__(self) -> Iterator[Callable[[_T], Any] | Callable[[], Any]]:
        return super().__iter__()

    def invoke(self, data: _T, /) -> list:
        return super().invoke(data)

    def subscribe(self, callback: Callable[[_T], Any] | Callable[[], Any]) -> None:
        return super().subscribe(callback)

    def unsubscribe(self, callback: Callable[[_T], Any] | Callable[[], Any]) -> None:
        return super().unsubscribe(callback)

    def getLastSentData(self) -> _T | None:
        return super().getLastSentData()

    def getSubsribers(self) -> list[Callable[[_T], Any] | Callable[[], Any]]:
        return super().getSubsribers()
