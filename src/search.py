import os
import tkinter as tk

from read_data import create_index

found_files = []

def search(query: str, resultsWidget: tk.Listbox) -> list:
  if not os.path.exists('index/simple.index'):
    print("Creating index..")
    create_index()
  
  print(f"Search for {query}")

  # TODO: do real search
  found_files = ["azer", "azertzg", "qflqdfq", "mkl,ml,"]

  resultsWidget.delete(0, tk.END)
  for a_file in found_files:
    resultsWidget.insert(tk.END, a_file)