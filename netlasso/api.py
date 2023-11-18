import requests

from .coreutils import log, __version__
from .messages import message


class Api:
    def __init__(self, netlas_api_endpoint: str, github_api_endpoint: str):
        self.search_endpoint = f"{netlas_api_endpoint}/responses/?q=%s&start=%s"
        self.updates_endpoint = (
            f"{github_api_endpoint}/repos/rly0nheart/netlasso/releases/latest"
        )

    @staticmethod
    def get_data(endpoint: str) -> dict:
        """
        Fetches JSON data from a given API endpoint.

        :param endpoint: The API endpoint to fetch data from.
        :return: A JSON object from the endpoint if request was successful.
            An empty JSON object if request unsuccessful.
        """
        try:
            with requests.get(url=endpoint) as response:
                if response.status_code == 200:
                    return response.json()
                else:
                    log.error(
                        message(
                            message_type="error",
                            message_key="api_error",
                            error_message=response.json(),
                        )
                    )
                    return {}
        except requests.exceptions.RequestException as error:
            log.error(
                message(
                    message_type="error",
                    message_key="http_error",
                    error_message=error,
                )
            )
            return {}
        except Exception as error:
            log.critical(
                message(
                    message_type="error",
                    message_key="unexpected_error",
                    error_message=error,
                )
            )
            return {}

    def check_updates(self):
        """
        Checks for updates from the program's releases.
        If the release version does not match the current program version, assume the program is outdated.
        """
        from rich.markdown import Markdown
        from rich import print

        response = self.get_data(endpoint=self.updates_endpoint)
        if response.get("tag_name"):
            remote_version = response.get("tag_name")
            if remote_version != __version__:
                log.info(
                    message(
                        message_type="info",
                        message_key="update_found",
                        program_name="Net Lasso",
                        program_call_name="netlasso",
                        release_version=remote_version,
                    )
                )

                release_notes = Markdown(response.get("body"))
                print(release_notes)

    def search(self, query: str, page: int):
        """
        Searches Netlas.io and fetches search results that match a given query.

        :param query: Search query string.
        :param page: Page number to get results from (default is 0)
        :return: A list of results that matched the query.
        """
        search_results = self.get_data(endpoint=self.search_endpoint % (query, page))
        return search_results.get("items", [])
