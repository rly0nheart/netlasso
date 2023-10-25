from datetime import datetime
from typing import Union

from rich import print
from rich.tree import Tree

from .coreutils import format_api_data, save_data


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


def result_branch(main_tree: Tree, result_data: dict) -> Tree:
    """
    Adds a result_branch to the main_tree and populates it with result_data.

    :param main_tree: Tree to add the branch to.
    :param result_data: Data to populate the branch with.
    :return: main_tree with the populated result_branch.
    """
    summary_data = format_api_data(api_data=result_data, data_file="summary.json")

    # Add a summary branch to the main tree and populate it with the summary data
    branch = main_tree.add(result_data.get("isp"))
    for summary_key, summary_value in summary_data.items():
        branch.add(f"{summary_key}: {summary_value}", style="dim")

    # Add a location branch to the main tree and populate it with location data
    add_branch(
        target_tree=branch,
        branch_title="Location",
        branch_data=format_api_data(
            api_data=result_data.get("geo"), data_file="location.json"
        ),
    )

    # Add a WHOIS branch to the main tree and populate it with WHOIS data (ASN, NET)
    whois_branch = branch.add("WHOIS")
    add_branch(
        target_tree=whois_branch,
        branch_title="Net",
        branch_data=format_api_data(
            api_data=result_data.get("whois").get("net"),
            data_file="net.json",
        ),
        additional_text=result_data.get("whois").get("net").get("description"),
    )
    add_branch(
        target_tree=whois_branch,
        branch_title="ASN",
        branch_data=format_api_data(
            api_data=result_data.get("whois").get("asn"),
            data_file="asn.json",
        ),
    )
    if result_data.get("domain"):
        add_branch(
            target_tree=branch,
            branch_title="Domains",
            branch_data=result_data.get("domain"),
        )

    return main_tree


async def results_tree(
    results: list,
    limit: int,
    save_to_json: bool,
    save_to_csv: bool,
    return_raw: bool = False,
):
    """
    Saves and visualises the search results into a tree structure.

    :param results: A list of search results from the search() function.
    :param limit: Number of results to visualise (default is 10).
    :param save_to_json: A boolean value to indicate whether to save data to a JSON file.
    :param save_to_csv: A boolean value to indicate whether to save data to a CSV file.
    :param return_raw: A boolean value indicating whether results should be printed in raw JSON format.
    """
    if results:
        main_tree = Tree(
            f"Showing [cyan]{limit}[/] results - {datetime.now()}",
            style="bold",
            guide_style="bold bright_blue",
        )
        # iterate over data and print: IP address, port, path and protocol
        for result_index, result in enumerate(results, start=1):
            raw_result_data = result.get("data")
            if return_raw:
                print(raw_result_data)
                print("\n")
            else:
                result_branch(main_tree=main_tree, result_data=raw_result_data)

            save_data(
                data=raw_result_data,
                save_to_json=save_to_json,
                save_to_csv=save_to_csv,
                filename=f"{raw_result_data.get('isp')}_{raw_result_data.get('ip')}",
            )
            if result_index == limit:
                break

        if not return_raw:
            print(main_tree)
