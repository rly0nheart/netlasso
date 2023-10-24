import argparse
import csv
import json
import logging
import os

from rich.logging import RichHandler
from rich_argparse import RichHelpFormatter

from . import __about__, __author__, __version__


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
            RichHandler(markup=True, log_time_format="%I:%M:%S %p", show_level=False)
        ],
    )
    return logging.getLogger("Netlasso")


def get_api_key(api_key: str) -> str:
    """
    Retrieve or store the Netlas.io API key.

    :param api_key: The API key provided as input.
    :return: The final API key, either retrieved from the file or the one provided by the user.
    """
    api_key_path = os.path.join(CURRENT_FILE_DIRECTORY, ".netlas-auth")
    try:
        # Check if the API key file exists and is not empty
        if os.path.exists(api_key_path) and os.path.getsize(api_key_path) > 0:
            # Read API key from the file
            with open(api_key_path, "r") as file:
                final_api_key = file.readline().rstrip("\n")
        else:
            # Write the input API key to the file
            with open(api_key_path, "w") as file:
                file.write(api_key)

            log.info(f"Netlas.io API key written to {api_key_path}")
            final_api_key = api_key
    except Exception as e:
        log.error(f"An error occurred while handling the API key: {e}")

    return final_api_key


def format_api_data(api_data: dict, data_file: str) -> dict:
    """
    Formats API data based on a key mapping from a JSON file.

    :param api_data: Dictionary containing raw data from the API.
    :param data_file: Path to the JSON file that contains the key mapping.

    :returns: A Formatted JSON object with human-readable keys.
    """
    # Construct path to the mapping data file
    mapping_data_file = os.path.join(CURRENT_FILE_DIRECTORY, "data", data_file)

    # Load the mapping from the specified file
    with open(mapping_data_file, "r", encoding="utf-8") as file:
        mapping_data = json.load(file)

    # Initialize an empty dictionary to hold the formatted data
    formatted_data = {}

    # Map API data to human-readable format using the mapping
    for api_data_key, mapping_data_key in mapping_data.items():
        formatted_data[mapping_data_key] = api_data.get(api_data_key, "N/A")

    return formatted_data


def save_data(
    data: dict,
    filename: str,
    save_to_json: bool = False,
    save_to_csv: bool = False,
):
    """
    Save the given data to JSON and/or CSV files based on the arguments.

    :param data: The data to be saved, which is a list of dictionaries.
    :param filename: The base filename to use when saving.
    :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
    :param save_to_csv: A boolean value to indicate whether to save data as a CSV file.
    """

    # Save to JSON if save_json is True
    if save_to_json:
        with open(os.path.join(JSON_DIRECTORY, f"{filename}.json"), "w") as json_file:
            json.dump(data, json_file)
        log.info(f"JSON data saved to {json_file.name}")

    # Save to CSV if save_csv is True
    if save_to_csv:
        with open(
            os.path.join(CSV_DIRECTORY, f"{filename}.csv"), "w", newline=""
        ) as csv_file:
            writer = csv.writer(csv_file)
            # Write the header based on keys from the first dictionary
            header = data.keys()
            writer.writerow(header)

            # Write each row
            writer.writerow(data.values())
        log.info(f"CSV data saved to {csv_file.name}")


def create_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=f"Net Lasso - by {__author__} ({__about__})",
        epilog="Net Lasso utilises the Netlas.io API to perform advanced searches for "
        "internet-connected (IoT) devices based on user-provided search queries.",
        formatter_class=RichHelpFormatter,
    )
    parser.add_argument("-q", "--query", help="Search query string")
    parser.add_argument(
        "-a",
        "--authenticate",
        help="Authenticate with a valid Netlas.io API Key",
    )
    parser.add_argument(
        "-p",
        "--page",
        type=int,
        default=0,
        help="Page number to get results from (default: %(default)s)",
    )
    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=10,
        help="Number of results to return (default: %(default)s)",
    )
    parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")
    parser.add_argument(
        "-r", "--raw", help="Return results in raw JSON format", action="store_true"
    )

    parser.add_argument(
        "-j", "--json", help="Write results to a JSON file", action="store_true"
    )
    parser.add_argument(
        "-c", "--csv", help="Write results to a CSV file", action="store_true"
    )
    parser.add_argument(
        "-v", "--version", version=f"Net Lasso v{__version__}", action="version"
    )

    return parser


log = setup_logging(debug_mode=create_parser().parse_args().debug)

# Construct path to the program's directory
PROGRAM_DIRECTORY = os.path.expanduser(os.path.join("~", "netlasso"))

# Construct path to the current file's directory
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
# Construct paths to directories of CSV and JSON files.
CSV_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "csv")
JSON_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "json")
