# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""
#minimax.py V. 150423

from helpimport import *
import matchesrules

graph = ""


def main(zustand):
    global graph
    # zustand wird als wurzel erstellt:
    graph = GameGraph("Match")
    graph.add_node(zustand, "max", None, None)
    # knotenname, knotentyp, elternknoten, bewertung
    infinity =  float("-Infinity")
    v = max_value(zustand, -infinity, infinity)
    zustand = graph.get_node(zustand)
    for edge in zustand.get_edges():
        if edge.end().get_value() == v:
            nachfolger = edge.end().name()
            break
    return nachfolger


def max_value(z, alpha, beta):  # returns value
    z = graph.get_node(z)
    if terminal_test(z.name()):
        return z.get_value()
    else:
        v = float("-Infinity")
        # alle nachfolgenden moeglichkeiten als knoten anhaengen!
        # 0 ziehen, wenn nicht davor oder davor 0 gezogen wurden;
        # 1 ziehen(immer erlaubt, nur hier kann gewonnen werden!);
        # 2 ziehen, wenn mehr als 2 da sind;
        zlist = list(z.name())
        if matchesrules.take_0_poss(z.name()):
            neu = z.name() + "0"
            graph.add_node(neu, "min", z.name(), None)
            graph.add_edge(z.name(), neu, 0)
        if matchesrules.take_2_poss(z.name()):
            neu = str(int(zlist[0])-2)
            for i in range(1, len(zlist), 1):
                neu = neu + zlist[i]
            neu = neu+"2"
            graph.add_node(neu, "min", z.name(), None)
            graph.add_edge(z.name(), neu, 0)
        if matchesrules.take_1_poss(z.name()):
            neu = str(int(zlist[0])-1)
            for i in range(1, len(zlist), 1):
                neu = neu + zlist[i]
            neu = neu+"1"
            if neu[0] == "0":
                # dies ist ein terminalknoten, da max den letzten schritt geht,
                # ist die bewertung = 1
                graph.add_node(neu, "ter", z.name(), 1)
                graph.add_edge(z.name(), neu, 0)
            else:  # kein terminalknoten, wird als min knoten hinzugefuegt.
                graph.add_node(neu, "min", z.name(), None)
                graph.add_edge(z.name(), neu, 0)

        for edge in z.get_edges():
            v = max(v, min_value(edge.end().name(), alpha, beta))
            alpha = max(alpha, v)
            if alpha >= beta:
                z.set_value(v)
                return v
        z.set_value(v)
        return v


def min_value(z, alpha, beta):
    z = graph.get_node(z)
    if terminal_test(z.name()):
        return z.get_value()
    else:
        v = float("Infinity")
        # alle nachfolgenden moeglichkeiten als knoten anhaengen!
        # 0 ziehen, wenn nicht davor oder davor 0 gezogen wurden;
        # 1 ziehen(immer erlaubt, nur hier kann gewonnen werden!);
        # 2 ziehen, wenn mehr als 2 da sind;
        zlist = list(z.name())

        if matchesrules.take_0_poss(z.name()):
            neu = z.name() + "0"
            graph.add_node(neu, "max", z.name(), None)
            graph.add_edge(z.name(), neu, 0)
        # if int(n[0]) >2:
        if matchesrules.take_2_poss(z.name()):
            neu = str(int(zlist[0])-2)
            for i in range(1, len(zlist), 1):
                neu = neu + zlist[i]
            neu = neu+"2"
            graph.add_node(neu, "max", z.name(), None)
            graph.add_edge(z.name(), neu, 0)

        if matchesrules.take_1_poss(z.name()):
            neu = str(int(zlist[0])-1)
            for i in range(1, len(zlist), 1):
                neu = neu + zlist[i]
            neu = neu+"1"
            if neu[0] == "0":
                # dies ist ein terminalknoten; da min den letzten schritt geht,
                # ist die bewertung = -1
                graph.add_node(neu, "ter", z.name(), -1)
                graph.add_edge(z.name(), neu, 0)
            else:  # kein terminalknoten, wird als max knoten hinzugefuegt.
                graph.add_node(neu, "max", z.name(), None)
                graph.add_edge(z.name(), neu, 0)

        for edge in z.get_edges():
            v = min(v, max_value(edge.end().name(), alpha, beta))
            beta = min(beta, v)
            if alpha >= beta:
                z.set_value(v)
                return v
        z.set_value(v)
        return v


def terminal_test(zustand):  # returns ture oder false
    # nicht terminal, wenn noch mind ein streichholz da ist
    if zustand[0] == "0":
        return True
    else:
        return False
