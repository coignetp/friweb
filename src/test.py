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
    # result_boolean = search(query, inv_index, stats_collection, "boolean")
    result_vector = search(query, inv_index, stats_collection, "vector")

    output = []
    with open(queries[query], "r") as f:
        output = f.readlines()
        output = [line.strip() for line in output]

    # for result in result_vector:
    #     if result.strip("data/") not in output:
    #         print(result, result_vector[result])

    a = len(list(set(output) - set([doc.strip("data/") for doc in result_vector])))
    b = len(list(set([doc.strip("data/") for doc in result_vector]) - set(output)))
    
    if len(list(result_vector)) != 0 and len(list(output)) != 0:
        print("Requête : " + query)
        print("Modèle : Vectoriel")
        print("Précision : " + str((len(list(result_vector)) - b)/len(list(result_vector))))
        print("Rappel : " + str((len(list(result_vector)) - b)/len(list(output))))
    else:
        print("Requête : " + query)
        print("Modèle : Vectoriel")
        print("Précision : " + str(0))
        print("Rappel : " + str(0))
