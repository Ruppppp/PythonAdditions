from typing import Generic, TypeVar, Callable, Self, Any, Iterator, overload
import inspect

_T = TypeVar("_T")
_CT = TypeVar("_CT", bound=Callable)


class BaseEvent(Generic[_CT]):
    """Base class that handles data or no data
    """
    _subscribers: list[_CT]

    def __init__(self) -> None:
        self._subscribers = []

    def __iadd__(self, other: _CT, /) -> Self:
        """Similar to `subscribe`
        """
        self.subscribe(other)
        return self

    def __isub__(self, other: _CT, /) -> Self:
        """Similar to `unsubscribe`
        """
        self.unsubscribe(other)
        return self

    def __iter__(self) -> Iterator[_CT]:
        """Iterate through subscribers
        """
        return iter(self._subscribers)

    def _callSubscriber(self, subscriber: _CT, data: Any) -> Any:
        """Provides security while calling subscribers, since they can have one input or no input.
        """
        sig = inspect.signature(subscriber)
        try:
            sig.bind(data)
        except TypeError:
            return subscriber()
        return subscriber(data)

    def invoke(self, data: Any, /) -> list[Any]:
        """Call every subscribed callbacks with the provided `data`, returns a list of all the objects returned by the callback functions by order of subscription
        """
        return [self._callSubscriber(subscriber, data) for subscriber in self]

    def subscribe(self, callback: _CT, /) -> None:
        """Subscribe a callback to the event
        """
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: _CT, /) -> None:
        """Unsubscribe a callback from the event
        """
        self._subscribers.remove(callback)

    def clear(self) -> None:
        """Clear all subsribers of the event
        """
        self._subscribers = []

    def getSubsribers(self) -> list[_CT]:
        """Get the list of all subscribers
        """
        return self._subscribers


class Event(BaseEvent[Callable[[], Any]]):
    """Allow easy event management, when an event is invoked, every subscribed callback function will be called automatically
    """

    @overload
    def invoke(self) -> list[Any]:
        pass

    @overload
    def invoke(self, data: None = None, /) -> list[Any]:
        pass

    def invoke(self, data: None = None) -> list[Any]:
        """Call every subscribed callbacks, returns a list of all the objects returned by the callback functions by order of subscription
        """
        return super().invoke(None)


class DataEvent(Generic[_T], BaseEvent[Callable[[_T], Any] | Callable[[], Any]]):
    """Allow easy event management, when an event is invoked, every subscribed callback function will be called automatically. Also transfers data to callback functions
    """
    _lastSentData: _T | None

    @overload
    def __init__(self) -> None:
        pass

    @overload
    def __init__(self, defaultData: _T) -> None:
        """`defaultData` is the value returned by `getLastSentData` if `invoke` was never called (`None` by default).
        """
        pass

    def __init__(self, defaultData: _T | None = None) -> None:
        super().__init__()
        self._lastSentData = defaultData

    def invoke(self, data: _T, /) -> list[Any]:
        return super().invoke(data)

    def getLastSentData(self) -> _T | None:
        return self._lastSentData
