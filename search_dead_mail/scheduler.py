# region import libraries
from .InitializationException import InitializationException
import re

# endregion


class Scheduler:
    # region class initialization
    def __init__(self, text, *args, **kwargs):
        """The main class for storing data from the Scheduler log.

        Args:
            text (str): line from Scheduler log

        Raises:
            InitializationException: if the input string does not match the pattern.
        """

        if not re.search(r"^\S+ \d+ -*?\d+ \S+ \S+$", text):
            raise InitializationException()

        self.text = text

        self.status = self._get_status()
        self.code = self._get_code()

    # endregion

    # region get content from line
    def _get_status(self, *args, **kwargs):
        """The method parses the input string from the log and returns the status.

        Returns:
            str: status from log line
        """

        status_reg = re.search(r"\S+ \S+$", self.text).group(0)
        status = re.sub(r"\S+$|\d| ", "", status_reg)
        # print(status)
        return status

    def _get_code(self, *args, **kwargs):
        """The method parses the input string from the log and returns the code.

        Returns:
            str: code from log line
        """

        code = re.search(r"^\S+", self.text).group(0)
        return code

    # endregion

    # region string representaion of class
    def __str__(self, *args, **kwargs):
        """The method returns a string representation of an instance of the class.

        Returns:
            str: a string representation of an instance of the class.
        """

        return "Code:{}, Status: {}".format(self.code, self.status)

    # endregion
