import os
import json
import threading

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
from nltk.corpus import wordnet

from collections import Counter, OrderedDict


def article_word_tokenize(article: str) -> list:
    if type(article) != str:
        raise Exception("The function takes a string as input data")
    else:
        tokens = word_tokenize(article)
        return tokens


def load_stop_word(filename: str) -> list:
    """ Load stop words to remove useless ones """
    with open(filename, 'r') as f:
        stop_words = []
        line = f.readline()
        while line != 'Z\n':
            if line != '\n':
                stop_words.append(line.rstrip())
            line = f.readline()
        stop_words.append(line.rstrip())
    return stop_words


def remove_stop_words(tokens: list, stop_words: list) -> list:
    """ Remove the useless words from the collection """
    # TODO: refactor
    tokens_filtered = []
    for i in tokens:
        i = i.upper()
        if i not in stop_words:
            tokens_filtered.append(i)
    return tokens_filtered


def count_frequency(tokens: list) -> Counter:
    return Counter(tokens)

def read_data(dirname: str, stop_words: list):
    filenames = [dirname + '/' +
                 f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]

    vocabulary = Counter()
    documents = {}

    i = 0
    for fname in filenames:
        with open(fname) as file:
            tokens = article_word_tokenize(file.read())
            tokens = remove_stop_words(tokens, stop_words)
            tokens = tokens_lemmatize(tokens)

            freq = count_frequency(tokens)

            vocabulary.update(freq)
            documents[fname[len('data/'):]] = freq

        i += 1
        print("Reading progress for {0}: {1:04.1f}%".format(
            dirname, 100 * i / len(filenames)), flush=True, end='\r')

    print(f"Reading complete for {dirname}")

    return vocabulary, documents

def get_wordnet_pos(word: str) -> str:
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

# Lemmatisation
def tokens_lemmatize(tokens: list) -> list:
    lemmatized_tokens = []
    lemmatizer = WordNetLemmatizer() # initialisation d'un lemmatiseur
    for t in tokens:
        lemma = lemmatizer.lemmatize(t, get_wordnet_pos(t))
        lemmatized_tokens.append(lemma)
    return lemmatized_tokens

# Stemming
def collection_stemming(segmented_collection: dict) -> dict:
    stemmed_collection={}
    stemmer = PorterStemmer() # initialisation d'un stemmer
    for k,v in segmented_collection.items():
        stem = stemmer.stem(k)
        if stem not in stemmed_collection:
            stemmed_collection[stem] = 0
        stemmed_collection[stem] += v
    return stemmed_collection

def read_everything(dirname: str, stop_words: list):
    """ Call read_data for all the subdirectories.
    TODO: refactor """
    paths = [os.path.join(dirname, str(n)) for n in range(10)]

    vocabulary = Counter()
    documents = {}

    for p in paths:
        v, d = read_data(p, stop_words)

        vocabulary = vocabulary + v
        documents = {**documents, **d}

    # documents = collection_lemmatize(documents)
    # vocabulary = collection_lemmatize(vocabulary)

    return vocabulary, documents


def get_stats_document(document: Counter) -> OrderedDict:
    stats = OrderedDict()
    try:
        stats["freq_max"] = document.most_common(1)[0][1]
        stats["unique_terms"] = len(document.items())
        tf_moy = sum(document.values())
        stats["freq_moy"] = tf_moy/len(document.items())
    except:
        print(document)
    return stats


def get_stats_collection(collection: dict) -> OrderedDict:
    stats = OrderedDict()
    stats["nb_docs"] = len(collection.keys())
    for doc in collection:
        stats[doc] = get_stats_document(collection[doc])
    return stats


def build_inverted_index(collection: dict) -> OrderedDict:
    # On considère ici que la collection est pré-traitée
    inverted_index = OrderedDict()

    i = 0
    for document in collection:
        n = 0
        for term in collection[document]:
            n = n+1
            if term in inverted_index.keys():
                if document in inverted_index[term].keys():
                    inverted_index[term][document][0] = inverted_index[term][document][0] + 1
                    inverted_index[term][document][1].append(n)
                else:
                    inverted_index[term][document] = [1, [n]]
            else:
                inverted_index[term] = OrderedDict()
                inverted_index[term][document] = [1, [n]]

        i += 1
        print("Building inverted index {0:04.1f}%".format(
            100 * i / len(collection)), flush=True, end='\r')

    return inverted_index


def save_inverted_index(inverted_index: OrderedDict, filename: str) -> None:
    with open(filename, 'w') as f:
        for term in inverted_index:
            f.write(term + "," + str(len(inverted_index[term])))
            for doc in inverted_index[term]:
                f.write("\t" + doc + "," +
                        str(inverted_index[term][doc][0]) + ";")
                for pos in inverted_index[term][doc][1]:
                    f.write(str(pos) + ",")
            f.write("\n")
        f.close()


def convert_list_to_int(liste: list) -> list:
    new_list = []
    for i in liste:
        new_list.append(int(i))
    return new_list


def load_inverted_index(filename: str) -> OrderedDict:
    if not os.path.exists(filename):
        create_index()

    with open(filename, 'r') as f:
        print("Loading inverted index...")
        inverted_index = OrderedDict()
        line = f.readline()
        while line != "":
            line = line.rstrip()
            content = line.split("\t")
            term = content[0].split(",")[0]
            postings = content[1:]
            postings_with_tf_and_pos = OrderedDict()
            for occurence in postings:
                content = occurence.split(";")
                positions = content[1].rstrip(",").split(",")
                positions = convert_list_to_int(positions)
                document = content[0].split(",")
                postings_with_tf_and_pos[document[0]] = [
                    int(document[1]), positions]
            inverted_index[term] = postings_with_tf_and_pos
            line = f.readline()
        print("Loading completed!")
        return inverted_index


def load_stats_collection(filename: str) -> OrderedDict:
    stats_collection = OrderedDict()
    with open(filename, 'r') as f:
        stats_collection = json.loads(f.read())

    return stats_collection


def create_index() -> None:
    stop_words = load_stop_word("data/stop_words.txt")

    v, d = read_everything("data", stop_words)

    print(v)

    inverted_index = build_inverted_index(d)
    save_inverted_index(inverted_index, "index/simple.index")

    stats_collection = get_stats_collection(d)
    with open("index/stats_collection.json", "w") as f:
        f.write(json.dumps(stats_collection))


if __name__ == '__main__':
    create_index()
