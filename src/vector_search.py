from math import log, sqrt
from collections import Counter, OrderedDict
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from statistics import pstdev, mean

from read_data import article_word_tokenize, remove_stop_words, load_stop_word, tokens_lemmatize
import matplotlib.pyplot as plt


def pre_processed_query(query: str, inverted_index: OrderedDict, nbDoc: int) -> list:
    """
    Résumé
    ---
    Cette fonction transforme la requête en entrée en une liste de tuple (token, poids) traités.
    On élimine notamment les stop words et on lemmatize les termes.
    Le poids est calculé par tf-idf.

    Note: Il est possible de donner plus de poids à un mot dans la requête en lui ajoutant "^poids(int)" à la fin (ex: "hello^1000 how are^10 you^100")

    Paramètres
    ---
    query: la requête à exécuter
    inverted_index: l'index inversé de la collection
    nbDoc: nombre de document dans la collection
    """
    stop_words = load_stop_word("data/stop_words.txt")

    counter_query = Counter()
    tokenized_query = article_word_tokenize(query)

    for term_with_weight in tokenized_query:

        term = term_with_weight.split("^")
        term[0] = tokens_lemmatize([term[0]])[0].upper()

        if (term[0] in inverted_index) and (term[0] not in stop_words):
            freq = int(term[1]) if len(term) == 2 else 1
            counter_query.update({term[0]: freq})

    filtered_query = []

    if counter_query:
        maxi = counter_query.most_common(1)[0][1]

        for term, freq in counter_query.most_common():
            tf = 0.5 + 0.5 * freq / maxi
            idf = log(nbDoc/len(inverted_index[term].keys()))
            weight = tf*idf
            filtered_query.append((term, weight))

    return filtered_query


def tf_idf(term: str, id: str, inverted_index: OrderedDict, stats_collection: OrderedDict) -> float:
    """
    Résumé
    ---
    Cette fonction calcule le tf-dif d'un terme pour un document donné

    Paramètres
    ---
    term: le terme duquel on calcul le tf-idf
    id: ID du document
    inverted_index: index inversé de la collection
    stats_collection: statistiques de la collection (i.e: fréquences min, max, mean pour chaque document)
    """
    tf = inverted_index[term][id][0]
    tf = 0.5 + 0.5 * tf/stats_collection[id]["freq_max"]
    idf = log(stats_collection["nb_docs"]/len(inverted_index[term].keys()))
    return tf*idf


def vector_search(query: str, inverted_index: OrderedDict, stats_collection: OrderedDict) -> OrderedDict:
    """
    Résumé
    ---
    Cette fonction effectue une recherche dans l'index en utilisant un modèle vectoriel

    Paramètres
    ---
    query: la requête à exécuter
    inverted_index: l'index inversé de la collection
    stats_collection: statistiques de la collection (i.e: fréquences min, max, mean pour chaque document)
    """
    relevant_docs = {}
    query_pre_processed = pre_processed_query(
        query, inverted_index, stats_collection["nb_docs"])
    norm_query = 0.
    norm_docs = {}

    for term, term_query_weight in query_pre_processed:
        norm_query += term_query_weight*term_query_weight
        for doc in inverted_index[term]:
            term_doc_weight = tf_idf(
                term, doc, inverted_index, stats_collection)
            if doc in relevant_docs:
                relevant_docs[doc] += term_doc_weight * term_query_weight
                norm_docs[doc] += term_doc_weight*term_doc_weight
            else:
                relevant_docs[doc] = term_doc_weight * term_query_weight
                norm_docs[doc] = term_doc_weight*term_doc_weight

    for doc in relevant_docs:
        relevant_docs[doc] /= (sqrt(norm_docs[doc])*sqrt(norm_query))

    scores = list(relevant_docs.values())

    if scores:
        ordered_relevant_docs = OrderedDict(
            sorted(filter(lambda t: t[1] >= 0.1, relevant_docs.items()), key=lambda t: t[1], reverse=True))
    else:
        ordered_relevant_docs = OrderedDict()

    return ordered_relevant_docs
