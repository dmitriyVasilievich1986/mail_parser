from .IterClass import IterClass


class Choices(IterClass):
    # region class initialization
    def __init__(self, *args, **kwargs):
        """A simple class for storing given values.
        It is used to select options for displaying information.
        """

        self.full = "full"
        self.null = "null"
        self.good = "good"
        self.bad = "bad"

        self.choices = list(self.__dict__.values())

    @property
    def default(self, *args, **kwargs):
        """The method returns the default value from the list of set values.

        Returns:
            str: default value from choices
        """

        return self.full

    # endregion

    # region get items from class storage
    def __getitem__(self, value, *args, **kwargs):
        """A method for retrieving data from values stored in an instance of a class.

        Args:
            value (Union[str, int, slice]): The index at which to search for the value.

        Raises:
            IndexError: Displayed if no data matching the entered index could be found.

        Returns:
            Union[str, list]: The value or slice corresponding to the entered index.
        """

        if isinstance(value, str) and self.__dict__.get(value, False):
            return self.__dict__[value]
        elif isinstance(value, int) or isinstance(value, slice):
            return self.choices[value]
        raise IndexError

    # endregion
