# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""

class Edge:
    def __init__(self, end):
        self.__end = end

    def end(self):
        return self.__end


class NameEdge(Edge):
    def __init__(self, end, name):
        Edge.__init__(self, end)
        self.name = name

    def title(self):
        return self.name

    def end(self):
        return Edge.end(self)


class WeightedEdge(Edge):
    def __init__(self, end, weight):
        Edge.__init__(self, end)
        self.weight = weight

    def cost(self):
        return self.weight

    def end(self):
        return Edge.end(self)

    def set_weight(self, newweight):
        self.weight = newweight


class Node:
    def __init__(self, name):
        self.__name = name
        self.edges = {}
        self.__xcoord_draw = 0
        self.__ycoord_draw = 0

    def name(self):
        return self.__name

    def get_edges(self):
        return self.edges.values()

    def __str__(self):
        return self.__name

    def set_xy_draw(self, xcoord, ycoord):
        self.__xcoord_draw = xcoord
        self.__ycoord_draw = ycoord

    def get_x_draw(self):
        return self.__xcoord_draw

    def get_y_draw(self):
        return self.__ycoord_draw

    def add_edge(self, end):
        edge = Edge(end)
        self.edges[end.name()] = edge

    def add_weighted_edge(self, end, weight):
        edge = WeightedEdge(end, weight)
        self.edges[end.name()] = edge

    def add_titled_edge(self, end, title):
        edge = NameEdge(end, title)
        self.edges[end.name()] = edge

    def remove_edge(self, end):
        self.edge = [e for e in self.edges if self.edge.end() != end]


class Mapnode(Node):
    def __init__(self, name, xcoordinate, ycoordinate):
        Node.__init__(self, name)
        self.__xcoordinate = xcoordinate
        self.__ycoordinate = ycoordinate
        self.__parent = None

    def name(self):
        return Node.name(self)

    def get_edges(self):
        return Node.get_edges(self)

    def add_edge(self, end, weight):
        Node.add_weighted_edge(self, end, weight)

    def remove_edge(self, end):
        Node.remove_edge(self, end)

    def __str__(self):
        return Node.__str__(self)

    def get_x_coordinate(self):
        return self.__xcoordinate

    def get_y_coordinate(self):
        return self.__ycoordinate

    def set_xy_draw(self, xcoord, ycoord):
        Node.set_xy_draw(self, xcoord, ycoord)

    def get_x_draw(self):
        return Node.get_x_draw(self)

    def get_y_draw(self):
        return Node.get_y_draw(self)

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent


class MiniMaxNode(Node):
    def __init__(self, name, nodetype, parentNode, value):
        Node.__init__(self, name)
        self.__type = nodetype
        self.__parent = parentNode
        self.__value = value

    def name(self):
        return Node.name(self)

    def get_type(self):
        return self.__type

    def get_edges(self):
        return Node.get_edges(self)

    def __str__(self):
        return Node.__str__(self)

    def get_parent(self):
        return self.__parent

    def set_value(self, value):
        self.__value = value

    def get_value(self):
        return self.__value

    def add_edge(self, end, weight):
        Node.add_weighted_edge(self, end, weight)

    def remove_edge(self, end):
        Node.remove_edge(self, end)


class DecisionNode(Node):
    def __init__(self, name):
        Node.__init__(self, name)
        self.__parent = None
        self.__mostleft_child = None
        self.__left_sibling = None
        self.__right_sibling = None
        self.__xcoordinate = 200
        self.__ycoordinate = 20
        self.xcoord = 0
        self.ycoord = 0
        self.__prelim = 0
        self.__modifier = 0
        self.__left_neighbor = None

    def name(self):
        return Node.name(self)

    def add_edge(self, end, title):
        Node.add_titled_edge(self, end, title)

    def remove_edge(self, end):
        Node.remove_edge(self, end)

    def get_edges(self):
        return Node.get_edges(self)

    def __str__(self):
        return Node.__str__(self)

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return self.__parent

    def set_left_neighbor(self, neighbor):
        self.__left_neighbor = neighbor

    def get_left_neighbor(self):
        return self.__left_neighbor

    def set_prelim(self, prelim):
        self.__prelim = prelim

    def get_prelim(self):
        return self.__prelim

    def set_modifier(self, modifier):
        self.__modifier = modifier

    def get_modifier(self):
        return self.__modifier

    def get_x_coordinate(self):
        return self.__xcoordinate

    def get_y_coordinate(self):
        return self.__ycoordinate

    def set_xy_draw(self, xcoord, ycoord):
        Node.set_xy_draw(self, xcoord, ycoord)

    def get_x_draw(self):
        return Node.get_x_draw(self)

    def get_y_draw(self):
        return Node.get_y_draw(self)

    def set_left_sibling(self, sibling):
        self.__left_sibling = sibling

    def get_left_sibling(self):
        return self.__left_sibling

    def set_right_sibling(self, sibling):
        self.__right_sibling = sibling

    def get_right_sibling(self):
        return self.__right_sibling

    def set_first_child(self, child):
        self.__mostleft_child = child

    def get_first_child(self):
        return self.__mostleft_child


class FFNode(Node):
    # typ: input, output, hidden
    def __init__(self, name, type):
        Node.__init__(self, name)
        self.__type = type
        self.__value = 0
        self.__parent = None
        self.__name = name

    def name(self):
        return Node.name(self)

    def get_value(self):
        return self.__value

    def set_value(self, newvalue):
        self.__value = newvalue

    def add_edge(self, end, weight):
        Node.add_weighted_edge(self, end, weight)

    def remove_edge(self, end):
        Node.remove_edge(self, end)

    def get_edges(self):
        return Node.get_edges(self)

    def get_type(self):
        return self.__type

    def __str__(self):
        return self.__name

    def set_xy_draw(self, xcoord, ycoord):
        Node.set_xy_draw(self, xcoord, ycoord)

    def get_x_draw(self):
        return Node.get_x_draw(self)

    def get_y_draw(self):
        return Node.get_y_draw(self)

    def set_parent(self, parent):
        self.__parent = parent


class BayesNode(Node):
    def __init__(self, name, problist, ebene):
        Node.__init__(self, name)
        self.__prob = problist
        self.__ebene = ebene

    def name(self):
        return Node.name(self)

    def ebene(self):
        return self.__ebene

    def get_edges(self):
        return Node.get_edges(self)

    def set_probs(self, prob):
        self.__probs = prob

    def get_probs(self):
        return self.__prob

    def __str__(self):
        return Node.__str__(self)

    def add_edge(self, end):
        Node.add_edge(self, end)

    def remove_edge(self, end):
        Node.remove_edge(self, end)

    def set_xy_draw(self, xcoord, ycoord):
        Node.set_xy_draw(self, xcoord, ycoord)

    def get_x_draw(self):
        return Node.get_x_draw(self)

    def get_y_draw(self):
        return Node.get_y_draw(self)

    def set_parent(self, parent):
        self.__parent = parent

    def get_parent(self):
        return Node.get_parent(self)
