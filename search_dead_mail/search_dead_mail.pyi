from typing import Union

def get_logs_from_path(path: str, *args: list, **kwargs: dict) -> list: ...
def sort_function(path: str, *args: list, **kwargs: dict) -> bool: ...
def main(
    v: str,
    mails: list,
    code: list,
    path: Union[str, None],
    s: bool,
    n: Union[int, None],
    *args: list,
    **kwargs: dict
) -> None: ...
