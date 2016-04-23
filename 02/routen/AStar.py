# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""

#breitenqueue.py - V. 150417

import Aimaqueue
from helpimport import *


def main(graph, start_name, end_name):
    if (start_name == end_name):
        print ("Ziel entspricht Start")
        return

    queue = Aimaqueue.SortedQueue()
    visited = []
    start = graph.get_node(start_name)
    queue.put((0, 0, None, start))

    while not queue.empty():
        fcost, gcost, parent, currentnode = queue.get()

        if currentnode.name() in visited:
            graph.ausgabe(currentnode.name(), "", fcost, gcost,
                          "bereitsbesucht")
            continue

        visited.append(currentnode.name())
        currentnode.set_parent(parent)

        if currentnode.name() == end_name:
            graph.ausgabe(currentnode.name(), "", fcost, gcost, "gefunden")
            break

        for edge in currentnode.get_edges():
            nextnode = edge.end()
            kosten = gcost + edge.weight
            fcost = graph.luftlinie(start.name(), nextnode.name())
            graph.ausgabe(currentnode.name(), nextnode.name(), fcost, kosten,
                          "expandieren")
            queue.put((fcost, kosten, currentnode, nextnode))
        graph.ausgabe(currentnode.name(), "", fcost, gcost, "abgearbeitet")
