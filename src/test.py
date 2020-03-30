from search import search
from read_data import load_inverted_index, load_stats_collection

queries = {}

with open("queries/queries.txt", "r") as f:
    while True:
        query = f.readline()
        filepath = f.readline()
        if query:
            queries[query.strip()] = filepath.strip()
        else:
            break
        print(query.strip())

inv_index = load_inverted_index("index/simple.index")
stats_collection = load_stats_collection("index/stats_collection.json")

for query in queries:
    result_boolean = search(query, inv_index, stats_collection, "boolean")
    result_vector = search(query, inv_index, stats_collection, "vector")

    output = []
    with open(queries[query], "r") as f:
        output = f.readlines()
        output = [line.strip() for line in output]

    result_vector = [doc for doc in result_vector]
    # Documents qui sont dans les documents attendus mais pas dans le résultat
    a = list(set(output) - set(result_vector))
    # Documents qui sont dans le résultat mais pas dans les documents attendus
    b = list(set(result_vector) - set(output))

    if len(list(result_vector)) != 0 and len(list(output)) != 0:
        print("Requête : " + query)
        print("Modèle : Vectoriel")
        print("Précision : " +
              str((len(set(result_vector) - set(b)))/len(result_vector)))
        print("Rappel : " + str((len(set(result_vector) - set(b)))/len(output)))
    else:
        print("Requête : " + query)
        print("Modèle : Vectoriel")
        print("Précision : " + str(0))
        print("Rappel : " + str(0))

    # Documents qui sont dans les documents attendus mais pas dans le résultat
    a = list(set(output) - set(result_boolean))
    # Documents qui sont dans le résultat mais pas dans les documents attendus
    b = list(set(result_boolean) - set(output))

    if len(list(result_boolean)) != 0 and len(list(output)) != 0:
        print("Requête : " + query)
        print("Modèle : Boolean")
        print("Précision : " +
              str((len(set(result_boolean) - set(b)))/len(result_boolean)))
        print("Rappel : " + str((len(set(result_boolean) - set(b)))/len(output)))
    else:
        print("Requête : " + query)
        print("Modèle : Boolean")
        print("Précision : " + str(0))
        print("Rappel : " + str(0))
