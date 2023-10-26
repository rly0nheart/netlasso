def on_query():
    from datetime import datetime

    from .api import Api
    from .coreutils import (
        args,
        log,
        message,
        path_finder,
        __version__,
    )
    from .masonry import Masonry

    start_time = datetime.now()

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
                program_version=__version__,
                start_time=start_time.strftime("%a %b %d %Y, %I:%M:%S %p"),
            )
        )
        path_finder()

        api = Api(
            netlas_api_endpoint="https://app.netlas.io/api",
            github_api_endpoint="https://api.github.com",
        )

        api.check_updates()
        search_results = api.search(query=args.query, page=args.page)
        if search_results:
            tree_masonry = Masonry(
                query=args.query,
                results=search_results,
                limit=args.limit,
                save_json=args.json,
                save_csv=args.csv,
                return_raw=args.raw,
            )
            tree_masonry.visualise_results()
        else:
            log.info(f"No results found for [italic][yellow]{args.query}[/][/]")

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
