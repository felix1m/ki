# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""

from tkinter import *

# globale Variablen fuer Spielbaeume:
xTopAdjustment = 100
yTopAdjustment = 100
LevelSeparation = 70  # const. distance
MaxDepth = 100  # max number of levels
SiblingSeparation = 30  # min distance
SubtreeSeparation = 30  # distance
meannodesize = 55
fenster = ""
fenstername = ""
have_matches = 4
comp_have = 0
i_have = 0
levellist = []


def set_window(window, name):
    global fenster
    global fenstername
    fenster = window
    fenstername = name


def zeichne_oval(x1, y1, x2, y2, farbe):
    fenster.create_oval(x1, y1, x2, y2, fill = farbe)


def zeichne_rechteck(x1, y1, x2, y2):
    fenster.create_rectangle(x1, y1, x2, y2)


def zeichne_leeres_oval(x1, y1, x2, y2):
    fenster.create_oval(x1, y1, x2, y2)


def schreibe_text_anzeige(x, y, text):
    fenster.create_text(x, y, anchor= W, text = text)


def zeichne_linie(x1, y1, x2, y2, farbe):
    fenster.create_line(x1, y1, x2, y2, fill = farbe)


def schreibe_text(fenster, text):
    fenster.insert(END, text)
    fenster.insert(END, "\n")


def draw(graph, wurzel, layers):
    umgebung = graph.__class__.__name__
    if umgebung == "MapGraph":
        scale_map(graph)
    if umgebung == "GameGraph":
        draw_match_start()
    if umgebung == "FFNetwork":
         draw_ffn(graph)
    if umgebung == "BayesGraph":
        draw_bayes(graph)
        
# skaliert und zeichnet Map!
def scale_map(graph):
    # anzeigefenster = 400 x 400
    max_x = 0
    max_y = 0
    # groesste x und y werte bekommen:
    for node in graph.get_nodes():
        xcoord = node.get_x_coordinate()
        ycoord = node.get_y_coordinate()
        if xcoord > max_x:
            max_x = xcoord
        if ycoord > max_y:
            max_y = ycoord
    # alle Punkte auf vorhandenen Platz skalieren:
    for node in graph.get_nodes():
        xcoord = node.get_x_coordinate()
        ycoord = node.get_y_coordinate()
        xcoord_draw = xcoord*(350/max_x)
        # 390 und +5, damit der Rand 5 Pixel frei bleibt
        ycoord_draw = ycoord*(350/max_y)
        node.set_xy_draw(xcoord_draw, ycoord_draw)
    draw_map(graph)


def draw_map(graph):
    for node in graph.get_nodes():
        xcoord_draw = node.get_x_draw()
        ycoord_draw = node.get_y_draw()
        city = node.name()
        zeichne_oval(xcoord_draw-3, ycoord_draw-3, xcoord_draw+3,
                     ycoord_draw+3, "black")
        schreibe_text_anzeige(xcoord_draw-10, ycoord_draw+10, city)
        for edge in node.get_edges():
            xcoord_e = edge.end().get_x_draw()
            ycoord_e = edge.end().get_y_draw()
            zeichne_linie(xcoord_draw, ycoord_draw, xcoord_e, ycoord_e,
                          "black")
            xcoord_m = (xcoord_draw + xcoord_e)/2
            ycoord_m = (ycoord_draw + ycoord_e)/2
            roadlength = edge.weight
            schreibe_text_anzeige(xcoord_m, ycoord_m, roadlength)
            


def draw_match_start():
    global have_matches
    global i_have
    global comp_have
    have_matches = 4
    i_have = 0
    comp_have = 0
    fenster.create_line(150, 0, 150, 150, fill = "black", width=2)
    fenster.create_line(0, 150, 150, 150, fill = "black", width=2)
    fenster.create_line(400, 250, 250, 250, fill = "black", width=2)
    fenster.create_line(250, 400, 250, 250, fill = "black", width=2)
    fenster.create_text(10, 10, anchor= W, text = "Computers:")
    fenster.create_text(260, 260, anchor= W, text = "Mine:")
    # streichhoelzer:
    fenster.create_line(170, 200, 170, 230, fill = "black", width=2)
    fenster.create_line(190, 200, 190, 230, fill = "black", width=2)
    fenster.create_line(210, 200, 210, 230, fill = "black", width=2)
    fenster.create_line(230, 200, 230, 230, fill = "black", width=2)


def take_match():
    global have_matches
    if have_matches == 4:
        # das vierte wird geloescht
        fenster.create_line(230, 200, 230, 230, fill = "white", width=2)
    elif have_matches == 3:
        # das dritte wird geloescht
        fenster.create_line(210, 200, 210, 230, fill = "white", width=2)
    elif have_matches == 2:
        # das zweite wird geloescht
        fenster.create_line(190, 200, 190, 230, fill = "white", width=2)
    elif have_matches == 1:
        # das letzte wird geloescht
        fenster.create_line(170, 200, 170, 230, fill = "white", width=2)
    have_matches -= 1


def give_comp_match():
    global comp_have
    if comp_have == 0:
        fenster.create_line(50, 90, 50, 120, fill = "black", width=2)
    elif comp_have == 1:
        fenster.create_line(70, 90, 70, 120, fill = "black", width=2)
    elif comp_have == 2:
        fenster.create_line(90, 90, 90, 120, fill = "black", width=2)
    elif comp_have == 3:
        fenster.create_line(110, 90, 110, 120, fill = "black", width=2)
    comp_have += 1


def give_me_match():
    global i_have
    if i_have == 0:
        fenster.create_line(300, 310, 300, 340, fill = "black", width=2)
    elif i_have == 1:
        fenster.create_line(320, 310, 320, 340, fill = "black", width=2)
    elif i_have == 2:
        fenster.create_line(340, 310, 340, 340, fill = "black", width=2)
    elif i_have == 3:
        fenster.create_line(360, 310, 360, 340, fill = "black", width=2)
    i_have += 1


def draw_ffn(graph):
    ebene = [[]]
    a = True
    list = []
    for node in graph.get_nodes():
        if node.get_type() == "input":
            ebene[0].append(node.name())
    i = 0
    while a:
        ebene.append([])
        for node in ebene[i]:
            node = graph.get_node(node)
            for edge in node.get_edges():
                if edge.end().name() not in ebene[i+1]:
                    ebene[i+1].append(edge.end().name())
                if edge.end().get_type() == "output":
                    a = False
        i += 1
    # zeichnen(fenster = 400 x 400
    anzahlebenen = len(ebene)
    space_x = 390/anzahlebenen  # xcoord f. ebene[0] = 1*space usw.
    for i in range(len(ebene)):  # jede ebene durchgehen
        anzahl = len(ebene[i])
        space_y = 390/anzahl
        nr = 1
        for node in ebene[i]:  # jedes element der einzelnen Ebene
            if node == "O":
                graph.get_node(node).set_xy_draw((i+1)*space_x-50,
                                                       0.55*space_y)
            else:
                graph.get_node(node).set_xy_draw((i+1)*space_x-50, nr*space_y)
                nr += 1
    # zeichnen:
    for node in graph.get_nodes():
        schreibe_text_anzeige(node.get_x_draw(), node.get_y_draw(),
                              node.name())
        for edge in node.get_edges():
            zeichne_linie(node.get_x_draw(), node.get_y_draw(),
                          edge.end().get_x_draw(), edge.end().get_y_draw(),
                          "black")


def draw_tree(graph):
    maxx = 0
    maxy = 0
    minx = 0
    miny = 0
    for node in graph.get_nodes():
        xcoord = node.get_x_draw()
        ycoord = node.get_y_draw()
        if xcoord < minx:
            minx = xcoord
    # falls baum links aus fenster rauskommt, muessen alle knoten nach rechts
    # verschoben werden, also um minx.
    if minx < 0:
        for node in graph.get_nodes():
            ycoord = node.get_y_draw()
            # +10, damit der knoten nicht direkt am rand beginnt.
            xcoord = (node.get_x_draw() - minx) +10 
            node.set_xy_draw(xcoord, ycoord)
    # dann schauen, was die maxwerte sind:
    for node in graph.get_nodes():
        xcoord = node.get_x_draw()
        ycoord = node.get_y_draw()
        if xcoord+50 > maxx:
            maxx = xcoord+50
        if ycoord+20 > maxy:
            maxy = ycoord+20
    if (fenstername == "anzeige" and maxx < 390 and
            maxy < 390) or (fenstername != "anzeige"):
        for node in graph.get_nodes():
            xcoord = node.get_x_draw()
            ycoord = node.get_y_draw()
            name = node.name()
            try:
                while isinstance(int(name[-1]), int):
                    name = name[:-1]
            except:
                pass
            zeichne_rechteck(xcoord, ycoord, xcoord+55, ycoord+20)
            schreibe_text_anzeige(xcoord+5, ycoord+10, name)
            for edge in node.get_edges():
                x_end = edge.end().get_x_draw()
                y_end = edge.end().get_y_draw()
                title = edge.title()
                zeichne_linie(xcoord+25, ycoord+20, x_end+25, y_end, "black")
                schreibe_text_anzeige((xcoord+25+x_end+25)/2,
                                      (ycoord+20+y_end)/2, title)
    else:  # fenster ist anzeige, aber zu gross zum zeichnen:
        schreibe_text_anzeige(30, 200,
                              "Unfortunately, the tree is too big to be drawn here! \nPlease open in seperate window! ('Show Decisiontree')")

    size = (maxx, maxy)
    return size


def draw_decision(graph):
    global levellist
    levellist = []
    # fuer jeden knoten benoetigt: Wurzel, parent,
    # leftmost child, leftsibling, rightsibling:
    for node in graph.get_nodes():
        leftmost = False
        leftsibling = None
        for edge in node.get_edges():
            edge.end().set_parent(node)
            if not leftmost:
                node.set_first_child(edge.end())
                leftmost = True
            if leftsibling is not None:
                edge.end().set_left_sibling(leftsibling)
                leftsibling.set_right_sibling(edge.end())
            leftsibling = edge.end()
    size = positiontree(graph, graph.get_root())
    return size

def positiontree(graph, wurzel):
    global xTopAdjustment
    global yTopAdjustment
    for node in graph.get_nodes():
        neighbor = left_neighbor(graph, node)
        node.set_left_neighbor(neighbor)
    firstwalk(graph, wurzel, 0)
    # for node in graph.get_nodes():
    xTopAdjustment = wurzel.get_x_coordinate() - wurzel.get_prelim()
    yTopAdjustment = wurzel.get_y_coordinate()
    if secondwalk(graph, wurzel, 0, 0):
        #nochmal alle durchgehen, schauen ob knoten kollidieren!
        for node in graph.get_nodes():
            node.set_modifier(0)
            for index in range(len(levellist)):
                try:
                    n = levellist[index].index(node.name())
                    m = index
                    if n != 0:
                        node.set_left_neighbor(graph.get_node(levellist[m][n-1]))
                        break
                    else:
                        node.set_left_neighbor(None)
                        break
                except:
                    pass
          
        thirdwalk(graph, wurzel, 0)
        size = draw_tree(graph)
        return(size)


def firstwalk(graph, node, level):
    global levellist
    if len(levellist)-1 < level:
        levellist.append([])
    if node.name() not in levellist[level]:
        levellist[level].append(node.name())
    node.set_modifier(0)
    if (is_leaf(node) or level == MaxDepth):
        if (node.get_left_sibling() is not None):
            # knoten hat linke geschwister!!
            pre = ((node.get_left_sibling().get_prelim()) +
                   SiblingSeparation + meannodesize)
            node.set_prelim(pre)
        else:  # no left sibling to worry about
            node.set_prelim(0)
    else:  # node is no leaf,call this procedure recursively for each of its
        # offspring
        leftmost = node.get_first_child()
        rightmost = node.get_first_child()
        firstwalk(graph, leftmost, level+1)
        while(rightmost.get_right_sibling() is not None):
            rightmost = rightmost.get_right_sibling()
            firstwalk(graph, rightmost, level+1)
        midpoint = (leftmost.get_prelim() + rightmost.get_prelim())/2
        if(node.get_left_sibling() is not None):
            pre = (node.get_left_sibling().get_prelim() + SiblingSeparation +
                   meannodesize)
            node.set_prelim(pre)
            mod = node.get_prelim() - midpoint
            node.set_modifier(mod)
            apportion(graph, node, level)
        elif(node.get_left_neighbor() is not None):
            pre = (node.get_left_neighbor().get_prelim() + SubtreeSeparation +
                   meannodesize)
            node.set_prelim(pre)
            mod = node.get_prelim() - midpoint
            node.set_modifier(mod)
            apportion(graph, node, level)
        else:
            node.set_prelim(midpoint)


def secondwalk(graph, node, level, modsum):
    global xTopAdjustment
    global yTopAdjustment
    result = True
    if level <= MaxDepth:
        xTemp = xTopAdjustment + node.get_prelim() +  modsum
        yTemp = yTopAdjustment + (level * LevelSeparation)
        node.set_xy_draw(xTemp, yTemp)
        if not is_leaf(node):  # knoten hat kinder!
                # apply modifier value to all of its offspring
            result = secondwalk(graph, node.get_first_child(), level+1,
                                modsum + node.get_modifier())
        if (result and node.get_right_sibling() is not None):
            result = secondwalk(graph, node.get_right_sibling(), level, modsum)
    else:
        # sind ein level tiefer, als wir wollen.
        result = True
    return result


def left_neighbor(graph, node):
    # linker nachbar = linker geschwisterknoten, wenn vorhanden:
    if node.get_left_sibling() is not None:
        return node.get_left_sibling()
    else:  # kein linker Geschwisterknoten, muss auf eltern zurueckgreifen!
        if node.get_parent() is not None:
            elter = node.get_parent()
            if elter.get_left_sibling() is not None:
                # elternknoten hat geschwister, brauche rchtestes kind des
                # geschwisterkotens
                egeschwister = elter.get_left_sibling()
                if egeschwister.get_first_child() is not None:
                    # geschwister von e hat auch kinder!
                    rightmost = egeschwister.get_first_child()
                    while(rightmost.get_right_sibling() is not None):
                        rightmost = rightmost.get_right_sibling()
                    return rightmost
                else:
                    return None
            else:  # elter hat keine geschwister:
                # hat elter nachbar?
                if elter.get_left_neighbor() is None:
                    # hat keinen nachbar! villt muss nachbar erst gesetzt
                    # werden!
                    elternachbar = left_neighbor(graph, elter)
                    node.get_parent().set_left_neighbor(elternachbar)
                if elter.get_left_neighbor() is not None:
                    # hat nun nachbar, entweder schon von vorher oder
                    # gerade neu erstellt!
                    enachbar = elter.get_left_neighbor()
                    if enachbar.get_first_child() is not None:
                        # geschwister von e hat auch kinder!
                        rightmost = enachbar.get_first_child()
                        while(rightmost.get_right_sibling() is not None):
                            rightmost = rightmost.get_right_sibling()
                        return rightmost
                    else:
                        return None
                else:
                    return None
        else:
            return (None)


def is_leaf(node):
    # im entschbaum leaf, wenn name == no oder yes.
    name = list(node.name())
    number = 0
    for edge in node.get_edges():
        number += 1
    if number == 0:
        return True
    else:
        return False


def getleftmost(node, level, depth):
    if level >= depth:
        return node
    elif is_leaf(node):
        return None
    else:
        rightmost = node.get_first_child()
        leftmost = getleftmost(rightmost, level +1, depth)
        # postorder walk of the subtree below node
        while (leftmost is None and rightmost.get_right_sibling() is not None):
            rightmost = rightmost.get_right_sibling()
            leftmost = getleftmost(rightmost, level+1, depth)  # level+1
        return leftmost

def apportion(graph, node, level):
    # wird aufgerufen, wenn ich kinder habe UND linken nachbarn!
    # pre wurde auf nachbar pre + sibling sep gesetzt,
    # mod wurde auf pre + midpoint gesetzt.
    # teste, ob subtree eines nachbarn mit meinem subtree kollidiert.
    leftmost = node.get_first_child()
    neighbor = leftmost.get_left_neighbor()
    compareDepth = 1
    # eigenes kind != None, nachbar vom Kind != None:
    if (leftmost is not None and neighbor is not None and
           compareDepth < 100):
        leftmodsum = 0
        rightmodsum = 0
        ancestorLeftmost = leftmost
        ancestorNeighbor = neighbor
        for i in range(compareDepth):
            # mod. von den Eltern werden addiert
            ancestorLeftmost = ancestorLeftmost.get_parent()
            ancestorNeighbor = ancestorNeighbor.get_parent()
            rightmodsum = rightmodsum + ancestorLeftmost.get_modifier()
            leftmodsum = leftmodsum + ancestorNeighbor.get_modifier()
        # wie weit sind subbaeume getrennt?
        distance = (leftmost.get_prelim() + 
                    rightmodsum) - (neighbor.get_prelim() +
                    leftmodsum)
        # rechter baum muss bewegt werden!
        if distance < (SubtreeSeparation + meannodesize):
            toMove = (SubtreeSeparation + meannodesize)- distance
            newMod = node.get_modifier() + toMove
            node.set_modifier(newMod)
            newPre = node.get_prelim() + toMove
            node.set_prelim(newPre)
        else:
            # alles okay, baum muss nicht bewegt werden!
            return
        compareDepth += 1
        
def thirdwalk(graph, node, move):
    if is_leaf(node):
        node.set_xy_draw(node.get_x_draw()+ move, node.get_y_draw())
        if node.get_left_neighbor() is None:
            return 0
        else:
            # ist mindestbstand eingehalten?
            distance = node.get_x_draw() - node.get_left_neighbor().get_x_draw()
            if distance >= (SubtreeSeparation + meannodesize):
                return 0
            else:
                mod = (SubtreeSeparation + meannodesize) - distance
                node.set_xy_draw(node.get_x_draw() + mod, node.get_y_draw())
                return mod
    else:
        mod = move
        leftmost = node.get_first_child()
        rightmost = node.get_first_child()
        mod += thirdwalk(graph, leftmost, mod)
        while(rightmost.get_right_sibling() is not None):
            rightmost = rightmost.get_right_sibling()
            mod += thirdwalk(graph, rightmost, mod)
        newx = node.get_x_draw() + mod
        if node.get_left_neighbor() is None:
            node.set_xy_draw(newx, node.get_y_draw())
            return mod
        else:
            distance = newx - node.get_left_neighbor().get_x_draw()
            if distance >= (SubtreeSeparation + meannodesize):
                node.set_xy_draw(newx, node.get_y_draw())
                return mod/2
            else:
                mod += (SubtreeSeparation + meannodesize) - distance
                for edge in node.get_edges():
                    move_subtree(graph, edge.end(), mod)
                node.set_xy_draw(newx + mod, node.get_y_draw())
                return mod
                
def move_subtree(graph, node, mod):
    # alle Nachfolger von node muessen um mod verschoben werden.
    if is_leaf(node):
        node.set_xy_draw(node.get_x_draw() + mod, node.get_y_draw())
        return
    else:
        node.set_xy_draw(node.get_x_draw() + mod, node.get_y_draw())
        for edge in node.get_edges():
            move_subtree(graph, edge.end(), mod)


def draw_bayes(graph):
    maxebene = 0
    for node in graph.get_nodes():
        if node.ebene() > maxebene:
            maxebene = node.ebene()
    knotenInEbene = []
    maxebene += 1  # weil knotenebene bei 0 beginnt.
    for ebene in range(maxebene):
        knotenInEbene.append([])
    for node in graph.get_nodes():
        knotenInEbene[node.ebene()].append(node.name())
    yebenestart = 400/(maxebene + 1)
    yebene = yebenestart
    for ebene in range(maxebene):
        numberNodes = len(knotenInEbene[ebene])
        xebenestart = 400/(numberNodes + 1)
        xebene = xebenestart
        for nodename in knotenInEbene[ebene]:
            node = graph.get_node(nodename)
            node.set_xy_draw(xebene, yebene)
            xebene += xebenestart
        yebene += yebenestart
    for node in graph.get_nodes():
        x = node.get_x_draw()
        y = node.get_y_draw()
        zeichne_leeres_oval(x, y, x+60, y+40)
        schreibe_text_anzeige(x+7, y+20, node.name())
    for node in graph.get_nodes():
        xstart = node.get_x_draw() + 30
        ystart = node.get_y_draw() +40
        for edge in node.get_edges():
            if node.ebene() < edge.end().ebene():
                xend = edge.end().get_x_draw() +30
                yend = edge.end().get_y_draw()
                zeichne_linie(xstart, ystart, xend, yend, "black")
            
        
    