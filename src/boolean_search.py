from tt import BooleanExpression
from collections import OrderedDict

# Binary search

def transformation_query_to_boolean(query: str) -> list:
  query = query.upper()
  boolean_query = BooleanExpression(query)

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
  query = transformation_query_to_boolean(query)
  evaluation_stack = []

  print(f"Boolean query on {query}")

  operators = ['AND', 'OR', 'NOT']

  for term in query:
    if term not in operators:
      evaluation_stack.append(inv_index[term])
    else:
      if term == 'NOT':
        operande = evaluation_stack.pop()
        eval_prop = boolean_operator_processing_with_inverted_index(term, evaluation_stack.pop(),operande)
        evaluation_stack.append(eval_prop[0])
        evaluation_stack.append(eval_prop[0])
      else:
        operator = term.upper()
        eval_prop =  boolean_operator_processing_with_inverted_index(operator, evaluation_stack.pop(),evaluation_stack.pop())
        evaluation_stack.append(eval_prop[0])

  return order_results(evaluation_stack.pop())