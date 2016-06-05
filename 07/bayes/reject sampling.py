# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""

from helpimport import *
import random

def main(graph, X, e, n):
    # Belegung der Knoten:
    x = []
    elternbelegung = []
    # fuer jeden Knoten:
    for i in range(4):
        elternbelegung.append([])
        for node in graph.get_nodes():
            if int(node.ebene()) == i:
                elter = ""
                wkeit = node.get_probs()
                for el in range(len(elternbelegung[i-1])):
                    if el == len(elternbelegung[i-1])-1:
                        elter = elter+str(elternbelegung[i-1][el])
                    else:
                        elter = elter+str(elternbelegung[i-1][el]) + ", "
                zahl = random.uniform(0, 1)
                # alle moeglichen elternbelegungen durchgehen
                for j in range (len(wkeit)):
                    if len(elter.split()) > 1:
                        belegung = []
                        # es gibt mehr als einen elternknoten!
                         # jeder elternknoten muss in wkeit[j][0] sein:
                        for el in elter.split(", "):
                            
                            if any (e == el for e in wkeit[j][0].split(", ")):
                                belegung.append(True)  
                                # gesuchter elternknoten ist in 
                                # elternmoeglichkeit vorhanden.
                            else:
                                belegung.append(False)  # nicht vorhanden.
                        if any (b == False for b in belegung):
                            continue
                        else:
                            
                            # alle wahr, eltern belegung stimmt also, kann 
                            # nun entschieden werden wie knoten selbst belegt 
                            # wird.
                            if zahl <= float(wkeit[j][1]):
                                x.append(node.name())
                                elternbelegung[i].append(node.name())
                            else:
                                neu = "-" + node.name()
                                x.append(neu)
                                elternbelegung[i].append(neu)
                            break
                    else:  # es gibt nur einen elternknoten.
                        if wkeit[j][0] == elter:
                            if zahl <= float(wkeit[j][1]):
                                x.append(node.name())
                                elternbelegung[i].append(node.name())
                            else:
                                neu = "-" + node.name()
                                x.append(neu)
                                elternbelegung[i].append(neu)
                            break
    return x