from math import log, sqrt
from collections import Counter, OrderedDict
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

from read_data import article_word_tokenize, remove_stop_words, load_stop_word


def pre_processed_query(query: str, inverted_index: OrderedDict) -> list:
    stop_words = load_stop_word("data/stop_words.txt")

    counter_query = Counter()
    tokenized_query = article_word_tokenize(query)
    norm = 0.
    for term in tokenized_query:
        weighted_term = term.split("^")
        if (weighted_term[0].upper() in inverted_index) and (weighted_term[0] not in stop_words):
            if(len(weighted_term) == 2):
                counter_query.update(
                    {weighted_term[0].upper(): int(weighted_term[1])})
                norm += int(weighted_term[1])
            else:
                counter_query.update({weighted_term[0].upper(): 1})
                norm += 1

    filtered_query = []
    for term, weight in counter_query.most_common():
        filtered_query.append((term, weight/norm))

    return filtered_query


def tf_idf_log(term: str, id: str, inverted_index: OrderedDict, stats_collection: OrderedDict) -> float:
    tf = inverted_index[term][id][0]
    tf_log = 0.5 + 0.5 * tf/stats_collection[id]["freq_max"]
    idf = log(stats_collection["nb_docs"]/len(inverted_index[term].keys()))
    return tf_log*idf


def vectorial_search(query: str, inverted_index: OrderedDict, stats_collection: OrderedDict) -> OrderedDict:
    relevant_docs = {}
    query_pre_processed = pre_processed_query(query, inverted_index)
    norm_query = 0.
    norm_docs = 0.

    for term, term_query_weight in query_pre_processed:
        norm_query += term_query_weight*term_query_weight
        for doc in inverted_index[term]:
            term_doc_weight = tf_idf_log(
                term, doc, inverted_index, stats_collection)
            norm_docs += term_doc_weight*term_doc_weight
            if doc in relevant_docs:
                relevant_docs[doc] += term_doc_weight * term_query_weight
            else:
                relevant_docs[doc] = term_doc_weight * term_query_weight

    for doc in relevant_docs:
        relevant_docs[doc] /= (sqrt(norm_docs)*sqrt(norm_query))

    ordered_relevant_docs = OrderedDict(
        sorted(relevant_docs.items(), key=lambda t: t[1], reverse=True))

    return ordered_relevant_docs
