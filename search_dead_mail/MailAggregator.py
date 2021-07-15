# region import libraries
from .InitializationException import InitializationException
from collections import OrderedDict
from .MailFilter import MailFilter
from .IterClass import IterClass
from .scheduler import Scheduler
from .config import logger, V3
from .router import Router
from .DB import DB

# endregion


class MailAggregator(IterClass):
    # region class initialization
    def __init__(self, path, *args, **kwargs):
        """The main class for storing, aggregating, sorting and filtering data.
        It takes a single line from the logs, creates a class that stores data on its basis.
        Accepts data filtering patterns. Also displays sorted and filtered data to the screen.
        Has the ability to save the received data to the sqlite database.

        Args:
            path (str): path to file or directory with log files.
        """

        self.mails = OrderedDict()
        self.path = path

    # endregion

    # region get items from class storage
    @property
    def mails_values(self, *args, **kwargs):
        """The method returns a list of all emails stored in an instance of the class.

        Returns:
            list: list of all emails stored in an instance of the class.
        """

        if self.__dict__.get("_mails_values") is None:
            self._mails_values = list(self.mails.values())
        return self._mails_values

    @property
    def length(self, *args, **kwargs):
        """The method returns the number of emails.

        Returns:
            int: the number of emails.
        """

        return len(self.mails_values)

    def get_mail_filter(self, code_and_mail=None, *args, **kwargs):
        """Method returns MailFilter class instance.

        Args:
            code_and_mail (list, optional): List of emails and codes by which you need to filter. Defaults to None.

        Returns:
            MailFilter: MailFilter class instance.
        """

        if self.__dict__.get("_mail_filter") is None:
            self._mail_filter = MailFilter(list(self), code_and_mail)
        return self._mail_filter

    def __getitem__(self, value, *args, **kwargs):
        """A method for retrieving data from values stored in an instance of a class.

        Args:
            value (Union[str, int, slice]): The index at which to search for the value.

        Raises:
            IndexError: Displayed if no data matching the entered index could be found.

        Returns:
            Union[str, list]: The value or slice corresponding to the entered index.
        """

        if isinstance(value, str) and self.mails.get(value, False):
            return self.mails[value]
        elif isinstance(value, int) or isinstance(value, slice):
            return self.mails_values[value]
        raise IndexError

    # endregion

    # region add new instances
    def __add__(self, value, *args, **kwargs):
        """The method accepts a string from the logs as input.
        Initializes one of the classes for storing data from logs.

        Args:
            value (str): string from the logs.
        """

        if not isinstance(value, str):
            return
        for class_name in [Scheduler, Router]:
            try:
                instance = class_name(value)
                self._add_instance(instance)
                return
            except InitializationException:
                pass

    def _add_instance(self, instance, *args, **kwargs):
        """The method accepts an instance of one of the classes for storing data. Saves it to its own storage.

        Args:
            instance (Union[Router, Scheduler]): an instance of one of the classes for storing data.
        """

        if isinstance(instance, Scheduler):
            try:
                self[instance.code] + instance
            except IndexError:
                pass
        elif isinstance(instance, Router):
            if self.mails.get(instance.code, False):
                # logger.warning("Code: {}, repeates in logs.".format(instance.code))
                pass
            else:
                instance.code_id = len(self.mails)
                self.mails[instance.code] = instance

    # endregion

    # region string representaion of class
    def __str__(self, mails=None, n=None, *args, **kwargs):
        """The method returns a string representation of an instance of the class.

        Args:
            mails (Union[list, None], optional): list of emails required for display. Defaults to None.
            n (Union[int, None], optional): number of displayed items. Defaults to None.

        Returns:
            str: a string representation of an instance of the class.
        """

        return self._get_list_string(mails=mails, n=n)

    def show(self, choice, code, mail, n, *args, **kwargs):
        """The method accepts email filtering parameters as input.
        Gets a filtered list and displays it.

        Args:
            choice (str): a value from a list of valid values to choose from.
            code (Union[list, None]): a list of codes by which filtering is required.
            mail (Union[list, None]): a list of emails by which filtering is required.
            n (Union[int, None]): The number of lines to display on the screen.

        Returns:
            str: displayed information.
        """

        code_and_mails = code + mail
        filtered_mails = self.get_mail_filter(code_and_mails)
        return self.__str__(mails=filtered_mails.get(choice), n=n)

    def _get_list_string(
        self, n=None, mails=None, message="\tList of mail objects:\n", *args, **kwargs
    ):
        """The method accepts a filtered email list. Returns a string with data from the list.

        Args:
            n (Union[int, None]): The number of lines to display on the screen.
            mails (Union[list, None], optional): a filtered email list. Defaults to None.
            message (str, optional): The message at the beginning of the displayed information. Defaults to "\tList of mail objects:\n".

        Returns:
            str: a string with data from the list.
        """

        mails = mails or list(self.get_mail_filter())
        length = len(mails)
        n = n and min(n, length) or length

        if not length:
            logger.warning("No matches were found that match your request.")
            return ""

        payload = "\n{}".format(message)
        for i, mail in enumerate(mails[:n], start=1):
            payload += "{:<4} - {}\n".format(i, mail)
        payload += "\tShow: {}, Overall: {}\n".format(n, length)
        return payload

    # endregion

    # region save data
    def save_sqlite(self, *args, **kwargs):
        """Method for working with a database. Creates a connection to the database, saves data to the database, closes the connection."""

        if not self.length:
            logger.warning("Can`t save data to DB. No data required.")
            return

        db = DB(self.path)
        self._insert_codes(db)
        self._insert_mails(db)
        db.close()

    def _insert_mails(self, db, *args, **kwargs):
        """Puts data into a mails table."""

        mails = list()
        for mail in self.mails_values:
            mails += mail.get_sql_values()

        query = "INSERT INTO mail(code_id, mail, status_id) VALUES {}".format(
            ",".join(x for x in mails)
        )
        db.execute(query)

    def _insert_codes(self, db, *args, **kwargs):
        """Puts data into a codes table."""

        codes = list(self.mails)
        query = "INSERT INTO code(code) VALUES {}".format(
            ",".join("('{}')".format(x) for x in codes)
        )
        db.execute(query)

    # endregion
