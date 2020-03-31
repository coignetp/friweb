import os
import json
import threading

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import pos_tag
from nltk.corpus import wordnet

from collections import Counter, OrderedDict


def article_word_tokenize(article: str) -> list:
    """
    Résumé
    ---
    tokenize la string donnée en entrée

    Paramètres
    ---
    article: String à tokenizer"""
    if type(article) != str:
        raise Exception("The function takes a string as input data")
    else:
        tokens = word_tokenize(article)
        return tokens


def load_stop_word(filename: str) -> list:
    """
    Résumé
    ---
    Charge le fichier de stop words

    Paramètres
    ---
    Lien vers le fichier de stop words
    """

    with open(filename, 'r') as f:
        stop_words = []
        line = f.readline()
        while line != 'Z\n' and line:
            if line != '\n':
                stop_words.append(line.rstrip())
            line = f.readline()
        stop_words.append(line.rstrip())
    return stop_words


def remove_stop_words(tokens: list, stop_words: list) -> list:
    """
    Résumé
    ---
    Enlève les stop words de la liste de tokens en entrée

    Paramètres
    ---
    tokens: liste de tokens
    stop_words: liste de stop words a enlever de tokens
    """
    tokens_filtered = []
    for i in tokens:
        i = i.upper()
        if i not in stop_words:
            tokens_filtered.append(i)
    return tokens_filtered


def count_frequency(tokens: list) -> Counter:
    """
    Résumé
    ---
    Renvoie un counter du nombre d'occurence de chaque terme dans la liste tokens

    Paramètres
    ---
    tokens: liste de tokens à compter
    """
    return Counter(tokens)


def read_data(dirname: str, stop_words: list):
    """
    Résumé
    ---
    Lit l'ensemble des fichiers dans le dossier dirname et renvoie le vocabulaire et un dictionaire
    qui à chaque document associe un counter avec la fréquence de chacun des termes du document.

    Paramètres
    ---
    dirname: nom du dossier à examiner
    stop_words: liste des stop words
    """
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
    """
    Résumé
    ---
    Déduit la fonction d'un mot dans un texte

    Paramètres
    ---
    word: mot dont on veut connaitre la fonction
    """
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)

# Lemmatisation


def tokens_lemmatize(tokens: list) -> list:
    """
    Résumé
    ---
    Lemmatize une liste de tokens

    Paramètres
    ---
    tokens: liste de tokens à lemmatizer
    """
    lemmatized_tokens = []
    lemmatizer = WordNetLemmatizer()  # initialisation d'un lemmatiseur
    for t in tokens:
        lemma = lemmatizer.lemmatize(t, get_wordnet_pos(t))
        lemmatized_tokens.append(lemma)
    return lemmatized_tokens


def read_everything(dirname: str, stop_words: list):
    """
    Résumé
    ---
    Lit l'ensemble des documents de la collection et aggrège les résultats

    Paramètres
    ---
    dirname: prefix du dossier contenant la collection
    stop_words: liste des stop words
    """
    paths = [os.path.join(dirname, str(n)) for n in range(10)]

    vocabulary = Counter()
    documents = {}

    for p in paths:
        v, d = read_data(p, stop_words)

        vocabulary = vocabulary + v
        documents = {**documents, **d}

    return vocabulary, documents


def get_stats_document(document: Counter) -> OrderedDict:
    """
    Résumé
    ---
    Pour un document donné calcule des statistiques liées à ce document comme le nombre unique de terme, la fréquence maximum
    d'un terme dans le document ou la fréquence moyenne.

    Paramètres
    ---
    document: counter représentant le document
    """
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
    """
    Résumé
    ---
    Pour chaque document de la collection, calcule des statistiques liées à ce document comme le nombre unique de terme, la fréquence maximum
    d'un terme dans le document ou la fréquence moyenne.

    Paramètres
    ---
    collection: dictionnaire de la collection
    """
    stats = OrderedDict()
    stats["nb_docs"] = len(collection.keys())
    for doc in collection:
        stats[doc] = get_stats_document(collection[doc])
    return stats


def build_inverted_index(collection: dict) -> OrderedDict:
    """
    Résumé
    ---
    Construit l'index inversé de la collection

    Paramètres
    ---
    collection: dictionnaire de la collection"""
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
    """
    Résumé
    ---
    Sauvegarde l'index inversé de la collection pour une utilisation ultérieure

    Paramètres
    ---
    inverted_index: l'index inversé de la collection
    filename: nom du fichier dans lequel on veut enregister l'index inversé
    """
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
    """
    Résumé
    ---
    Transforme chaque terme d'une liste en entier

    Paramètres
    ---
    liste: liste à convertir
    """
    new_list = []
    for i in liste:
        new_list.append(int(i))
    return new_list


def load_inverted_index(filename: str) -> OrderedDict:
    """
    Résumé
    ---
    Lit l'index inversé de la collection depuis un fichier

    Paramètres
    ---
    filename: nom du fichier duquel on veut lire l'index inversé
    """
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
    """
    Résumé
    ---
    Lit les statistiques de la collection depuis un fichier

    Paramètres
    ---
    filename: nom du fichier duquel on veut lire les statistiques
    """
    stats_collection = OrderedDict()
    with open(filename, 'r') as f:
        stats_collection = json.loads(f.read())

    return stats_collection


def create_index() -> None:
    """
    Résumé
    ---
    Procédure complète de la création d'un index inversé
    """
    stop_words = load_stop_word("data/stop_words.txt")

    _, d = read_everything("data", stop_words)

    inverted_index = build_inverted_index(d)
    save_inverted_index(inverted_index, "index/simple.index")

    stats_collection = get_stats_collection(d)
    with open("index/stats_collection.json", "w") as f:
        f.write(json.dumps(stats_collection))


if __name__ == '__main__':
    create_index()
