from datetime import datetime

import netlas
from rich import print
from rich.tree import Tree

from .coreutils import (
    __version__,
    create_parser,
    get_api_key,
    log,
    save_data,
)
from .tree_masonry import result_branch


def search(query: str, page: int, api_key: str = None) -> list:
    """
    Searches Netlas.io and fetches search results that match a given query.

    :param query: Search query string.
    :param page: Page number to get results from (default is 0)
    :param api_key: A valid Netlas.io API key.
    :return: A list of results that matched the query.
    """
    apikey = get_api_key(api_key=api_key)
    netlas_query = None
    try:
        # create new connection to Netlas
        netlas_connection = netlas.Netlas(api_key=apikey)
        # retrieve data from responses by query `port:7001`
        netlas_query = netlas_connection.query(query=query, page=page)
    except netlas.exception.APIError as e:
        log.error(e)

    return netlas_query.get("items")


def visualise_results(
    results: list,
    limit: int,
    save_to_json: bool,
    save_to_csv: bool,
    return_raw: bool = False,
):
    """
    Saves and visualises the search results into a tree structure.

    :param results: A list of search results from the search() function.
    :param limit: Number of results to visualise (default is 10).
    :param save_to_json: A boolean value to indicate whether to save data to a JSON file.
    :param save_to_csv: A boolean value to indicate whether to save data to a CSV file.
    :param return_raw: A boolean value indicating whether results should be printed in raw JSON format.
    """
    main_tree = Tree(
        f"Showing [cyan]{limit}[/] results - {datetime.now()}",
        style="bold",
        guide_style="bold bright_blue",
    )
    if results:
        # iterate over data and print: IP address, port, path and protocol
        for result_index, result in enumerate(results, start=1):
            raw_result_data = result.get("data")
            if return_raw:
                print(raw_result_data)
                print("\n")
            else:
                result_branch(main_tree=main_tree, result_data=raw_result_data)

            save_data(
                data=raw_result_data,
                save_to_json=save_to_json,
                save_to_csv=save_to_csv,
                filename=raw_result_data.get("isp"),
            )
            if result_index == limit:
                break

        print(main_tree)


def on_call():
    start_time = datetime.now()
    args = create_parser().parse_args()
    api_key = None
    if args.authenticate:
        api_key = get_api_key(api_key=args.authenticate)
    if args.query:
        try:
            print(
                """
┳┓     ┓       
┃┃┏┓╋  ┃ ┏┓┏┏┏┓
┛┗┗ ┗  ┗┛┗┻┛┛┗┛"""
            )
            log.info(f"Starting Net Lasso {__version__} at {start_time}...")

            results = search(query=args.query, page=args.page, api_key=api_key)
            visualise_results(
                results=results,
                return_raw=args.raw,
                limit=args.limit,
                save_to_csv=args.csv,
                save_to_json=args.json,
            )
        except KeyboardInterrupt:
            log.warning("User interruption detected (Ctrl+C)")
        except Exception as e:
            log.error(f"An error occurred: {e}")
        finally:
            log.info(f"Stopped in {datetime.now() - start_time} seconds.")
