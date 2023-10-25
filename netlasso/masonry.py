from datetime import datetime
from typing import Union

from rich import print
from rich.tree import Tree

from .coreutils import format_api_data, save_data


class TreeMason:
    def __init__(
        self,
        query: str,
        results: list,
        limit: int,
        save_json: bool,
        save_csv: bool,
        return_raw: bool = False,
    ):
        """
        Initialises the TreeMason class with results' data to populate the main_tree with.

        :param query: A search query string.
        :param results: A list of JSON objects each containing result data.
        :param limit: Number of results to show.
        :param save_json: A boolean value indicating whether each result should be saved to a JSON file.
        :param save_csv: A boolean value indicating whether each result should be saved to a CSV file.
        :param return_raw: A boolean value indicating whether results
            should not be visualised in a tree and instead be printed in raw JSON format.
        """
        self.results = results
        self.limit = limit
        self.save_json = save_json
        self.save_csv = save_csv
        self.return_raw = return_raw
        self.main_tree = Tree(
            f"Visualising [cyan]{self.limit}[/] results for [italic][yellow]{query}[/][/] - {datetime.now()}",
            guide_style="bold bright_blue",
        )

    @staticmethod
    def add_branch(
        target_tree: Tree,
        branch_title: str,
        branch_data: Union[dict, list],
        additional_text: str = None,
    ) -> Tree:
        """
        Adds a branch to a specified tree and populates it with the given data.

        :param target_tree: Tree to add the branch to.
        :param branch_title: Branch title.
        :param branch_data: Branch data
        :param additional_text: Additional text to add at the end of the branch.
        :return: A populated branch.
        """
        branch = target_tree.add(branch_title)
        data_types = [dict, list]
        if type(branch_data) in data_types:
            if type(branch_data) is dict:
                for key, value in branch_data.items():
                    branch.add(f"{key}: {value}", style="dim")
                if additional_text:
                    branch.add(additional_text, style="italic")
            else:
                for index, item in enumerate(branch_data, start=1):
                    branch.add(f"{index}. {item}", style="italic")
        return branch

    def result_branch(self, main_tree: Tree, result_data: dict) -> Tree:
        """
        Adds a result_branch to the main_tree and populates it with result_data.

        :param main_tree: Tree to add the branch to.
        :param result_data: Data to populate the branch with.
        :return: main_tree with the populated result_branch.
        """
        summary_data = format_api_data(api_data=result_data, data_file="summary.json")

        # Add a summary branch to the main_tree and populate it with the summary data
        branch = main_tree.add(result_data.get("isp"))
        for summary_key, summary_value in summary_data.items():
            branch.add(f"{summary_key}: {summary_value}", style="dim")

        # Add a location branch to the main_tree and populate it with location data
        self.add_branch(
            target_tree=branch,
            branch_title="Location",
            branch_data=format_api_data(
                api_data=result_data.get("geo"), data_file="location.json"
            ),
        )

        # Add a WHOIS branch to the main_tree and populate it with WHOIS data (ASN, NET)
        whois_branch = branch.add("WHOIS")
        self.add_branch(
            target_tree=whois_branch,
            branch_title="Net",
            branch_data=format_api_data(
                api_data=result_data.get("whois").get("net"),
                data_file="net.json",
            ),
            additional_text=result_data.get("whois").get("net").get("description"),
        )
        self.add_branch(
            target_tree=whois_branch,
            branch_title="ASN",
            branch_data=format_api_data(
                api_data=result_data.get("whois").get("asn"),
                data_file="asn.json",
            ),
        )

        # Add a Domains branch to the main_tree and populate it with a list of domains associated with the result
        if result_data.get("domain"):
            self.add_branch(
                target_tree=branch,
                branch_title="Domains",
                branch_data=result_data.get("domain"),
            )

        return main_tree

    def visualise_results(self):
        """
        Saves and visualises the search results into a tree structure.
        """
        if self.results:
            for result_index, result in enumerate(self.results, start=1):
                raw_result_data = result.get("data")

                # If -r/--raw is passed, return results in raw JSON format
                if self.return_raw:
                    print(raw_result_data)
                    print("\n")
                else:
                    # Otherwise, populate the result_branch and add it to the main_tree
                    self.result_branch(
                        main_tree=self.main_tree, result_data=raw_result_data
                    )

                # Save each result to a file (if the right command-line arguments are passed)
                save_data(
                    data=raw_result_data,
                    save_to_json=self.save_json,
                    save_to_csv=self.save_csv,
                    filename=f"{raw_result_data.get('isp')}_{raw_result_data.get('ip')}",
                )

                # If result_index is equal to the limit, break the loop and visualise the main_tree
                if result_index == self.limit:
                    break

            if not self.return_raw:
                print(self.main_tree)
