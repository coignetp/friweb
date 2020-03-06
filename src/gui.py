import tkinter as tk
from functools import partial

from search import search

if __name__ == "__main__":
  window = tk.Tk()

  window.title("Friweb")

  results = tk.Listbox(window)
  results.pack(side=tk.BOTTOM,fill=tk.BOTH, pady=10, padx=10, expand=True)

  searchBar = tk.Entry(window)
  searchBar.pack(side=tk.LEFT, pady=10, padx=10, expand=True, fill=tk.X)
  searchButton = tk.Button(window, text="Search", command=lambda: search(searchBar.get(), results))
  searchButton.pack(side=tk.RIGHT, pady=10, padx=10)

  window.resizable(True, True)
  window.mainloop()