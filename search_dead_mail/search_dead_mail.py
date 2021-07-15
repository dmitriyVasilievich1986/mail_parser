# region import libraries
from .config import BaseConfig, V3, logger
from .MailAggregator import MailAggregator
from .Choices import Choices, Null

from os.path import exists, isfile, isdir, join
from datetime import datetime
from os import listdir
import re

# endregion

# region constants initialization
if V3:
    from .p3_print import p3_print as p
else:
    from .p2_print import p2_print as p

OPEN_DICT = {"mode": "r", "encoding": "cp437"} if V3 else {"mode": "r"}
# endregion


# region search and formation of a list of pathes to logs
def get_logs_from_path(path, *args, **kwargs):
    """The function accepts as input to the file
        or to the folder where you need to find the logs for parsing.
        Returns a list of all logs located in the folder and subfolders.

    Args:
        path (str): Path to file or dir.

    Returns:
        list: list of all logs located in the folder and subfolders.
    """

    payload = list()
    # if not exists, then empty
    if not exists(path):
        return payload
    # if file, than returns list this file
    if isfile(path):
        return [path]
    for file_or_dir in listdir(path):
        if isdir(join(path, file_or_dir)):
            payload += get_logs_from_path(join(path, file_or_dir))
        elif re.search(r".*?.log", file_or_dir):
            payload.append(join(path, file_or_dir))
    return payload


def sort_function(path, *args, **kwargs):
    """Sorting function.
        Sorts the data, puts above the logs in which the specified template is present.

    Args:
        path (str): path to log file.

    Returns:
        bool: contain line exact template or not.
    """

    with open(path, **OPEN_DICT) as file:
        for i, line in enumerate(file.readlines()):
            if re.search(r"^\S+ \d+ -*?\d+ \S+ \S+$", line) is not None:
                return True
            if i >= 20:
                return False


# endregion


# region main function
def main(
    v=Choices().default,
    mails=list(),
    code=list(),
    path=None,
    s=False,
    n=None,
    *args,
    **kwargs
):
    """The function is the main entry point for the search_dead_mail module.

    Args:
        v (Choice, optional): type of displayed informations. Defaults to Choices().default.
        mails (list, optional): a list of emails by which filtering is required. Defaults to None.
        code (list, optional): a list of codes by which filtering is required. Defaults to None.
        path (str, optional): path to file or directory with log files. Defaults to None.
        s (bool, optional): Flag of the need to save data to the sqlite database. Defaults to False.
        n (Union[int, None], optional): number of displayed items. Defaults to None.
    """

    logger.info("start")
    start_time = datetime.now()

    path = path or BaseConfig.LOGS
    logger.info("Path to log files: {}".format(path))
    logs = sorted(get_logs_from_path(path), key=sort_function)

    agg = MailAggregator(path)

    len(logs) or logger.warning("No log files were found.")

    # read logs
    for log in logs:
        # open file
        with open(log, **OPEN_DICT) as file:
            logger.info("Open for read file: {}".format(log))
            lines = file.readlines()
            # progress bar
            length = len(lines) // 100
            for i, line in enumerate(lines):
                i % length or p("Progress: {}%".format(i // length))
                agg + line

    not isinstance(v, Null) and p(agg.show(n=n, choice=v, mail=mails, code=code))
    s and agg.save_sqlite()

    end_time = datetime.now() - start_time
    logger.info("Overall time: {}".format(end_time))


# endregion
