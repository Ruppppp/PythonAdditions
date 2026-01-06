# PythonAdditions
Recurring Python additions to avoid having to code them every time.

## Singleton
Allow easy singleton pattern. Make a class inherit from `Singleton` will assure only one instance of the class exists at any given time. A `SingletonError` will be raised if the constructor is called more than once. The unique instance can be accessed through the `INSTANCE` attribute of the class.
