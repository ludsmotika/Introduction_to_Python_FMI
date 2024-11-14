class LockPicker_0MI0600397:
    def __init__(self, lock):
        self._lock = lock
        self._concrete_arguments = []

    def unlock(self):
        try:
            self._lock.pick(*self._concrete_arguments)
            return True
        except TypeError as ex:
            if ex.position:
                if ex.expected != type(None):
                    self._concrete_arguments[ex.position - 1] = ex.expected()
                self.unlock()
            else:
                self._concrete_arguments = [None] * ex.expected
        except ValueError as ex:
            self._concrete_arguments[ex.position - 1] = ex.expected
            self.unlock()
