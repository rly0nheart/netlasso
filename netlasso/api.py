import aiohttp

from .coreutils import log
from .messages import message


class API:
    BASE_NETLAS_API_ENDPOINT = "https://app.netlas.io/api"
    BASE_GITHUB_API_ENDPOINT = "https://api.github.com"

    def __init__(self):
        self.search_endpoint = (
            f"{API.BASE_NETLAS_API_ENDPOINT}/responses/?q=%s&start=%s"
        )
        self.updates_endpoint = ""

    @staticmethod
    async def get_data(endpoint: str) -> dict:
        """
        Asynchronously fetches JSON data from a given API endpoint.

        :param endpoint: The API endpoint to fetch data from.
        :return: A JSON object from the endpoint.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        error_message = await response.json()
                        log.error(
                            message(
                                message_type="error",
                                message_key="api_error",
                                error_message=error_message,
                            )
                        )
        except aiohttp.ClientError as e:
            log.error(
                message(
                    message_type="error",
                    message_key="http_error",
                    error_message=str(e),
                )
            )
        except Exception as e:
            log.critical(
                message(
                    message_type="error",
                    message_key="unexpected_error",
                    error_message=str(e),
                )
            )

    async def search(self, query: str, page: int):
        """
        Searches Netlas.io and fetches search results that match a given query.

        :param query: Search query string.
        :param page: Page number to get results from (default is 0)
        :return: A list of results that matched the query.
        """
        search_results = await self.get_data(
            endpoint=self.search_endpoint % (query, page)
        )
        return search_results.get("items")
