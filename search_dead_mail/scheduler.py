from .InitializationException import InitializationException
from .config import V3
import re


class Scheduler:
    # region class initialization
    def __init__(self, text, *args, **kwargs):
        if not re.search(r"^\S+ \d+ -*?\d+ \S+ \S+$", text):
            raise InitializationException()

        self.text = text

        self.status = self._get_status()
        self.code = self._get_code()

    # endregion

    # region get content from line
    def _get_status(self, *args, **kwargs):
        status_reg = re.search(r"\S+ \S+$", self.text).group(0)
        status = re.sub(r"\S+$|\d| ", "", status_reg)
        # print(status)
        return status

    def _get_code(self, *args, **kwargs):
        code = re.search(r"^\S+", self.text).group(0)
        return code

    # endregion

    # region string representaion of class
    def __str__(self, *args, **kwargs):
        return "Code:{}, Status: {}".format(self.code, self.status)

    # endregion
