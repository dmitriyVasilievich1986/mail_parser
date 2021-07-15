class IterClass:
    # region iteration methods for class
    def __iter__(self, *args, **kwargs):
        """Method initializer for an iterable object.

        Returns:
            Choices: returns self.
        """

        self.__iter_item = 0
        return self

    def __next__(self, *args, **kwargs):
        """A loop method that returns the next value when iterating over an object.

        Raises:
            StopIteration: Raises when there is nothin to returns.

        Returns:
            str: next item in the loop.
        """

        try:
            payload = self[self.__iter_item]
            self.__iter_item += 1
            return payload
        except IndexError:
            raise StopIteration

    def next(self, *args, **kwargs):
        """A loop method that returns the next value when iterating over an object.

        Raises:
            StopIteration: Raises when there is nothin to returns.

        Returns:
            str: next item in the loop.
        """

        return self.__next__()

    # endregion
