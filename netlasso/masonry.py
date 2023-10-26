from datetime import datetime
from typing import Union

from rich import print
from rich.tree import Tree

from .coreutils import data_broker, save_data


class Masonry:
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
        Masonry class creates and populates the main_tree with branches
        containing data on each result from the results list.

        :param query: A search query string.
        :param results: A list of JSON objects each containing result data.
        :param limit: Number of results to show.
        :param save_json: A boolean value indicating whether each result should be saved to a JSON file.
        :param save_csv: A boolean value indicating whether each result should be saved to a CSV file.
        :param return_raw: A boolean value indicating whether results
            should not be visualised in a tree and instead be printed in raw JSON format.
        """
        current_time = datetime.now()
        self.results = results
        self.limit = limit
        self.save_json = save_json
        self.save_csv = save_csv
        self.return_raw = return_raw

        self.first_branch_guide_style: str = "bold blue"
        self.second_branch_guide_style: str = "dim blue"
        self.main_tree = Tree(
            f"Showing [cyan]{self.limit}[/] results for [italic][yellow]{query}[/][/] at "
            f"{current_time.strftime('%a %b %d %Y, %H:%M:%S %p')}",
            guide_style="bold bright_blue",
        )

    def add_branch(
        self,
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
        branch = target_tree.add(
            branch_title, guide_style=self.second_branch_guide_style
        )
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

    def certificate_branch(self, result_branch: Tree, certificate_data: dict) -> Tree:
        """
        Adds and populates a Certificate branch to the result_branch.

        :param result_branch: Branch to which the certificate_branch will be added.
        :param certificate_data: A JSON object containing a result's certificate data to populate the branch with.
        :return: result_branch with a populated certificate_branch added to it.
        """
        certificate_branch = result_branch.add("[bold]Certificate[/]")
        self.add_branch(
            target_tree=certificate_branch,
            branch_title=certificate_data.get("serial_number"),
            branch_data=data_broker(
                api_data=certificate_data,
                data_file="certificate/summary.json",
            ),
        )
        self.add_branch(
            target_tree=certificate_branch,
            branch_title="[bold]Issuer[/]",
            branch_data=data_broker(
                api_data=certificate_data.get("issuer"),
                data_file="certificate/issuer.json",
            ),
        )
        self.add_branch(
            target_tree=certificate_branch,
            branch_title="[bold]Validity[/]",
            branch_data=certificate_data.get("validity"),
        )

        if certificate_data.get("names"):
            self.add_branch(
                target_tree=certificate_branch,
                branch_title="[bold]Names[/]",
                branch_data=certificate_data.get("names"),
            )

        return result_branch

    def whois_branch(self, result_branch: Tree, whois_data: dict) -> Tree:
        """
        Adds and populates a WHOIS branch to the result_branch.

        :param result_branch: Branch to which the whois_branch will be added.
        :param whois_data: A JSON object containing a result's WHOIS data to populate the branch with.
        :return: result_branch with a populated whois_branch added to it.
        """
        whois_branch = result_branch.add("[bold]WHOIS[/]")
        self.add_branch(
            target_tree=whois_branch,
            branch_title="[bold]Net[/]",
            branch_data=data_broker(
                api_data=whois_data.get("net"),
                data_file="host/net.json",
            ),
            additional_text=whois_data.get("net").get("description"),
        )
        self.add_branch(
            target_tree=whois_branch,
            branch_title="[bold]ASN[/]",
            branch_data=data_broker(
                api_data=whois_data.get("asn"),
                data_file="host/asn.json",
            ),
        )

        return result_branch

    def result_branch(self, main_tree: Tree, result_data: dict) -> Tree:
        """
        Adds a result_branch to the main_tree and populates it with result_data.

        :param main_tree: Tree to add the branch to.
        :param result_data: Data to populate the branch with.
        :return: main_tree with the populated result_branch.
        """
        summary_data = data_broker(api_data=result_data, data_file="host/summary.json")

        # Add a summary branch to the main_tree and populate it with the summary data
        branch = main_tree.add(
            result_data.get("isp"), guide_style=self.first_branch_guide_style
        )
        for summary_key, summary_value in summary_data.items():
            branch.add(f"{summary_key}: {summary_value}", style="dim")

        # Add a location branch to the main_tree and populate it with location data
        self.add_branch(
            target_tree=branch,
            branch_title="[bold]Location[/]",
            branch_data=data_broker(
                api_data=result_data.get("geo"), data_file="host/location.json"
            ),
        )
        self.whois_branch(result_branch=branch, whois_data=result_data.get("whois"))

        if result_data.get("certificate"):
            self.certificate_branch(
                result_branch=branch, certificate_data=result_data.get("certificate")
            )

        # Add a Domains branch to the main_tree and populate it with a list of domains associated with the result
        if result_data.get("domain"):
            self.add_branch(
                target_tree=branch,
                branch_title="[bold]Domains[/]",
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
