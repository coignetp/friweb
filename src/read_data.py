from os import listdir
from os.path import isfile, join

from nltk.tokenize import word_tokenize
import collections

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


def count_frequency(tokens: list) -> collections.Counter:
  return collections.Counter(tokens)


def read_data(dirname: str, stop_words: list):
  filenames = [dirname + '/' + f for f in listdir(dirname) if isfile(join(dirname, f))]

  vocabulary = collections.Counter()
  documents = {}

  for fname in filenames:
    with open(fname) as file:
      tokens = article_word_tokenize(file.read())
      tokens = remove_stop_words(tokens, stop_words)

      freq = count_frequency(tokens)

      vocabulary.update(freq)
      documents[fname] = freq

  return vocabulary, documents

if __name__ == '__main__':
  stop_words = load_stop_word("data/stop_words.txt")

  v, d = read_data("data/pa1-data/1", stop_words)

  print(v.most_common(30))
  print(len(d))