# region import libraries
from .IterClass import IterClass
from .Choices import Choice
from .router import Router
from typing import Union

# endregion

class MailFilter(IterClass):
    def __init__(
        self, mails: list, code_and_mail: list, *args: list, **kwargs: dict
    ) -> None: ...
    def __getitem__(
        self, value: Union[int, slice], *args: list, **kwargs: dict
    ) -> Union[Router, list]: ...
    def get(self, value: Choice, *args: list, **kwargs: dict) -> list: ...
    def _get_sorted_mails(self, *args: list, **kwargs: dict) -> None: ...
    def _get_filtered_mails(
        self, mails: list, code_and_mail: list, *args: list, **kwargs: dict
    ) -> list: ...
