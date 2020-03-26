import os

from read_data import load_inverted_index
from boolean_search import boolean_search
from vectorial_search import vectorial_search

from collections import OrderedDict


def search(query: str, inv_index: OrderedDict, searchType: str) -> list:
    print(f"Search for {query} with {searchType} search")

    if searchType == 'boolean':
        return boolean_search(query, inv_index)

    elif searchType == 'vector':
        return vectorial_search(query, inv_index)

    return []


# if __name__ == '__main__':
#     inv_index = load_inverted_index("index/simple.index")
#     print(search("stanford class", inv_index, "vector"))
