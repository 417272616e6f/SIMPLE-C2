def encode_ascii_to_int(command:str):
    """
    Encode a string into its ASCII integer representation.

    Args:
        command (str): The input string to be encoded.

    Returns:
        str: A string of space-separated ASCII values.
    """
    ascii_values = " ".join(str(ord(c)) for c in command)

    return ascii_values

