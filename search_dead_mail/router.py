# region import libraries
from .InitializationException import InitializationException
import re

# endregion


class Router:
    # region class initialization
    def __init__(self, text, *args, **kwargs):
        """The main class for storing data from the Router log.

        Args:
            text (str): line from Router log

        Raises:
            InitializationException: if the input string does not match the pattern.
        """

        valid_line = re.search(r"\[\d+\] \S+: fromto:.*$", text)
        if valid_line is None:
            raise InitializationException()

        self.scheduler = list()
        self._add_all = False
        self.mails = list()
        self.text = text

        self.from_ = self._get_from()
        self.code = self._get_code()
        self.to = self._get_to()
        self.code_id = None
        self.is_ok = False

    # endregion

    # region add and get instances
    def __add__(self, instance, *args, **kwargs):
        """The method accepts and stores an instance of the Scheduler class.

        Args:
            instance (Scheduler): an instance of the Scheduler class.
        """

        if instance.code == self.code:
            self.scheduler.append(instance)
            if instance.status == "ok":
                self.is_ok = True

    def __getitem__(self, value, *args, **kwargs):
        """A method for retrieving data from values stored in an instance of a class.

        Args:
            value (Union[str, list]): The index at which to search for the value.

        Raises:
            IndexError: Displayed if no data matching the entered index could be found.

        Returns:
            Union[str, list]: The value or slice corresponding to the entered index.
        """

        if isinstance(value, str) and self.mails.get(value, False):
            return self.mails[value]
        elif isinstance(value, list):
            if self.code in value:
                return True
            for mail in self.mails:
                if mail in value:
                    return True
        raise IndexError

    # endregion

    # region get parsed data from line from log
    def _get_code(self, *args, **kwargs):
        """The method parses the input string from the log and returns the code.

        Returns:
            str: code from log line
        """

        code_reg = re.search(r"^\[\d+\] \S+?:", self.text).group(0)
        code = re.sub(r"^\[\d+\]| |:", "", code_reg)
        return code

    def _get_from(self, *args, **kwargs):
        """The method parses the input string from the log and returns the "from" value.

        Returns:
            str: "from" value from log line
        """

        from_to_line = re.search(r"fromto:.*$", self.text).group(0)
        from_reg = re.search(r"^fromto: <.*?> =>", from_to_line)
        from_ = from_reg and re.sub(r"^fromto: <|> =>", "", from_reg.group(0)) or ""
        if self._add_all and from_ != "":
            self.mails.append(from_)
        return "null" if from_ == "" else from_

    def _get_to(self, *args, **kwargs):
        """The method parses the input string from the log and returns the "to" value.

        Returns:
            str: "to" value from log line
        """

        from_to_line = re.search(r"fromto:.*$", self.text).group(0)
        to_reg = re.search(r"=>.*", from_to_line)
        to_all_reg = to_reg and re.findall(r"<.*?>", to_reg.group(0)) or None
        to_all = to_all_reg and [re.sub(r"<|>", "", x) for x in to_all_reg] or []
        if not self._add_all and not len(
            [x for x in to_all if re.search(r"rol.ru$|online.ru$", x)]
        ):
            raise InitializationException()
        else:
            self.mails += to_all
        return "null" if to_all == "" else to_all

    # endregion

    # region get string representation
    def __str__(self, *args, **kwargs):
        """The method returns a string representation of an instance of the class.

        Returns:
            str: a string representation of an instance of the class.
        """

        return "Code: {}, From: {}, To: {}, Status: {}".format(
            self.code, self.from_, self.to, self.status
        )

    def get_sql_values(self, *args, **kwargs):
        """The method returns a string suitable for writing to the database.

        Returns:
            str: a string suitable for writing to the database.
        """

        payload = list()
        for mail in self.mails:
            values = "({}, '{}', {})".format(self.code_id, mail, 2 if self.is_ok else 1)
            payload.append(values)
        return payload

    @property
    def status(self, *args, **kwargs):
        """The method returns a string representation of the status of the email: bad / good.

        Returns:
            str: a string representation of the status of the email.
        """

        payload = "[" + ",".join(x.status for x in self.scheduler) + "]"
        return "[Unknown]" if payload == "[]" else payload

    # endregion
