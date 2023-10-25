from datetime import datetime

from .api import Api
from .coreutils import (
    create_parser,
    log,
    message,
    path_finder,
    __version__,
)
from .masonry import TreeMason


def on_call():
    start_time = datetime.now()
    args = create_parser().parse_args()

    print(
        """
┳┓     ┓       
┃┃┏┓╋  ┃ ┏┓┏┏┏┓
┛┗┗ ┗  ┗┛┗┻┛┛┗┛"""
    )

    try:
        log.info(
            message(
                message_type="info",
                message_key="program_started",
                program_name="Net Lasso",
                version=__version__,
                start_time=start_time,
            )
        )

        api = Api()
        path_finder()

        api.check_updates()
        search_results = api.search(query=args.query, page=args.page)

        tree_masonry = TreeMason(
            query=args.query,
            results=search_results,
            limit=args.limit,
            save_json=args.json,
            save_csv=args.csv,
            return_raw=args.raw,
        )
        tree_masonry.visualise_results()

    except KeyboardInterrupt:
        log.warning(message(message_type="warning", message_key="user_interruption"))
    except Exception as e:
        log.error(
            message(message_type="error", message_key="unknown_error", error_message=e)
        )
    finally:
        log.info(
            message(
                message_type="info",
                message_key="program_stopped",
                run_time=datetime.now() - start_time,
            )
        )
