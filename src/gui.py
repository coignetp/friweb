import tkinter as tk
from functools import partial

from search import search


def tk_search(query: str, resultsWidget: tk.Listbox) -> None:
  found_files = search(query)

  resultsWidget.delete(0, tk.END)
  for a_file in found_files:
    resultsWidget.insert(tk.END, a_file)


def on_listbox_select(selection: str, preview: tk.Text) -> None:
  preview.delete(1.0, tk.END)

  with open(selection) as file:
    preview.insert(tk.END, file.read())


if __name__ == "__main__":
  window = tk.Tk()

  window.title("Friweb")

  topFrame = tk.Frame(window)
  botFrame = tk.Frame(window)

  topFrame.pack(side=tk.TOP, fill=tk.X, expand=True)
  botFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

  results = tk.Listbox(botFrame)
  preview = tk.Text(botFrame)
  searchBar = tk.Entry(topFrame)
  searchButton = tk.Button(topFrame, text="Search", command=lambda: tk_search(searchBar.get(), results))

  searchBar.pack(side=tk.LEFT, pady=10, padx=10, expand=True, fill=tk.X)
  searchButton.pack(side=tk.RIGHT, pady=10, padx=10)

  results.pack(side=tk.LEFT,fill=tk.BOTH, pady=10, padx=10, expand=True)
  preview.pack(side=tk.RIGHT,fill=tk.BOTH, pady=10, padx=10, expand=True)

  # Document selection
  results.bind('<<ListboxSelect>>', lambda evt: on_listbox_select(results.get(results.curselection()[0]), preview))

  window.resizable(True, True)
  window.mainloop()