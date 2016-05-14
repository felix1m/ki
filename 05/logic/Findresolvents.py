# -*- coding: utf-8 -*-

def is_neg(a):
  return a[0]=="-"

def negate(a):
  if is_neg(a):
    return a[1:]
  else:
    return "-"+a

def resolvents(clauseA,clauseB):
    newclauses = []

    clauseA = set(clauseA)
    clauseB = set(clauseB)

    for s in clauseA:
      negation = negate(s)
      if negation in clauseB:
          newclauses.append(list(clauseA.union(clauseB).difference({s, negation})))

    return newclauses
