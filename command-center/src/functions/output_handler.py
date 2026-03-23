def handle_output(response: str) -> dict:
    """
    Processes the output data and returns a formatted result.

    Args:
        data (str): The output data to be processed.

    Returns:
        dict: A dictionary containing the 'path' and 'output' extracted from the response.
    """

    if not isinstance(response, str):
        return {
            "path": "",
            "output": response
        }

    if '|' not in response:
        return {
            "path": "",
            "output": response
        }

    path, _, output = response.partition('|')

    return {
        "path": path,
        "output": output
    }