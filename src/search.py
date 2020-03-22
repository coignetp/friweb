import os

from read_data import create_index
from boolean_search import boolean_search

from collections import OrderedDict

def search(query: str, inv_index: OrderedDict, searchType: str) -> list:
  print(f"Search for {query} with {searchType} search")

  if searchType == 'boolean':
    return boolean_search(query, inv_index)

  elif searchType == 'vector':
    # TODO: do real search
    return [
      "data/0/3dradiology.stanford.edu_",
      "data/2/foodallergies.stanford.edu_about_us_contact_us.html",
      "data/2/iis-db.stanford.edu_evnts_4795_flyer.pdf",
      "data/7/www-project.slac.stanford.edu_ilc_acceldev_injector_ILCPES_index.htm",
    ]

  return []