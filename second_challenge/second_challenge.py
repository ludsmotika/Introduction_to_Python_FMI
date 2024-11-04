class HauntedMansion:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __setattr__(self, key, value):
        object.__setattr__(self, f'spooky_{key}', value)

    def __getattr__(self, item):
        return 'Booooo, only ghosts here!'
