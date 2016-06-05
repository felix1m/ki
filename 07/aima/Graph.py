# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""

from Node import *
import time
import zeichne


# abtrakte klasse:
class Graph:
    def __init__(self, name, anzeigefenster, printfenster, gui):
        self.nodes = {}
        self.name = name
        self.anzeigefenster = anzeigefenster
        self.printfenster = printfenster
        self.gui = gui

    def get_name(self):
        return self.name

    def get_node(self, name):
        return self.nodes[name]

    def get_nodes(self):
        return self.nodes.values()


class UnDirGraph(Graph):
    def __init__(self, name, anzeigefenster, printfenster, gui):
        Graph.__init__(self, name, anzeigefenster, printfenster, gui)

    def get_name(self):
        return Graph.get_name(self)

    def add_weighted_edge(self, start_name, end_name, cost):
        self.nodes[start_name].add_edge(self.nodes[end_name], cost)
        self.nodes[end_name].add_edge(self.nodes[start_name], cost)

    def get_node(self, name):
        return Graph.get_node(self, name)

    def get_nodes(self):
        return Graph.get_nodes(self)

    def remove_edge(self, start_name, end_name):
        self.nodes[start_name].remove_edge(self.nodes[end_name])
        self.nodes[end_name].remove_edge(self.nodes[start_name])


class DirGraph(Graph):
    def __init__(self, name, anzeigefenster, printfenster, gui):
        Graph.__init__(self, name, anzeigefenster, printfenster, gui)

    def get_name(self):
        return Graph.name(self)

    def get_node(self, name):
        return Graph.get_node(self, name)

    def get_nodes(self):
        return Graph.get_nodes(self)

    def add_weighted_edge(self, start_name, end_name, cost):
        self.nodes[start_name].add_edge(self.nodes[end_name], cost)

    def add_titled_egde(self, start_name, end_name, title):
        self.nodes[start_name].add_edge(self.nodes[end_name], title)

    def add_edge(self, start_name, end_name):
        self.nodes[start_name].add_edge(self.nodes[end_name])

    def remove_edge(self, start_name, end_name):
        self.nodes[start_name].remove_edge(self.nodes[end_name])


class MapGraph(UnDirGraph):

    def __init__(self, name, anzeigefenster, printfenster, gui):
        UnDirGraph.__init__(self, name, anzeigefenster, printfenster, gui)

    def get_name(self):
        return UnDirGraph.get_name(self)

    def add_node(self, name, xcoordinate, ycoordinate):
        self.nodes[name] = Mapnode(name, xcoordinate, ycoordinate)

    def add_edge(self, start_name, end_name, cost):
        UnDirGraph.add_weighted_edge(self, start_name, end_name, cost)

    def get_node(self, name):
        return UnDirGraph.get_node(self, name)

    def get_nodes(self):
        return UnDirGraph.get_nodes(self)

    def remove_edge(self, start_name, end_name):
        UnDirGraph.remove_edge(self, start_name, end_name)

    def luftlinie(self, starta, ziela):
        start = self.get_node(starta)
        ziel = self.get_node(ziela)
        sx = start.get_x_coordinate()
        sy = start.get_y_coordinate()
        zx = ziel.get_x_coordinate()
        zy = ziel.get_y_coordinate()
        luftlinie = ((sx-zx)**2 + (sy-zy)**2)**0.5
        return(luftlinie)

    def ausgabe(self, aktuell, nach, fkosten, gkosten, was):
        if was == "bereitsbesucht":
            zeichne.schreibe_text(self.printfenster,
                                  "{0} bereits besucht, wird übersprungen!".format(aktuell))
        elif was == "gefunden":
            time.sleep(1)
            zeichne.schreibe_text(self.printfenster,
                                  "{0} mit Kosten {1} gefunden!".format(
                                                                  aktuell,
                                                                  int(gkosten)
                                                                  ))
            zeichne.schreibe_text(self.printfenster,
                                  "----------------------------------------")
            # Weg zeichnen:
            node = aktuell
            node = self.get_node(node)
            while node.get_parent() is not None:
                parent = node.get_parent()
                zeichne.zeichne_linie(parent.get_x_draw(),
                                      parent.get_y_draw(),node.get_x_draw(),
                                      node.get_y_draw(), "blue")
                node = parent
            self.gui.update()
        elif was == "expandieren":
            time.sleep(1)
            if fkosten == 0:
                zeichne.schreibe_text(self.printfenster,
                "{0} nach {1} wird mit Kosten {2} besucht".format(aktuell,
                                                                  nach,
                                                                  int(gkosten
                                                                  )))
            else:
                zeichne.schreibe_text(
                self.printfenster,
                "{0} nach {1} wird mit g-Kosten {2} und f-Kosten {3} hinzugefuegt.".format(
                    aktuell, nach, int(gkosten), int(fkosten)))
            zeichne.zeichne_oval(self.nodes[aktuell].get_x_draw()-3,
                                 self.nodes[aktuell].get_y_draw()-3,
                                 self.nodes[aktuell].get_x_draw()+3,
                                 self.nodes[aktuell].get_y_draw()+3, "pink")
            node = aktuell
            node = self.get_node(node)
            while node.get_parent() is not None:
                parent = node.get_parent()
                zeichne.zeichne_linie(parent.get_x_draw(), parent.get_y_draw(),
                                      node.get_x_draw(), node.get_y_draw(),
                                      "blue")
                node = parent
            zeichne.zeichne_linie(self.nodes[aktuell].get_x_draw(),
                                  self.nodes[aktuell].get_y_draw(),
                                  self.nodes[nach].get_x_draw(),
                                  self.nodes[nach].get_y_draw(), "blue")
            self.gui.update()
            # fuer naechsten Schritt alle Kanten uebermalen:
            for node in self.get_nodes():
                for edge in node.get_edges():
                    xcoord_a = node.get_x_draw()
                    ycoord_a = node.get_y_draw()
                    xcoord_e = edge.end().get_x_draw()
                    ycoord_e = edge.end().get_y_draw()
                    zeichne.zeichne_linie(xcoord_a, ycoord_a, xcoord_e,
                                          ycoord_e, "black")
            # fuer naechsten Schritt
            zeichne.zeichne_oval(self.nodes[aktuell].get_x_draw()-3,
                                 self.nodes[aktuell].get_y_draw()-3,
                                 self.nodes[aktuell].get_x_draw()+3,
                                 self.nodes[aktuell].get_y_draw()+3, "black")
        elif was == "abgearbeitet":
            zeichne.schreibe_text(self.printfenster,
                                  "{0} vollständig abgearbeitet".format(
                                      aktuell))

class GameGraph(DirGraph):
    def __init__(self, name):
        self.nodes = {}
        self.name = name

    def get_name(self):
        return DirGraph.name(self)

    def add_node(self, name, type, parentNode, value):
        self.nodes[name] = MiniMaxNode(name, type, parentNode, value)

    def add_edge(self, start_name, end_name, cost):
        DirGraph.add_weighted_edge(self, start_name, end_name, cost)

    def get_node(self, name):
        return DirGraph.get_node(self, name)

    def get_nodes(self):
        return DirGraph.get_nodes(self)


class DecisionTree(DirGraph):
    def __init__(self):
        self.nodes = {}
        self.root = None

    def add_node(self, name, root):
        self.nodes[name] = DecisionNode(name)
        if root:
            self.root = self.nodes[name]

    def add_edge(self, start_name, end_name, title):
        DirGraph.add_titled_egde(self, start_name, end_name, title)

    def get_node(self, name):
        return self.nodes[name]

    def get_nodes(self):
        return self.nodes.values()

    def get_root(self):
        return self.root


class FFNetwork(DirGraph):
    def __init__(self, name, anzeigefenster, printfenster, gui):
        DirGraph.__init__(self, name, anzeigefenster, printfenster, gui)

    def add_node(self, name, type):
        self.nodes[name] = FFNode(name, type)

    def add_edge(self, start_name, end_name, weight):
        DirGraph.add_weighted_edge(self, start_name, end_name, weight)

    def get_node(self, name):
        return DirGraph.get_node(self, name)

    def get_nodes(self):
        return DirGraph.get_nodes(self)


class BayesGraph(DirGraph):
    def __init__(self, name, anzeigefenster, printfenster, gui):
        DirGraph.__init__(self, name, anzeigefenster, printfenster, gui)

    def add_node(self, name, problist, ebene):
        self.nodes[name] = BayesNode(name, problist, ebene)

    def add_edge(self, start_name, end_name):
        DirGraph.add_edge(self, start_name, end_name)

    def get_node(self, name):
        return DirGraph.get_node(self, name)

    def get_nodes(self):
        return DirGraph.get_nodes(self)
