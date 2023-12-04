# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import aiohttp

from .coreutils import log

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

NETLAS_API_ENDPOINT: str = "https://app.netlas.io/api"
PYPI_PROJECT_ENDPOINT: str = "https://pypi.org/pypi/netlasso/json"


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_data(endpoint: str, session: aiohttp.ClientSession) -> dict:
    """
    Fetches JSON data from a given API endpoint.

    :param endpoint: The API endpoint to fetch data from.
    :param session: aiohttp session to use for the request.
    :return: A JSON object from the endpoint if request was successful.
        An empty JSON object if request was unsuccessful.
    """
    try:
        async with session.get(url=endpoint) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message: dict = await response.json()
                log.error(f"An API error occurred: {error_message}")
                return {}
    except aiohttp.ClientConnectionError as error:
        log.error(f"An HTTP error occurred: [red]{error}[/]")
        return {}
    except Exception as error:
        log.critical(f"An unknown error occurred: [red]{error}[/]")
        return {}


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_results(
    query: str, page: int, session: aiohttp.ClientSession
) -> list[dict]:
    """
    Searches Netlas.io and fetches search results that match a given query.

    :param query: Search query string.
    :param page: Page to start from.
    :param session: aiohttp session to use for the request.
    :return: A list of results that matched the query.
    """
    response: dict = await get_data(
        endpoint=f"{NETLAS_API_ENDPOINT}/responses/?q={query}&start={page}",
        session=session,
    )
    results: list = response.get("items", [])

    return results


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def check_updates(session: aiohttp.ClientSession):
    """
    Gets and compares the current program version with the remote version.

    Assumes version format: major.minor.patch.prefix

    :param session: aiohttp session to use for the request.
    """
    from . import __version__

    # Make a GET request to PyPI to get the project's latest release.
    response: dict = await get_data(endpoint=PYPI_PROJECT_ENDPOINT, session=session)

    if response.get("info"):
        remote_version: str = response.get("info").get("version")
        # Splitting the version strings into components
        remote_parts: list = remote_version.split(".")
        local_parts: list = __version__.split(".")

        update_message: str = ""

        # ---------------------------------------------------------- #

        # Check for differences in version parts
        if remote_parts[0] != local_parts[0]:
            update_message = (
                f"MAJOR update ({remote_version}) available:"
                f" It might introduce significant changes."
            )

        # ---------------------------------------------------------- #

        elif remote_parts[1] != local_parts[1]:
            update_message = (
                f"MINOR update ({remote_version}) available:"
                f" Includes small feature changes/improvements."
            )

        # ---------------------------------------------------------- #

        elif remote_parts[2] != local_parts[2]:
            update_message = (
                f"PATCH update ({remote_version}) available:"
                f" Generally for bug fixes and small tweaks."
            )

        # ---------------------------------------------------------- #

        elif (
            len(remote_parts) > 3
            and len(local_parts) > 3
            and remote_parts[3] != local_parts[3]
        ):
            update_message = (
                f"BUILD update ({remote_version}) available."
                f" Might be for specific builds or special versions."
            )

        # ---------------------------------------------------------- #

        if update_message:
            log.info(update_message)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
