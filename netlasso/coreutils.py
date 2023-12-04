# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


import argparse
import csv
import json
import logging
import os

from rich.logging import RichHandler
from rich.markdown import Markdown
from rich_argparse import RichHelpFormatter

from . import (
    __description__,
    __epilog__,
    __version__,
    CSV_DIRECTORY,
    JSON_DIRECTORY,
)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def pathfinder():
    """
    Creates file directories if they don't already exist.
    """
    file_directories = [CSV_DIRECTORY, JSON_DIRECTORY]
    for directory in file_directories:
        os.makedirs(directory, exist_ok=True)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def setup_logging(debug_mode: bool) -> logging.getLogger:
    """
    Configure and return a logging object with the specified log level.

    :param debug_mode: A boolean value indicating whether debug mode should be enabled or not.
    :return: A logging object configured with the specified log level.
    """
    logging.basicConfig(
        level="NOTSET" if debug_mode else "INFO",
        format="%(message)s",
        handlers=[
            RichHandler(
                markup=True, log_time_format="%I:%M:%S%p", show_level=debug_mode
            )
        ],
    )
    return logging.getLogger("Net Lasso")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def save_data(
    data: list,
    filename: str,
    save_json: bool = False,
    save_csv: bool = False,
):
    """
    Save the given data to JSON and/or CSV files based on the arguments.

    :param data: The data to be saved, which is a list of Host objects.
    :param filename: The base filename to use when saving.
    :param save_json: A boolean value to indicate whether to save data as a JSON file.
    :param save_csv: A boolean value to indicate whether to save data as a CSV file.
    """

    # Save to JSON if save_json is True
    if save_json:
        with open(
            os.path.join(JSON_DIRECTORY, f"{filename}.json"), "w", encoding="utf-8"
        ) as json_file:
            json.dump([item.__dict__ for item in data], json_file, indent=4)
        log.info(
            f"{os.path.getsize(json_file.name)} bytes written to [link file://{json_file.name}]{json_file.name}"
        )

    if save_csv:
        with open(
            os.path.join(CSV_DIRECTORY, f"{filename}.csv"),
            "w",
            newline="",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(csv_file)
            if data:
                writer.writerow(
                    data[0].__dict__.keys()
                )  # header from keys of the first item
                for item in data:
                    writer.writerow(item.__dict__.values())
        log.info(
            f"{os.path.getsize(csv_file.name)} bytes written to [link file://{csv_file.name}]{csv_file.name}"
        )


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=Markdown(__description__, style="argparse.text"),
        epilog=Markdown(__epilog__, style="argparse.text"),
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument(
        "-p",
        "--page",
        type=int,
        default=0,
        help="page number to get results from (default: %(default)s)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "-d", "--debug", help="([green]dev[/]) enable debug mode", action="store_true"
    )
    parser.add_argument(
        "-j", "--json", help="write results to a JSON file", action="store_true"
    )
    parser.add_argument(
        "-c", "--csv", help="write results to a CSV file", action="store_true"
    )
    parser.add_argument(
        "-v", "--version", version=f"Net Lasso v{__version__}", action="version"
    )

    return parser


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

args = create_parser().parse_args()
log = setup_logging(debug_mode=args.debug)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
