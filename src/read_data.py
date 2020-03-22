import os

from nltk.tokenize import word_tokenize
from collections import Counter, OrderedDict

def article_word_tokenize(article: str) -> list:
  if type(article)!= str:
    raise Exception("The function takes a string as input data")
  else:
    tokens = word_tokenize(article)
    return tokens


def load_stop_word(filename: str) -> list:
  """ Load stop words to remove useless ones """
  with open(filename, 'r') as f:
    stop_words = []
    line = f.readline()
    while line !='Z\n':
      if line !='\n':
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
  filenames = [dirname + '/' + f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]

  vocabulary = Counter()
  documents = {}

  i = 0
  for fname in filenames:
    with open(fname) as file:
      tokens = article_word_tokenize(file.read())
      tokens = remove_stop_words(tokens, stop_words)

      freq = count_frequency(tokens)

      vocabulary.update(freq)
      documents[fname] = freq

    i += 1
    print("Reading progress for {0}: {1:04.1f}%".format(dirname, 100 * i / len(filenames)), flush=True, end='\r')

  print(f"Reading complete for {dirname}")

  return vocabulary, documents


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

  return vocabulary, documents


def build_inverted_index(collection: dict) -> OrderedDict:
  # On considère ici que la collection est pré-traitée
  inverted_index = OrderedDict()

  i = 0
  for document in collection:
    n=0
    for term in collection[document]:
      n = n+1
      if term in inverted_index.keys():
        if document in inverted_index[term].keys():
          inverted_index[term][document][0] = inverted_index[term][document][0] + 1
          inverted_index[term][document][1].append(n)
        else:
          inverted_index[term][document]= [1,[n]]
      else:
        inverted_index[term]=OrderedDict()
        inverted_index[term][document]=[1,[n]]

    i += 1
    print("Building inverted index {0:04.1f}%".format(100 * i / len(collection)), flush=True, end='\r')
                
  return inverted_index


def save_inverted_index(inverted_index: OrderedDict, filename: str) -> None:
  with open(filename, 'w') as f:
    for term in inverted_index:
      f.write(term + "," + str(len(inverted_index[term])))
      for doc in inverted_index[term]:
        f.write("\t" + doc + "," + str(inverted_index[term][doc][0]) + ";")
        for pos in inverted_index[term][doc][1]:
          f.write(str(pos) + ",")
      f.write("\n")
    f.close()

def convert_list_to_int(liste: list) -> list:
    new_list = []
    for i in liste:
         new_list.append (int(i))
    return new_list

def load_inverted_index(filename: str) -> OrderedDict:
  if not os.path.exists(filename):
    create_index()

  with open(filename, 'r') as f:
    print("Loading inverted index...")
    inverted_index = OrderedDict()
    line = f.readline()
    while line!="":
      line = line.rstrip()
      content = line.split("\t")
      term = content[0].split(",")[0]
      postings = content[1:]
      postings_with_tf_and_pos= OrderedDict()
      for occurence in postings:
        content = occurence.split(";")
        positions = content[1].rstrip(",").split(",")
        positions=convert_list_to_int(positions)
        document = content[0].split(",")
        postings_with_tf_and_pos[document[0]] = [int(document[1]), positions]
      inverted_index[term] = postings_with_tf_and_pos
      line = f.readline()
    print("Loading completed!")
    return inverted_index

def create_index() -> None:
  stop_words = load_stop_word("data/stop_words.txt")

  v, d = read_everything("data", stop_words)

  inverted_index = build_inverted_index(d)

  save_inverted_index(inverted_index, "index/simple.index")

  # TODO: remove
  print(v.most_common(30))
  print(len(d))


if __name__ == '__main__':
  create_index()
