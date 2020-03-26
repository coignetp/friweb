import os

from boolean_search import boolean_search
from vector_search import vector_search

from collections import OrderedDict


def search(query: str, inv_index: OrderedDict, stats_collection: OrderedDict, searchType: str) -> list:
    print(f"Search for {query} with {searchType} search")

    if searchType == 'boolean':
        return boolean_search(query, inv_index)

    elif searchType == 'vector':
        return vector_search(query, inv_index, stats_collection)

    return []
