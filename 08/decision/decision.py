# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""
from helpimport import *
import math
from copy import deepcopy
from functools import reduce

classification = ""
unterscheidung = 0

def main(graph, listexamples, listattributes, default):
    graph = decision_tree_learning(listexamples, listattributes, default)
    return graph


def decision_tree_learning(examples, attributes, default):  # default: string
    global classification
    global unterscheidung

    # Es gibt gar keine Bsp: Default wird als einziger Knoten im Graphen erzeugt.
    if len(examples) == 0:
        graph = DecisionTree()
        graph.add_node(default, True)
        return graph

    # Alle Bsp enden gleich: Ausgabe wird als einziger Knoten im Graphen erzeugt.
    elif all_the_same(examples):
        graph = DecisionTree()
        # hier werden Ja und Nein iwann hinzugefuegt
        graph.add_node(classification, True)
        return graph

    # Alle attribute aufgebraucht: Rauschen! Mehrheit der Ausgaben der
    # Bsp wird als Knoten erzeugt.
    elif attributes_empty(attributes):
        graph = DecisionTree()
        graph.add_node(majority_value(examples), True)
        return graph

    # Alles "normal"
    else:
        graph = DecisionTree()
        best = choose_attribute(examples, attributes)
        name = best[1] + str(unterscheidung)  # unterscheidung, da im einfaches
                                              # fall die attribute auch mehrfach
                                              # getestet werden können, von
                                              # unterschiedlichen Stellen aus!
        graph.add_node(name, True)  # True: ist Wurzel
        unterscheidung +=1
        attributesnew = deepcopy(attributes)
        attributesnew.pop(best[3])
        for vi in best[2]:  # auswahlmoeglichkeiten
            examplesi = []
            # spalte mit attribut loeschen&example zu neuen examples hinzufuegen.
            for el in range(len(examples)):
                if examples[el][best[3]] == vi:
                    examplesi.append(deepcopy(examples[el]))
            for e in range(len(examplesi)):
                examplesi[e].pop(best[3])
            subtree = decision_tree_learning(examplesi, attributesnew, majority_value(examples))
            # alle knoten aus subtree auch zu graph hinzufuegen:
            for node in subtree.get_nodes():
                graph.add_node(node.name(), False)
            # alle kanten aus subtree hinzufuegen:
            for node in subtree.get_nodes():
                for edge in node.get_edges():
                    graph.add_edge(node.name(), edge.end().name(), edge.title())
            graph.add_edge(name, subtree.get_root().name(), vi)
        return graph

def all_the_same(examples):
    global classification
    global unterscheidung
    # Bsp in positive und neg. bsp aufteilen:
    posex = []
    negex = []
    for bsp in examples:

        if bsp[-1] == "No":
            negex.append(bsp)
        else:
            posex.append(bsp)
    # es gibt nur pos oder neg bsp:
    if len(posex) == 0 or len(negex) == 0:
        if len(posex) == 0:
            classification = "No"+str(unterscheidung)
        else:
            classification = "Yes"+str(unterscheidung)
        unterscheidung +=1
        return True
    else:
        return False

def attributes_empty(attributes):
    if len(attributes) == 0:
        return True
    else:
        return False

def majority_value(examples):
    # bsp aufteilen, um zu schauen, was noch öfter übrig bleibt
    posex = []
    negex = []
    for bsp in examples:
        if bsp[-1] == "No":
            negex.append(bsp)
        else:
            posex.append(bsp)
    if len(posex) < len(negex):
        ausgabe = "No"
    else:
        ausgabe = "Yes"
    return ausgabe  # =string


def I(examples):
    def count(predicate, seq):
        f = lambda count, x: count + (not not predicate(x))
        return reduce(f, seq, 0)
    return information_content([count(lambda x: (x[-1] == v), examples)
                            for v in examples])

def choose_attribute(examples, attributes):

    index = 0
    max_gain = 0
    for ind, attr in enumerate(attributes):

        N = float(len(examples))
        remainder = 0
        splitted = [(v, [e for e in examples if e[-1] == v[-1]])
                    for v in examples]

        for (v, examples_i) in splitted:
            remainder += (len(examples_i) / N) * I(examples_i)

        gain = I(examples) - remainder

        if gain > max_gain:
            max_gain = gain
            index = ind

    at = 0
    poss = []
    attr = []
    for e in examples:
        if not e[at] in poss:
            poss.append(e[at])  # poss[index][0] = "name" des attributs
    attr.append(max_gain)  # spaeter fuer gain!
    attr.append(attributes[index])
    attr.append(poss)
    attr.append(at)
    return(attr)


def information_content(values):
    "Number of bits to represent the probability distribution in values."
    values = [x for x in values if x != 0]
    s = float(sum(values))
    if s != 1.0: values = [v/s for v in values]
    return sum([- v * log2(v) for v in values])
