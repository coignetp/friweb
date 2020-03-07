import os

from read_data import create_index


def search(query: str) -> list:
  if not os.path.exists('index/simple.index'):
    print("Creating index..")
    create_index()
  
  print(f"Search for {query}")

  # TODO: do real search
  found_files = [
    "data/0/3dradiology.stanford.edu_",
    "data/2/foodallergies.stanford.edu_about_us_contact_us.html",
    "data/2/iis-db.stanford.edu_evnts_4795_flyer.pdf",
    "data/7/www-project.slac.stanford.edu_ilc_acceldev_injector_ILCPES_index.htm",
  ]

  return found_files