# region import libraries
from .IterClass import IterClass

# endregion

# region all choices classes
class Choice:
    def __str__(self, *args, **kwargs):
        """The method returns a string representation of an instance of the class.

        Returns:
            str: a string representation of an instance of the class.
        """

        return self.__class__.__name__.lower()


class Full(Choice):
    pass


class Null(Choice):
    pass


class Good(Choice):
    pass


class Bad(Choice):
    pass


# endregion


class Choices(IterClass):
    # region class initialization
    def __init__(self, *args, **kwargs):
        """A simple class for storing given values.
        It is used to select options for displaying information.
        """

        self.full = Full()
        self.null = Null()
        self.good = Good()
        self.bad = Bad()

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
        elif isinstance(value, Choice):
            return self.__dict__[str(value)]
        raise IndexError

    # endregion

    # region iteration methods for class
    def __iter__(self, *args, **kwargs):
        """Method initializer for an iterable object.

        Returns:
            Choices: returns self.
        """

        self.__iter_item = 0
        return self

    def __next__(self, *args, **kwargs):
        try:
            payload = str(self[self.__iter_item])
            self.__iter_item += 1
            return payload
        except IndexError:
            raise StopIteration

    def next(self, *args, **kwargs):
        return self.__next__()

    # endregion
