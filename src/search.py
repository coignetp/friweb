import os

from read_data import create_index
from collections import OrderedDict

def search(query: str, index: OrderedDict, searchType: str) -> list:
  print(f"Search for {query} with {searchType} search")

  # TODO: do real search
  found_files = [
    "data/0/3dradiology.stanford.edu_",
    "data/2/foodallergies.stanford.edu_about_us_contact_us.html",
    "data/2/iis-db.stanford.edu_evnts_4795_flyer.pdf",
    "data/7/www-project.slac.stanford.edu_ilc_acceldev_injector_ILCPES_index.htm",
  ]

  return found_files