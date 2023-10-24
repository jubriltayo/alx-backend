#!/usr/bin/env python3
"""This module defines class `Server` using a helper function `index_range`"""

import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    A helper function to give range of index
    """
    if page < 1:
        start_index = 0
    else:
        start_index = (page - 1) * page_size

    end_index = start_index + page_size
    result = (start_index, end_index)

    return result


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """gets a specific page from the dataset"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        # unpack tuple
        start_index, end_index = index_range(page, page_size)

        return self.dataset()[start_index: end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """returns a dictionary that contains information about
            current page and hypermedia pagination details
        """
        total_pages = math.ceil(len(self.dataset()) / page_size)

        return {
                    "page_size": page_size,
                    "page": page,
                    "data": self.get_page(page, page_size),
                    "next_page": page + 1 if page < total_pages else None,
                    "prev_page": page - 1 if page > 1 else None,
                    "total_pages": total_pages
            }
