class ProtectedSection:

    def __init__(self, log=(), suppress=()):
        self._suppress = tuple(suppress)
        self._log = tuple(log)
        self.exception = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type in self._log:
            self.exception = exc_type(exc_val)
        elif exc_type not in self._suppress:
            return False

        return True