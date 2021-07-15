# region import libraries
from pathlib import Path
import platform
import logging
import sys

# endregion

# region initialize constants

# python version
V3 = sys.version_info.major == 3

is_linux = platform.system() == "Linux"
# endregion


class Colors:
    INFO = "\033[92m" if is_linux else ""
    ERROR = "\033[91m" if is_linux else ""
    WARNING = "\033[93m" if is_linux else ""

    END = "\033[0m" if is_linux else ""


# region initialize logger
class MyFormatter(logging.Formatter):
    _formats = {
        "INFO": logging.Formatter(
            "{}[%(asctime)s]%(levelname)s: %(message)s{}".format(
                Colors.INFO, Colors.END
            ),
            datefmt="%H:%M:%S",
        ),
        "ERROR": logging.Formatter(
            "{}[%(asctime)s]%(levelname)s: %(message)s{}".format(
                Colors.ERROR, Colors.END
            ),
            datefmt="%H:%M:%S",
        ),
        "WARNING": logging.Formatter(
            "{}[%(asctime)s]%(levelname)s: %(message)s{}".format(
                Colors.WARNING, Colors.END
            ),
            datefmt="%H:%M:%S",
        ),
    }

    def __init__(self, *args, **kwargs):
        if V3:
            super().__init__(*args, **kwargs)
        else:
            super(MyFormatter, self).__init__(*args, **kwargs)

    def format(self, record, *args, **kwargs):
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
    BASE_DIR = Path(__file__).resolve().parent.parent
    LOGS = BASE_DIR / "logs"


# endregion
