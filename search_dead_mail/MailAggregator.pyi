# region import libraries
from .MailFilter import MailFilter
from .IterClass import IterClass
from .scheduler import Scheduler
from .router import Router
from typing import Union
from .DB import DB

# endregion

class MailAggregator(IterClass):
    # region class initialization
    def __init__(self, path, *args: list, **kwargs: dict) -> None: ...
    @property
    def mails_values(self, *args: list, **kwargs: dict) -> list: ...
    def get_mail_filter(
        self, code_and_mail: Union[list, None], *args: list, **kwargs: dict
    ) -> MailFilter: ...
    def __getitem__(
        self, value: Union[str, int, slice], *args: list, **kwargs: dict
    ) -> Union[Router, list]: ...
    def __add__(self, value: str, *args: list, **kwargs: dict) -> None: ...
    def _add_instance(
        self, instance: Union[Router, Scheduler], *args: list, **kwargs: dict
    ) -> None: ...
    def __str__(
        self, mails: Union[list, None], n: Union[int, None], *args: list, **kwargs: dict
    ) -> str: ...
    def show(
        self,
        choice: str,
        code: Union[list, None],
        mail: Union[list, None],
        n: Union[int, None],
        *args: list,
        **kwargs: dict
    ) -> str: ...
    def _get_list_string(
        self,
        n: Union[int, None],
        mails: Union[list, None],
        message: str,
        *args: list,
        **kwargs: dict
    ) -> str: ...
    def save_sqlite(self, *args: list, **kwargs: dict) -> None: ...
    def _insert_mails(self, db: DB, *args: list, **kwargs: dict) -> None: ...
    def _insert_codes(self, db: DB, *args: list, **kwargs: dict) -> None: ...
