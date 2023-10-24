#!/usr/bin/env python3
"""This module defines function `index_range`"""

from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    A helper function to give range of index

    Args:
        page (int): page number
        page_size (int): number of items to display on a single page

    Return:
        Tuple: start_index and end_index
    """

    if page < 1:
        start_index = 0
    else:
        start_index = (page - 1) * page_size

    end_index = start_index + page_size
    result = (start_index, end_index)

    return result
