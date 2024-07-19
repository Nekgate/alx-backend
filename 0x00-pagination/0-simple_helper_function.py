#!/usr/bin/env python3
""" Python script that contains function named index_range
that takes two integer arguments page and page_size.
"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ Returns a tuple containing the start index and end index
    for pagination.
    Args:
        page (int): The current page number.
        page_size (int): The number of items per page.
    Returns:
        tuple[int, int]: A table containing the start index and end index.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return (start_index, end_index)
