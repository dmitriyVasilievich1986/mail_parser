# region import libraries
from .config import V3

# endregion


class InitializationException(Exception):
    def __init__(self, message="Invalid line to init class."):
        if V3:
            super().__init__(message)
        else:
            super(Exception, self).__init__(message)
