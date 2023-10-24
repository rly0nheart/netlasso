import asyncio
from datetime import datetime

from rich import print
from rich.tree import Tree

from .api import API
from .coreutils import (
    __version__,
    create_parser,
    log,
    message,
    path_finder,
    save_data,
)
from .tree_masonry import result_branch


async def visualise_results(
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
    if results:
        main_tree = Tree(
            f"Showing [cyan]{limit}[/] results - {datetime.now()}",
            style="bold",
            guide_style="bold bright_blue",
        )
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
                filename=f"{raw_result_data.get('isp')}_{raw_result_data.get('ip')}",
            )
            if result_index == limit:
                break

        if not return_raw:
            print(main_tree)


def on_call():
    start_time = datetime.now()
    args = create_parser().parse_args()

    if args.query:
        print(
            """
┳┓     ┓       
┃┃┏┓╋  ┃ ┏┓┏┏┏┓
┛┗┗ ┗  ┗┛┗┻┛┛┗┛"""
        )

        try:
            api = API()
            log.info(
                message(
                    message_type="info",
                    message_key="program_started",
                    program_name="Net Lasso",
                    version=__version__,
                    start_time=start_time,
                )
            )
            path_finder()

            search_results = asyncio.run(api.search(query=args.query, page=args.page))
            asyncio.run(
                visualise_results(
                    results=search_results,
                    limit=args.limit,
                    save_to_csv=args.csv,
                    save_to_json=args.json,
                )
            )

        except KeyboardInterrupt:
            log.warning(
                message(message_type="warning", message_key="user_interruption")
            )
        except Exception as e:
            log.error(
                message(
                    message_type="error", message_key="unknown_error", error_message=e
                )
            )
        finally:
            log.info(
                message(
                    message_type="info",
                    message_key="program_stopped",
                    run_time=datetime.now() - start_time,
                )
            )
