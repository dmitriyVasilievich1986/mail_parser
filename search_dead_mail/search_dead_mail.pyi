from typing import Union

def get_logs_from_path(path: str, *args: list, **kwargs: dict) -> list: ...
def sort_function(path: str, *args: list, **kwargs: dict) -> bool: ...
def main(
    v: str,
    mails: Union[list, None],
    code: Union[list, None],
    path: Union[str, None],
    n: Union[int, None],
    s: Union[bool, None],
    *args: list,
    **kwargs: dict,
) -> None: ...
