#!/usr/bin/env python3
"""Function that returns the start and end index"""


def index_range(page, page_size):
    """
    Calculate the start and end indexes for a given page and page size.

    Args:
    - page (int): The page number (1-indexed).
    - page_size (int): The number of items per page.

    Returns:
    Tuple[int, int]: A tuple containing the start and end indexes.
    """
    if page <= 0 or page_size <= 0:
        raise ValueError("Page and page_size must be positive integers.")

    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    return start_index, end_index
