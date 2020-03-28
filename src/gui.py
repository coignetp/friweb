import tkinter as tk
from functools import partial
from collections import OrderedDict
import os

from read_data import load_inverted_index, load_stats_collection
from search import search


def tk_search(query: str, index: OrderedDict, stats_collection: OrderedDict, searchType: str, resultsWidget: tk.Listbox) -> None:
    found_files = search(query, index, stats_collection, searchType)

    resultsWidget.delete(0, tk.END)
    for a_file in found_files:
        resultsWidget.insert(tk.END, a_file)


def on_listbox_select(selection: str, preview: tk.Text) -> None:
    preview.delete(1.0, tk.END)

    with open(os.path.join('data', selection)) as file:
        preview.insert(tk.END, file.read())


if __name__ == "__main__":
    inv_index = load_inverted_index("index/simple.index")
    stats_collection = load_stats_collection("index/stats_collection.json")

    window = tk.Tk()

    window.title("Friweb")

    topFrame = tk.Frame(window)
    midFrame = tk.Frame(window)
    botFrame = tk.Frame(window)

    topFrame.pack(side=tk.TOP, fill=tk.X, expand=True)
    midFrame.pack(side=tk.TOP, fill=tk.X, expand=True)
    botFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    searchType = tk.StringVar()
    typeBoolean = tk.Radiobutton(
        midFrame, text="Boolean", variable=searchType, value="boolean", justify=tk.LEFT)
    typeBoolean.select()
    typeVector = tk.Radiobutton(
        midFrame, text="Vector", variable=searchType, value="vector", justify=tk.RIGHT)

    results = tk.Listbox(botFrame)
    preview = tk.Text(botFrame)
    searchBar = tk.Entry(topFrame)
    searchButton = tk.Button(topFrame, text="Search", command=lambda: tk_search(
        searchBar.get(), inv_index, stats_collection, searchType.get(), results))

    searchBar.pack(side=tk.LEFT, pady=10, padx=10, expand=True, fill=tk.X)
    searchButton.pack(side=tk.RIGHT, pady=10, padx=10)

    typeBoolean.pack()
    typeVector.pack()

    results.pack(side=tk.LEFT, fill=tk.BOTH, pady=10, padx=10, expand=True)
    preview.pack(side=tk.RIGHT, fill=tk.BOTH, pady=10, padx=10, expand=True)

    # Document selection
    results.bind('<<ListboxSelect>>', lambda evt: on_listbox_select(
        results.get(results.curselection()[0]), preview))

    window.resizable(True, True)
    window.mainloop()
