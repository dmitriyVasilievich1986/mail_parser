# region import libraries
import logging

# endregion

class MyFormatter(logging.Formatter):
    def __init__(self, *args: list, **kwargs: dict) -> None: ...
    def format(self, record: logging.LogRecord, *args, **kwargs) -> str: ...
