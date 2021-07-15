from typing import Union
from .IterClass import IterClass

class Choices(IterClass):
    def __init__(self, *args: list, **kwargs: dict) -> None: ...
    @property
    def default(self, *args: list, **kwargs: dict) -> str: ...
    def __getitem__(
        self, value: Union[int, str, slice], *args: list, **kwargs: dict
    ) -> str: ...
