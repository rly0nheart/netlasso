from rich.tree import Tree

from .coreutils import format_api_data


def add_branch(
    target_tree: Tree, branch_title: str, branch_data: dict, additional_text: str = None
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
    for key, value in branch_data.items():
        branch.add(f"{key}: {value}", style="dim")
    if additional_text:
        branch.add(additional_text, style="italic")
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

    return main_tree
