class Singleton(object):
    """Singleton pattern class."""

    _instances = {}

    def __new__(class_, *args, **kwargs):
        """Create new instance if it does not already exist; else reuse."""
        if class_ not in class_._instances:
            class_._instances[class_] = super(Singleton, class_).__new__(
                class_, *args, **kwargs
            )
        return class_._instances[class_]
