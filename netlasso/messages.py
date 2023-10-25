#: Dictionary of general message templates
warning_messages = {
    "user_interruption": "User interruption detected ([yellow]Ctrl+C[/])"
}

#: Dictionary of error message templates
error_messages = {
    "http_error": "HTTP Error: [yellow]{error_message}[/]",
    "api_error": "API Error: {error_message}",
    "unknown_error": "An unknown error occurred: [red]{error_message}[/]",
}

#: Dictionary of informational message templates
info_messages = {
    "program_started": "Started [bold]{program_name}[/] {version} at {start_time}...",
    "program_stopped": "Stopped in {run_time} seconds.",
    "help": "usage: [green]{program_call} -h/--help[/]",
    "data_saved": "{data_type} written to [link file://{file_path}]{file_path}",
    "update": "[bold]{program_name}[/] {version} is available. "
    "To update, run: [italic][green]pip install --upgrade {program_call_name}[/][/]",
}


def message(message_type: str, message_key: str, **kwargs) -> str:
    """
    Generates a formatted message string based on the given message type and key.

    :param message_type: The type of message (e.g., 'general', 'error', 'info').
    :param message_key: The key of the message in the corresponding message dictionary.
    :param kwargs: Additional key-value pairs to fill in the message template.
    :return: The formatted message string.
    """
    message_dict = {
        "warning": warning_messages,
        "error": error_messages,
        "info": info_messages,
    }

    template = message_dict.get(message_type, {}).get(message_key, "Message not found.")
    return template.format(**kwargs)
