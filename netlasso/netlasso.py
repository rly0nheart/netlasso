def on_query():
    from datetime import datetime

    from rich.prompt import Prompt, Confirm

    from .api import Api
    from .coreutils import (
        args,
        log,
        message,
        path_finder,
        __version__,
    )
    from .masonry import Masonry

    print(
        """
┳┓     ┓       
┃┃┏┓╋  ┃ ┏┓┏┏┏┓
┛┗┗ ┗  ┗┛┗┻┛┛┗┛"""
    )

    start_time = datetime.now()
    path_finder()

    try:
        api = Api(
            netlas_api_endpoint="https://app.netlas.io/api",
            github_api_endpoint="https://api.github.com",
        )
        query = args.query or Prompt.ask("Enter search query", default="port:7070")
        page = args.page or Prompt.ask(
            "From which page would you like to get results?", default="0"
        )

        if args.query:
            log.info(
                message(
                    message_type="info",
                    message_key="program_started",
                    program_name="Net Lasso",
                    program_version=__version__,
                    start_time=start_time.strftime("%a %b %d %Y, %I:%M:%S %p"),
                )
            )
            api.check_updates()

        search_results = api.search(query=query, page=int(page))
        if search_results:
            tree_masonry = Masonry(
                query=query,
                results=search_results,
                limit=args.limit
                if hasattr(args, "limit")
                else Prompt.ask("How many results would you like to show?", default=10),
                save_json=args.json
                if hasattr(args, "json")
                else Confirm.ask(
                    "Would you like to save the output to a JSON file?", default=False
                ),
                save_csv=args.csv
                if hasattr(args, "csv")
                else Confirm.ask(
                    "Would you like to save the output to a CSV file?", default=False
                ),
                return_raw=args.raw
                if hasattr(args, "raw")
                else Confirm.ask(
                    "Would you like to return results in raw JSON format?",
                    default=False,
                ),
            )
            tree_masonry.visualise_results()
        else:
            log.info(f"No results found for [italic][yellow]{query}[/][/]")

    except KeyboardInterrupt:
        log.warning(message(message_type="warning", message_key="user_interruption"))
    except Exception as error:
        log.error(
            message(
                message_type="error", message_key="unknown_error", error_message=error
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
