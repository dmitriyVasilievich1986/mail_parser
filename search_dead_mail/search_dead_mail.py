from .config import BaseConfig, V3, logger, CHOICES
from .MailAggregator import MailAggregator

from os.path import exists, isfile, isdir, join
from datetime import datetime
from os import listdir
import re

if V3:
    from .p3_print import p3_print as p
else:
    from .p2_print import p2_print as p

OPEN_DICT = {"mode": "r", "encoding": "cp437"} if V3 else {"mode": "r"}


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


def main(
    v=CHOICES[0], mails=None, code=None, path=None, n=None, s=None, *args, **kwargs
):
    logger.info("start")
    start_time = datetime.now()

    path = path or BaseConfig.LOGS
    logs = sorted(get_logs_from_path(path), key=sort_function)

    agg = MailAggregator(path)

    if not len(logs):
        logger.warning("No log files were found.")

    # read logs
    for log in logs:
        # check file
        if not isfile(log):
            logger.warning("File <{}> doesn`t exist.".format(log))
            continue
        # open file
        with open(log, **OPEN_DICT) as file:
            logger.info("Open for read file: {}".format(log))
            lines = file.readlines()
            # progress bar
            length = len(lines) // 100
            for i, line in enumerate(lines):
                if not i % length:
                    p("Progress: {}%".format(i // length))
                # try to add data from log
                agg + line

    print(agg.show(n=n, choice=v, mail=mails, code=code))
    s and agg.save_sqlite()
    # print(agg.mails.keys())

    end_time = datetime.now() - start_time
    logger.info("Overall time: {}".format(end_time))
