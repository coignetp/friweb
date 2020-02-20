from os import listdir
from os.path import isfile, join

from nltk.tokenize import word_tokenize
import collections

def article_word_tokenize(article: str):
    if type(article)!= str:
        raise Exception("The function takes a string as input data")
    else:
        tokens = word_tokenize(article)
        return tokens


def count_frequency(tokens: list):
  return collections.Counter(tokens)


def read_data(dirname: str):
  filenames = [dirname + '/' + f for f in listdir(dirname) if isfile(join(dirname, f))]

  vocabulary = collections.Counter()
  documents = {}

  for fname in filenames:
    with open(fname) as file:
      tokens = article_word_tokenize(file.read())
      # TODO: Remove stop words and filter

      freq = count_frequency(tokens)

      vocabulary.update(freq)
      documents[fname] = freq

  return vocabulary, documents

if __name__ == '__main__':
  v, d = read_data("data/pa1-data/1")

  print(v.most_common(30))
  print(len(d))