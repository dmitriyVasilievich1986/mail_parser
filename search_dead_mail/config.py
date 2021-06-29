# region import libraries
import logging
import sys

# endregion

# region initialize constants

# python version
V3 = sys.version_info.major == 3

# choices to which information to show
CHOICES = [
    "full",
    "good",
    "bad",
]
# endregion


# region initialize logger
class MyFormatter(logging.Formatter):
    _formats = {
        "INFO": logging.Formatter(
            "\033[92m[%(asctime)s]%(levelname)s: %(message)s\033[0m", datefmt="%H:%M:%S"
        ),
        "ERROR": logging.Formatter(
            "\033[91m[%(asctime)s]%(levelname)s: %(message)s\033[0m", datefmt="%H:%M:%S"
        ),
        "WARNING": logging.Formatter(
            "\033[93m[%(asctime)s]%(levelname)s: %(message)s\033[0m", datefmt="%H:%M:%S"
        ),
    }

    def __init__(self, *args, **kwargs):
        if V3:
            super().__init__(*args, **kwargs)
        else:
            super(MyFormatter, self).__init__(*args, **kwargs)

    def format(self, record):
        f = self._formats.get(record.levelname)

        return f.format(record)


logger = logging.getLogger()

formatter = MyFormatter()
handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# endregion

# region initialize base configuration


class BaseConfig:
    LOGS = "logs"


# endregion
