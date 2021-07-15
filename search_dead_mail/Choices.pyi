# region import libraries
from .IterClass import IterClass
from typing import Union

# endregion

class Choice:
    def __str__(self, *args: list, **kwargs: dict) -> None: ...

class Full(Choice):
    pass

class Null(Choice):
    pass

class Good(Choice):
    pass

class Bad(Choice):
    pass

class Choices(IterClass):
    def __init__(self, *args: list, **kwargs: dict) -> None: ...
    @property
    def default(self, *args: list, **kwargs: dict) -> str: ...
    def __getitem__(
        self, value: Union[str, int, slice], *args: list, **kwargs: dict
    ) -> Union[str, list]: ...
    def __iter__(self, *args: list, **kwargs: dict) -> Choices: ...
    def __next__(self, *args: list, **kwargs: dict) -> str: ...
    def next(self, *args: list, **kwargs: dict) -> str: ...
