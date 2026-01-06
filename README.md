# PythonAdditions
Recurring Python additions to avoid having to code them every time.

## Singleton
Allow easy singleton pattern. Make a class inherit from `Singleton` will assure only one instance of the class exists at any given time. A `SingletonError` will be raised if the constructor is called more than once. The unique instance can be accessed through the `INSTANCE` attribute of the class.

## Event
Event system to easily call a list of subscribed `Callables` with or without data. By creating an `Event` and subscribing serveral methods, they will all be called when the `Event.invoke` methode is called. With a `DataEvent`, the desired data will be provided to the callbacks, making it easy to notify a value change for exemple.
