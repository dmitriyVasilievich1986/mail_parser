#!/usr/bin/python

from search_dead_mail import main, CHOICES
from argparse import ArgumentParser


def get_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-M",
        "--mails",
        nargs="+",
        metavar="",
        default=list(),
        help="Enter one or multiple email, to show data with only these mails.",
    )
    parser.add_argument(
        "-C",
        "--code",
        nargs="+",
        metavar="",
        default=list(),
        help="Enter one or multiple hash code, to show data with only these codes.",
    )
    parser.add_argument(
        "-P",
        "--path",
        metavar="",
        help="Enter path to log file or directpry with log files.",
    )
    parser.add_argument(
        "-S",
        "--save",
        action="store_true",
        help="Enter argument, if need to save data to database.",
    )
    parser.add_argument(
        "-V",
        "--verbose",
        default=CHOICES[0],
        choices=CHOICES,
        help='Which type information show. bad/good - only bad or good mails. none - doesn`t show any. Default: "full".',
    )
    parser.add_argument(
        "-L",
        "--limit",
        type=int,
        metavar="",
        help="Enter limit strings to show. Don`t use this argument, to show full list.",
    )
    parser.add_argument(
        "-F",
        "--file",
        action="store_true",
        help="Enter argument, if need to save data to file.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    parser = get_parser()

    main(
        mails=parser.mails,
        code=parser.code,
        path=parser.path,
        v=parser.verbose,
        n=parser.limit,
        s=parser.save,
    )
