# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import asyncio
from dataclasses import dataclass
from datetime import datetime

import aiohttp
from rich.pretty import pprint

from . import __version__
from .api import get_results, check_updates
from .coreutils import args, log, save_data, pathfinder


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@dataclass
class Host:
    isp: str
    ip: str
    port: int
    uri: str
    host: str
    host_type: str
    domains: str
    protocol: str
    prot4: str
    path: str
    last_updated: str
    last_seen: str
    location: dict
    whois: dict
    certificate: dict
    raw_data: dict


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def search(query: str, page: int) -> list[Host]:
    async with aiohttp.ClientSession() as session:
        await check_updates(session=session)

        results: list = await get_results(query=query, page=page, session=session)
        results_list: list = []
        if results:
            for result in results:
                data: dict = result.get("data")
                host = Host(
                    isp=data.get("isp"),
                    ip=data.get("ip"),
                    port=data.get("port"),
                    uri=data.get("uri"),
                    host=data.get("host"),
                    host_type=data.get("host_type"),
                    domains=data.get("domain"),
                    protocol=data.get("protocol"),
                    prot4=data.get("prot4"),
                    path=data.get("path"),
                    location=data.get("geo"),
                    whois=data.get("whois"),
                    certificate=data.get("certificate"),
                    last_updated=data.get("last_updated"),
                    last_seen=data.get("last_seen"),
                    raw_data=data,
                )
                results_list.append(host)
            return results_list
        else:
            log.info(f"No results found for {query}.")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def on_query():
    # -------------------------------------------------------- #

    start_time = datetime.now()

    # -------------------------------------------------------- #

    print(
        """
┳┓     ┓       
┃┃┏┓╋  ┃ ┏┓┏┏┏┓
┛┗┗ ┗  ┗┛┗┻┛┛┗┛"""
    )

    log.info(
        f"[bold]Net Lasso[/] {__version__} started at {start_time.strftime('%a %b %d %Y, %I:%M:%S%p')}..."
    )

    # -------------------------------------------------------- #

    try:
        pathfinder()
        function_data: list = asyncio.run(search(query=args.query, page=args.page))
        pprint(function_data, expand_all=True)

        if args.json or args.csv:
            save_data(
                data=function_data,
                filename=args.query,
                save_json=args.json,
                save_csv=args.csv,
            )

    except KeyboardInterrupt:
        log.warning("User interruption detected (Ctrl+C)")
    finally:
        log.info(f"Stopped in {datetime.now() - start_time} seconds.")


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
