import asyncio
from datetime import datetime

from rich import print

from .api import API
from .coreutils import (
    __version__,
    create_parser,
    log,
    message,
    path_finder,
)
from .tree_masonry import results_tree


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
                results_tree(
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
