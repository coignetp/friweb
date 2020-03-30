from tt import BooleanExpression
from collections import OrderedDict

from copy import deepcopy

from read_data import article_word_tokenize, remove_stop_words, load_stop_word, tokens_lemmatize

# Binary search

def transformation_query_to_boolean(query: str) -> list:
  splitted_query = tokens_lemmatize(article_word_tokenize(query))
  for operator in ['AND', 'OR', 'NOT']:
    if operator in splitted_query:
      boolean_query = BooleanExpression(query)
      return boolean_query.postfix_tokens

  # If there is no operator in the query, we use AND between every word
  boolean_query = BooleanExpression(' AND '.join(splitted_query))

  return boolean_query.postfix_tokens

# Handle the different operators

## AND
def merge_and_postings_list(posting_term1: OrderedDict, posting_term2: OrderedDict) -> OrderedDict:
  result = OrderedDict()
  
  for key in posting_term1.keys():
    if key in posting_term2:
      result[key] = posting_term1[key]
      result[key][0] = result[key][0] + posting_term2[key][0]
      result[key][1] += posting_term2[key][1]

  return result

## OR

def merge_or_postings_list(posting_term1: OrderedDict, posting_term2: OrderedDict) -> OrderedDict:
  result = OrderedDict()

  for key in posting_term1.keys():
    result[key] = posting_term1[key]
    if key in posting_term2:
      result[key][0] = result[key][0] + posting_term2[key][0]
      result[key][1] += posting_term2[key][1]

  for key in posting_term2.keys():
    if key not in result:
      result[key] = posting_term2[key]

  return result


# AND NOT

def merge_and_not_postings_list(posting_term1: OrderedDict, posting_term2: OrderedDict) -> OrderedDict:
  result = OrderedDict()
  
  for key in posting_term1.keys():
    if key not in posting_term2:
      result[key] = posting_term1[key]
  
  for key in posting_term2.keys():
    if key not in posting_term1:
      result[key] = posting_term2[key]

  return result

def boolean_operator_processing_with_inverted_index(operator: str, posting_term1: OrderedDict, posting_term2: OrderedDict) -> list:
  result=[]
  if operator == "AND":
    result.append(merge_and_postings_list(posting_term1,posting_term2))
  elif operator=="OR" :
    result.append(merge_or_postings_list(posting_term1,posting_term2))
  elif operator == "NOT":
    result.append(merge_and_not_postings_list(posting_term1,posting_term2))
  return result


def order_results(evaluation: OrderedDict) -> list:
  results = list(evaluation.keys())

  # TODO
  results.sort()
  
  return results 


def boolean_search(query: str, inv_index: OrderedDict) -> list:
  query = query.upper()
  query = transformation_query_to_boolean(query)
  evaluation_stack = []

  operators = ['AND', 'OR', 'NOT']

  for term in query:
    if term not in operators:
      try:
        evaluation_stack.append(inv_index[term.upper()])
      except:
        evaluation_stack.append(None)
    else:
      if term == 'NOT':
        operande = evaluation_stack.pop()
        posting_term = evaluation_stack.pop()

        if posting_term is not None:
          eval_prop = boolean_operator_processing_with_inverted_index(term, posting_term,operande)
          evaluation_stack.append(eval_prop[0])
          evaluation_stack.append(eval_prop[0])
      else:
        operator = term.upper()
        posting_term1 = evaluation_stack.pop()
        posting_term2 = evaluation_stack.pop()

        if posting_term1 is None and posting_term2 is not None:
          posting_term1 = deepcopy(posting_term2)
        elif posting_term1 is not None and posting_term2 is None:
          posting_term2 = deepcopy(posting_term1)

        if posting_term1 is not None:
          eval_prop =  boolean_operator_processing_with_inverted_index(operator, posting_term1, posting_term2)
          evaluation_stack.append(eval_prop[0])

  if len(evaluation_stack) == 0 or evaluation_stack[-1] is None:
    print("WARN: Boolean response is empty")
    return []

  return order_results(evaluation_stack.pop())