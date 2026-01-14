import abc
import inspect
from collections.abc import Callable, Iterator
from typing import Any, Self, overload


class BaseEvent[CT: Callable](abc.ABC):
    """Abstract base class."""

    _subscribers: list[CT]

    def __init__(self) -> None:
        self._subscribers = []

    def __iadd__(self, other: CT, /) -> Self:
        """Similar to `subscribe`."""
        self.subscribe(other)
        return self

    def __isub__(self, other: CT, /) -> Self:
        """Similar to `unsubscribe`."""
        self.unsubscribe(other)
        return self

    def __iter__(self) -> Iterator[CT]:
        """Iterate through subscribers."""
        return iter(self._subscribers)

    @staticmethod
    def _call_subscriber(subscriber: CT, data: Any) -> Any:
        """Provides security while calling subscribers, since they can have one input or no input."""
        sig = inspect.signature(subscriber)
        try:
            sig.bind(data)
        except TypeError:
            return subscriber()
        return subscriber(data)

    def invoke(self, data: Any, /) -> list[Any]:
        """Call every subscribed callbacks with the provided `data`, returns a list of all the objects returned by the callback functions by order of subscription."""
        return [self._call_subscriber(subscriber, data) for subscriber in self]

    def subscribe(self, callback: CT, /) -> None:
        """Subscribe a callback to the event."""
        if callback not in self._subscribers:
            self._subscribers.append(callback)

    def unsubscribe(self, callback: CT, /) -> None:
        """Unsubscribe a callback from the event."""
        self._subscribers.remove(callback)

    def clear(self) -> None:
        """Clear all subscribers of the event."""
        self._subscribers = []

    def get_subscribers(self) -> list[CT]:
        """Get the list of all subscribers."""
        return self._subscribers


class Event(BaseEvent[Callable[[], Any]]):
    """Allow easy event management, when an event is invoked, every subscribed callback function will be called automatically."""

    @overload
    def invoke(self) -> list[Any]: ...
    @overload
    def invoke(self, data: None = None, /) -> list[Any]: ...
    def invoke(self, data: None = None) -> list[Any]:
        """Call every subscribed callbacks, returns a list of all the objects returned by the callback functions by order of subscription."""
        return super().invoke(None)


class DataEvent[T](BaseEvent[Callable[[T], Any] | Callable[[], Any]]):
    """Allow easy event management, when an event is invoked, every subscribed callback function will be called automatically. Also transfers data to callback functions."""

    def invoke(self, data: T, /) -> list[Any]:
        return super().invoke(data)
