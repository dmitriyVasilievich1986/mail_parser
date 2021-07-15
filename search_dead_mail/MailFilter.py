# region import libraries
from .IterClass import IterClass
from .Choices import Good, Bad

# endregion


class MailFilter(IterClass):
    # region class initialization
    def __init__(self, mails, code_and_mail, *args, **kwargs):
        """The main class for sorting and filtering the list of emails.
        Accepts a list of emails, filtering conditions.
        Performs filtering, sorting and storage of the received data.

        Args:
            mails (list): list of unsorted, unfiltered emails
            code_and_mail (list): List of emails and codes to filter by.
        """

        self.filtered_mails = self._get_filtered_mails(mails, code_and_mail)
        self._get_sorted_mails()
        self.mails = sorted(mails, key=lambda x: x.is_ok)

    # endregion

    # region get items from class storage
    def __getitem__(self, value, *args, **kwargs):
        """A method for retrieving data from values stored in an instance of a class.

        Args:
            value (Union[int, slice]): The index at which to search for the value.

        Raises:
            IndexError: Displayed if no data matching the entered index could be found.

        Returns:
            Union[str, list]: The value or slice corresponding to the entered index.
        """

        if isinstance(value, int) or isinstance(value, slice):
            return self.mails[value]
        raise IndexError

    def get(self, value, *args, **kwargs):
        """The method accepts a condition and,
            according to this condition, returns a list of only good or bad emails,
            or a complete list.

        Args:
            value (Choice): type of condition

        Returns:
            list: list of only good or bad emails, or a complete list.
        """

        if isinstance(value, Good):
            return self.good_mails
        elif isinstance(value, Bad):
            return self.bad_mails
        return self.sorted_mails

    def _get_sorted_mails(self, *args, **kwargs):
        """The method sorts the list of emails by good and bad emails."""

        def _sort_function(value, *args, **kwargs):
            """Sorted function."""

            if value.is_ok:
                self.good_mails.append(value)
                return True
            self.bad_mails.append(value)
            return False

        self.good_mails = list()
        self.bad_mails = list()

        self.sorted_mails = sorted(self.filtered_mails, key=_sort_function)

    def _get_filtered_mails(self, mails, code_and_mail, *args, **kwargs):
        """The method accepts a list of emails,
            as well as a list of emails and codes by which to filter.

        Args:
            mails (list): a list of emails.
            code_and_mail ([type]): a list of emails and codes by which to filter.

        Returns:
            list: filtered list of emails
        """

        if code_and_mail is None or not len(code_and_mail):
            return mails

        def _filter(value, *args, **kwargs):
            """filtered function."""
            try:
                value[code_and_mail]
                return True
            except IndexError:
                return False

        filtered_mails = filter(_filter, mails)
        return filtered_mails

    # endregion
