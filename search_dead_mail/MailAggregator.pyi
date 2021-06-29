from .scheduler import Scheduler
from .router import Router
from typing import Union
from .DB import DB

class MailAggregator:
    def _get_list_string(
        self,
        n: Union[int, None],
        mails: Union[list, None],
        message: str,
        *args: list,
        **kwargs: dict,
    ) -> str: ...
    def show(
        self,
        choice: str,
        n: Union[int, None],
        code: list,
        mail: list,
        *args: list,
        **kwargs: dict,
    ) -> str: ...
    def _get_good_and_bad_mails(
        self, filtered_list: list, *args: list, **kwargs: dict
    ) -> tuple[list, list, list]: ...
    def _filter_by_mail_or_code(
        self, mails: list, mail_or_code: list, *args: list, **kwargs: dict
    ) -> list: ...
    def _add_instance(
        self, instance: Union[Scheduler, Router], *args: list, **kwargs: dict
    ) -> None: ...
    def __getitem__(
        self, value: str, *args: list, **kwargs: dict
    ) -> Union[Router, bool]: ...
    def _insert_mails(
        self, mails: list, db: DB, *args: list, **kwargs: dict
    ) -> None: ...
    def _insert_codes(
        self, codes: list, db: DB, *args: list, **kwargs: dict
    ) -> None: ...
    def __add__(self, value: str, *args: list, **kwargs: dict) -> None: ...
    def __init__(self, path: str, *args: list, **kwargs: dict) -> None: ...
    def __str__(self, n=None, *args: list, **kwargs: dict) -> str: ...
    def save_to_file(self, *args: list, **kwargs: dict) -> None: ...
    def save_sqlite(self, *args: list, **kwargs: dict) -> None: ...
    def _get_mails(self, *args: list, **kwargs: dict) -> list: ...
    def _get_codes(self, *args: list, **kwargs: dict) -> list: ...
