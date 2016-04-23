"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""
from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from Graph import *
import zeichne
import matchesrules
from sys import path
import os
from os import path
import math
import random
import numpy as np
import matplotlib.pyplot as plt
import hinton
from matplotlib.figure import Figure


# Fenster:
ki = Tk()
ki.geometry("760x440")
ki.title("AIMA")

# globale Variablen
neu = True  # Ist es die erste Umgebung, die geoeffnet wird?
error = False  # fuer fehler beim laden von Daten
directory = ""
algoindex = 0
importdict = {}

# globale Variablen
graph = MapGraph(" ", "anzeigefenster", "printfenster", ki)
importiert = []  # ""
importiertname = []  # ""
rejection_sam_var = [graph, "", "", 20]
startvar = StringVar(ki)
goalvar = StringVar(ki)
probsvar = ""
alphaffn = DoubleVar()
alphaffn.set(0.2)
schwellwertffn = DoubleVar()
schwellwertffn.set(2.5)
hintonnumberffn = IntVar()
hintonnumberffn.set(20)

# globale Namen fuer buttons, pull down usw:
printfenster = ""
anzeigefenster = ""
# routenplanung:
startm = ""
goalm = ""
runbutton = ""
startlabel = ""
goallabel = ""
# Spiele:
zerobutton = ""
onebutton = ""
twobutton = ""
turnbutton = ""

gesetzt = False
belegt = []
# matches:
hat_max = 0
hat_min = 0
noch_da = 4
pfad = ""
# bayes:
probtable = ""
backprob = ""
bayesrunbutton = ""
probtable = ""
probslabel = ""
parameterbutton = ""
# Feed-Forward Netze
examplebutton = ""
schwellwert = 2.5
hintonnumber = 20
alpha = 0.2
ownexample = ""
ffnname = ""
backproperties = ""
# Decision:
decidebutton = ""
decisiontable = ""
decisiontree = ""

sizedec = ""


# Routenplanung:
def routefinding():
    global graph
    global startm
    global goalm
    global runbutton
    global startlabel
    global goallabel
    global error

    if neu:
        add_clear_and_window()
    else:
        clear_gui()
    # Leiste mit Auswahl für Start, Ziel, properties, Steps, Run
    startlabel = Label(ki, text="Start:")
    startlabel.grid(row=0, column=0)
    startm = OptionMenu(ki, startvar, "Start")
    startm.grid(row=0, column=1)
    goallabel = Label(ki, text="Goal:")
    goallabel.grid(row=0, column=2)
    goalm = OptionMenu(ki, goalvar, "Goal")
    goalm.grid(row=0, column=3)
    runbutton = Button(ki, text="Run", command=run)
    runbutton.grid(row=0, column=4)

    # ordner oeffnen, nur die Map-Files anzeigen:
    # datei ist die Ascii-Datei mit den staedten und strassen.
    folder = os.path.abspath(os.path.dirname("AIMA.py"))
    folder = folder.split("\\aima")[0]
    folder = folder + "\\routen"
    name = filedialog.askopenfilename(filetypes=[("Map files", "*.map")], 
                                      initialdir=(folder))
    try:
        datei = open(name).read()

        szenario = []
        for string in datei.split("\n"):
            szenario.append(string)
        name = szenario[0]
        numberofcities = int(szenario[1])
        numberofstreets = int(szenario[2 + numberofcities])
        graph = MapGraph(name, anzeigefenster, printfenster, ki)

        # staedte in graphen aufnehmen, Liste fuer das Menue erweitern.
        new_cities_s = []
        new_cities_g = []
        for element in range(2, 2 + numberofcities, 1):
            szenario[element] = szenario[element].split()
            city = szenario[element][0]
            new_cities_s.append(city)
            new_cities_g.append(city)
            xcoord = int(szenario[element][1])
            ycoord = int(szenario[element][2])
            graph.add_node(city, xcoord, ycoord)
            # neue staedte in optionmenue aufnehmen:
        startm['menu'].delete(0, 'end')
        goalm['menu'].delete(0, 'end')
        for city in new_cities_s:
            startm["menu"].add_command(label=city,
                                       command=tk._setit(startvar, city))
        for city in new_cities_g:
            goalm["menu"].add_command(label=city,
                                      command=tk._setit(goalvar, city))
        startvar.set(new_cities_s[0])
        goalvar.set(new_cities_g[-1])
        # Straßen in graphen aufnehmen
        for element in range(3 + numberofcities,
                             3 + numberofcities + numberofstreets, 1):
            szenario[element] = szenario[element].split()
            start = szenario[element][0]
            end = szenario[element][1]
            start = graph.get_node(start)
            end = graph.get_node(end)
            lengthofroad = int(szenario[element][2])
            graph.add_edge(start.name(), end.name(), lengthofroad)
            # skalieren und zeichnen
        zeichne.draw(graph, "", "")
        error = False
    except:
        printfenster.insert(END, "Error\n")
        error = True


# Geladenen Algo aufrufen
def run():
    if not error:
        zeichne.scale_map(graph)
        # falls vorher schon wege gezeichnet waren,
        # werden diese jetzt "geloescht"
        anfang = startvar.get()
        ende = goalvar.get()
        # falls vorher schon gezeichnet wurde,
        # wurden eltern belegt, diese nun loeschen
        for node in graph.get_nodes():
            node.set_parent(None)

        try:
            # start und end knoten rot faerben
            anfangknoten = graph.get_node(anfang)
            xcoord_a = anfangknoten.get_x_draw()
            ycoord_a = anfangknoten.get_y_draw()
            zeichne.zeichne_oval(xcoord_a - 3,
                                 ycoord_a - 3, xcoord_a + 3,
                                 ycoord_a + 3, "red")

            endknoten = graph.get_node(ende)
            xcoord_e = endknoten.get_x_draw()
            ycoord_e = endknoten.get_y_draw()
            zeichne.zeichne_oval(xcoord_e - 3,
                                 ycoord_e - 3,
                                 xcoord_e + 3, ycoord_e + 3, "red")

            ki.update()
        except KeyError:
            new_window("Choose!", "Please choose Start and Goal!")
            # algo ausfuehren
        importiert[algoindex-1].main(graph, anfang, ende)
        new_window("Done", "Done!")
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


# Spiele: Steichholzspiel
def match_game():
    global graph
    global gesetzt
    global zerobutton
    global onebutton
    global twobutton
    global turnbutton
    gesetzt = False  # erster Zug ist der des Spielers.
    if neu:
        add_clear_and_window()
    else:
        clear_gui()
    graph = GameGraph("")  # fuer clear!
    printfenster.insert(END, ">>")
    printfenster.insert(END,
                        "Rules: You can take 0, 1 or 2 matches.The object of play is to be able to take\nthe last match away. If player A takes 0\nmatches, player B and player A have to \ntake at least one when it's their turn \nagain. If you want to take 2 matches, at\nleast one match has to remain.")
    printfenster.insert(END, "\n")

    zerobutton = Button(ki, text="Take 0", command=choose_zero)
    zerobutton.grid(row=0, column=0)
    onebutton = Button(ki, text="Take 1", command=choose_one)
    onebutton.grid(row=0, column=1)
    twobutton = Button(ki, text="Take 2", command=choose_two)
    twobutton.grid(row=0, column=2)
    zeichne.draw_match_start()

# Algo ausfuehren
def play_matches():
    global noch_da
    global pfad
    global gesetzt
    zustand = str(noch_da) + pfad
    zustand = importiert[algoindex-1].main(zustand)
    # dort: return zustand
    zustand = list(zustand)
    noch_da = int(zustand[0])
    pfad = ""
    # angaben ueber die entscheidung treffen, 
    # Hoelzer verteilen
    for i in range(1, len(zustand), 1):
        pfad = pfad + zustand[i]
    last = zustand[len(zustand) - 1]
    if last == "0":
        printfenster.insert(END, "Computer took 0 matches.")
        printfenster.insert(END, "\n")
    if last == "1":
        printfenster.insert(END, "Computer took 1 match.")
        printfenster.insert(END, "\n")
        zeichne.take_match()
        zeichne.give_comp_match()
    if last == "2":
        printfenster.insert(END, "Computer took 2 matches.")
        printfenster.insert(END, "\n")
        zeichne.take_match()
        zeichne.take_match()
        zeichne.give_comp_match()
        zeichne.give_comp_match()
    gesetzt = False
    if noch_da == 0:
        printfenster.insert(END, "You lost!")
        new_window("Lost!", "You lost!")


def choose_zero():
    global noch_da
    global pfad
    global gesetzt
    if gesetzt:
        new_window("Sorry!", "It's not your turn!")
    else:
        helppfad = list(str(noch_da) + str(pfad))
        if matchesrules.take_0_poss(
                helppfad):
            gesetzt = True
            pfad = pfad + "0"
            printfenster.insert(END, "You took 0 matches.\n")
            play_matches()
        else:
            new_window("Choose!", "You have to take at least one!")


def choose_one():
    global noch_da
    global gesetzt
    global pfad
    if gesetzt:
        new_window("Sorry!", "It's not your turn!")
    else:
        if noch_da == 0:
            new_window("Sorry!", "There are no more matches you could take!")
        else:
            zustand = list(str(noch_da) + str(pfad))
            if matchesrules.take_1_poss(zustand):
                zeichne.take_match()
                zeichne.give_me_match()
                gesetzt = True
                noch_da -= 1
                pfad = pfad + "1"
                printfenster.insert(END, "You took 1 match.\n")
                if noch_da == 0:
                    printfenster.insert(END, "You won!")
                    new_window("Won!", "You won!")
                else:
                    play_matches()
            else:
                new_window("Sorry!", "You are not allowed to take 1 match!")


def choose_two():
    global noch_da
    global gesetzt
    global pfad
    if gesetzt:
        new_window("Sorry!", "It's not your turn!")
    else:
        if noch_da == 0:
            new_window("Sorry!", "There are no more matches you could take!")
        else:
            zustand = list(str(noch_da) + str(pfad))
            if matchesrules.take_2_poss(zustand):
                pfad = pfad + "2"
                noch_da -= 2
                zeichne.take_match()
                zeichne.take_match()
                zeichne.give_me_match()
                zeichne.give_me_match()
                gesetzt = True
                printfenster.insert(END, "You took 2 matches.\n")
                play_matches()
            else:
                new_window("Sorry!",
                           "You cannot take 2; at least one has to remain!")


# Feed-ForwardNetwork: Restaurant
def restaurantffn():
    global graph
    global backprob
    global img
    global examplebutton
    global backproperties
    global error
    global ffnname

    if neu:
        add_clear_and_window()
    else:
        clear_gui()
    if graph.__class__.__name__ == "FFNetwork":
        zeichne.draw(graph, "", "")
    number_inputnodes = 0
    number_hiddennodes = 0
    # Buttons etc:
    backprob = Button(ki, text="Backpropagation",
                      command=lambda: backpropagation(ex, number_inputnodes,
                                                      number_hiddennodes))
    backprob.grid(row=0, column=5)
    backproperties = Button(ki, text="Poperties", command = properties_ffn)
    backproperties.grid(row=0, column=2)
    examplebutton = Button(ki, text="Insert own Example!", command=enterbackprop)
    examplebutton.grid(row=0, column=4)

    # bsp aufnhemen:
    folder = os.path.abspath(os.path.dirname("AIMA.py"))
    folder = folder.split("\\aima")[0]
    folder = folder + "\\feedforward"
    name = filedialog.askopenfilename(filetypes=[("Feature files", "*.feat")], 
                                                 initialdir=(folder))
    ffnname = name
    try:
        datei = open(name).read()
        ex = []
        szenario = []
        for string in datei.split("\n"):
            szenario.append(string)
        name = szenario[0]
        numberofexamples = int(szenario[3])
        for element in range(4, 4 + numberofexamples, 1):
            ex.append([])
            szenario[element] = szenario[element].split()
            for item in szenario[element]:
                if item == "Yes" or item == "Full" or item == "Expensive":
                    bewertung = 1
                elif item == "No" or item == "None" or item == "Cheap":
                    bewertung = -1
                elif item == "Some" or item == "Okay":
                    bewertung = 0
                elif item == "0-10" or item == "French":
                    bewertung = 1
                elif item == "10-30" or item == "Thai":
                    bewertung = 0.5
                elif item == "30-60" or item == "Burger":
                    bewertung = -0.5
                elif item == ">60" or item == "Italian":
                    bewertung = -1
                ex[element - 4].append(bewertung)
        error = False
        number_nodes = restaurantffn_net_topology()
        number_inputnodes = number_nodes[0]
        number_hiddennodes = number_nodes[1]
    except:
        printfenster.insert(END, "Error\n")
        error = True


def restaurantffn_net_topology():
    global graph
    global error
    global ffnname
    
    number_nodes = [0, 0]
    graph = FFNetwork("", anzeigefenster, printfenster, ki)  # fuer clear_gui
    
    folder = os.path.abspath(os.path.dirname("AIMA.py"))
    folder = folder.split("\\aima")[0]
    path = folder + "\\feedforward"
    
    #path = os.path.abspath(os.path.dirname(__file__))
    # datei mit selben namen.ffn wie bsp werden geoeffnet
    ffnname = ffnname.split("/")
    ffnname = ffnname[-1]
    ffnname = ffnname.split(".")
    ffnname = ffnname[0]
    name = str(path)+"/"+ffnname+".ffn"
    print(name)
    try:
        datei = open(name).read()
        matrix = np.empty([15, 15])  # fuer hinton diagramm
        szenario = []
        for string in datei.split("\n"):
            szenario.append(string)
        name = szenario[0]
        numberofnodes = int(szenario[1])
        numberofedges = int(szenario[2 + numberofnodes])
        graph = FFNetwork(name, anzeigefenster, printfenster, ki)
        # knoten und kanten in graphen aufnehmen:
        for element in range(2, 2 + numberofnodes, 1):
            szenario[element] = szenario[element].split()
            nameofnode = szenario[element][0]
            nodetype = szenario[element][1]
            graph.add_node(nameofnode, nodetype)
            if nameofnode[0] == "I":
                number_nodes[0] += 1
            if nameofnode[0] == "H":
                number_nodes[1] += 1
        for element in range(3 + numberofnodes,
                             3 + numberofnodes + numberofedges, 1):
            szenario[element] = szenario[element].split()
            start = szenario[element][0]
            end = szenario[element][1]
            start = graph.get_node(start)
            end = graph.get_node(end)
            weight = random.randint(0, 100) / 100
            graph.add_edge(start.name(), end.name(), weight)
            # matrix fuellen:
        for zeile in range(15):
            for spalte in range(15):
                matrix[zeile][spalte] = 0
        for node in graph.get_nodes():
            name = node.name()
            for edge in node.get_edges():
                dest = edge.end().name()
                weight = edge.weight
                # ueberpruefung worein es geschireben wird:
                if name[0] == "I":
                    oben = int(name[1])
                elif name[0] == "H":
                    oben = int(name[1]) + 9
                if dest[0] == "H":
                    runter = int(dest[1]) + 9
                else:
                    runter = 14
                matrix[oben][14- runter] = weight
                matrix[runter][14- oben] = weight
        hinton.hinton(matrix)
        # unspruengliche Matrix mit noch zufaelligen Werten anzeigen:
        plt.show()
        # testen ob genug input/output
        output = 0
        input = 0
        for node in graph.get_nodes():
            if node.get_type() == "output":
                output += 1
            if node.get_type() == "input":
                input += 1
        if (output == 0 or input == 0):
            printfenster.insert(END, "Not enough Input/Outputnodes")
        zeichne.draw(graph, "", "")
        return number_nodes
    except:
        error = True
        printfenster.insert(END, "Error\n")
# Eigenschaften        
def properties_ffn():
    global schwellwert
    global hintonnumber
    global alpha
    global alphaffn
    global schwellwertffn
    global hintonnumberffn
    if not error:
        
        def close_and_save():
            global schwellwert
            global hintonnumber
            global alpha
            schwellwert = schwellwertffn.get()
            hintonnumber = hintonnumberffn.get()
            alpha = alphaffn.get()
            properties.destroy()
        properties = Toplevel()
        properties.title("Properties")

        schwellwertlabel = Label(properties, text = "Threshold to stop Algorithm?")
        schwellwertlabel.grid(row = 0, column = 0)
        schwellwertentry = Entry(properties, textvar = schwellwertffn)
        schwellwertentry.grid(row = 0, column = 1)
        hintonlabel = Label(properties, text = "After which iteration do you want the diagram to change?")
        hintonlabel.grid(row = 1, column = 0)
        hintonentry = Entry(properties, textvar = hintonnumberffn)
        hintonentry.grid(row = 1, column = 1)
        alphalabel = Label(properties, text = "Learning rate? ")
        alphalabel.grid(row = 2, column = 0)
        alphaentry = Entry(properties, textvar = alphaffn)
        alphaentry.grid(row = 2, column = 1)
        closebutton = Button(properties, text = "Save and Close", command = close_and_save)
        closebutton.grid(row = 3, column = 1)
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")

# Backpropagation Algorithmus aufrufen
def backpropagation(ex, number_inputnodes, number_hiddennodes):
    global graph
    # backprop. starten! graph wird hinsichtlich der Kantengewichte geaendert!
    if not error:
        graph = importiert[algoindex-1].main(plt, graph, ex, schwellwert,
                                             hintonnumber, alpha,
                                             number_inputnodes,
                                             number_hiddennodes)
        new_window("Done", "Done!")
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")

# eigenes bsp eingeben:
def enterbackprop():
    global ownexample
    if not error:
        global graph
        prop = Toplevel()
    
        def close():
            global ownexample
            try:
                ownexample = []
                # Ausgabe berechnen und anschliessend das Fenster schliessen
                h = [0, 0, 0, 0]
                out = 0
                # inputknoten belegen!
                node0 = graph.get_node("I0")
                node0.set_value(patrons.get())
                ownexample.append(patrons.get())
                node1 = graph.get_node("I1")
                node1.set_value(wait.get())
                ownexample.append(wait.get())
                node2 = graph.get_node("I2")
                node2.set_value(alt.get())
                ownexample.append(alt.get())
                node3 = graph.get_node("I3")
                node3.set_value(hungry.get())
                ownexample.append(hungry.get())
                node4 = graph.get_node("I4")
                node4.set_value(res.get())
                ownexample.append(res.get())
                node5 = graph.get_node("I5")
                node5.set_value(bar.get())
                ownexample.append(bar.get())
                node6 = graph.get_node("I6")
                node6.set_value(fs.get())
                ownexample.append(fs.get())
                node7 = graph.get_node("I7")
                node7.set_value(rain.get())
                ownexample.append(rain.get())
                node8 = graph.get_node("I8")
                node8.set_value(price.get())
                ownexample.append(price.get())
                node9 = graph.get_node("I9")
                node9.set_value(ttype.get())
                ownexample.append(ttype.get())
                # ausgaben berechnen:
                for i in range(10):
                    node = "I" + str(i)
                    node = graph.get_node(node)
                    for edge in node.get_edges():
                        dest = edge.end().name()
                        if dest == "H1":
                            h[0] = h[0] + (edge.weight * node.get_value())
                        elif dest == "H2":
                            h[1] = h[2] + (edge.weight * node.get_value())
                        elif dest == "H3":
                            h[2] = h[2] + (edge.weight * node.get_value())
                        elif dest == "H4":
                            h[3] = h[3] + (edge.weight * node.get_value())
                for j in range(4):
                    neu = "H" + str(j + 1)
                    neu = graph.get_node(neu)
                    hneu = 1 / (1 + math.e ** (-h[j]))
                    neu.set_value(hneu)
                    for edge in neu.get_edges():
                        # keine ueberpruefung, da nur ein outputknoten!
                        out = out + (edge.weight * neu.get_value())
                printfenster.insert(END, "Do I want to wait? \n")
                if out < 0:
                    printfenster.insert(END, "No\n")
                elif out > 0:
                    printfenster.insert(END, "Yes\n")
                else:
                    printfenster.insert(END, "Couldn't decide!\n")
            except:
                printfenster.insert(END, "Every Attribute has to be chosen!\n")
        
        prop.title("Insert Example")
        patrons = IntVar()
        patrons.set(None)
        wait = IntVar()
        alt = IntVar()
        hungry = IntVar()
        res = IntVar()
        bar = IntVar()
        fs = IntVar()
        rain = IntVar()
        price = IntVar()
        price.set(None)
        ttype = IntVar()
        if ownexample != "": 
            patrons.set(ownexample[0])
            wait.set(ownexample[1])
            alt.set(ownexample[2])
            hungry.set(ownexample[3])
            res.set(ownexample[4])
            bar.set(ownexample[5])
            fs.set(ownexample[6])
            rain.set(ownexample[7])
            price.set(ownexample[8])
            ttype.set(ownexample[9])
        label1 = Label(prop, text="Patrons").grid(row=0, column=0)
        Radiobutton(prop, text="None", variable=patrons,
                    value=-1).grid(row=0, column=1)
        Radiobutton(prop, text="Some", variable=patrons,
                    value=0).grid(row=0, column=2)
        Radiobutton(prop, text="Full", variable=patrons,
                    value=1).grid(row=0, column=3)
        label2 = Label(prop, text="Wait Estimate").grid(row=1, column=0)
        Radiobutton(prop, text="0-10", variable=wait,
                    value=1).grid(row=1, column=1)
        Radiobutton(prop, text="10-30", variable=wait,
                    value=0.5).grid(row=1, column=2)
        Radiobutton(prop, text="30-60", variable=wait,
                    value=-0.5).grid(row=1, column=3)
        Radiobutton(prop, text=">60", variable=wait,
                    value=-1).grid(row=1, column=4)
        label3 = Label(prop, text="Alternate").grid(row=2, column=0)
        Radiobutton(prop, text="Yes", variable=alt,
                    value=1).grid(row=2, column=1)
        Radiobutton(prop, text="No", variable=alt,
                    value=-1).grid(row=2, column=2)
        label4 = Label(prop, text="Hungry").grid(row=3, column=0)
        Radiobutton(prop, text="Yes", variable=hungry,
                    value=1).grid(row=3, column=1)
        Radiobutton(prop, text="No", variable=hungry,
                    value=-1).grid(row=3, column=2)
        label5 = Label(prop, text="Reservation").grid(row=4, column=0)
        Radiobutton(prop, text="Yes", variable=res,
                    value=1).grid(row=4, column=1)
        Radiobutton(prop, text="No", variable=res,
                    value=-1).grid(row=4, column=2)
        label6 = Label(prop, text="Bar").grid(row=5, column=0)
        Radiobutton(prop, text="Yes", variable=bar,
                    value=1).grid(row=5, column=1)
        Radiobutton(prop, text="No", variable=bar,
                    value=-1).grid(row=5, column=2)
        label7 = Label(prop, text="Fri/Sat").grid(row=6, column=0)
        Radiobutton(prop, text="Yes", variable=fs,
                    value=1).grid(row=6, column=1)
        Radiobutton(prop, text="No", variable=fs,
                    value=-1).grid(row=6, column=2)
        label8 = Label(prop, text="Raining").grid(row=7, column=0)
        Radiobutton(prop, text="Yes", variable=rain,
                    value=1).grid(row=7, column=1)
        Radiobutton(prop, text="No", variable=rain,
                    value=-1).grid(row=7, column=2)
        label9 = Label(prop, text="Price").grid(row=8, column=0)
        Radiobutton(prop, text="Cheap", variable=price,
                    value=-1).grid(row=8, column=1)
        Radiobutton(prop, text="Okay", variable=price,
                    value=0).grid(row=8, column=2)
        Radiobutton(prop, text="Expensive", variable=price,
                    value=1).grid(row=8, column=3)
        label10 = Label(prop, text="Type").grid(row=9, column=0)
        Radiobutton(prop, text="French", variable=ttype,
                    value=1).grid(row=9, column=1)
        Radiobutton(prop, text="Thai", variable=ttype,
                    value=0.5).grid(row=9, column=2)
        Radiobutton(prop, text="Burger", variable=ttype,
                    value=-0.5).grid(row=9, column=3)
        Radiobutton(prop, text="Italian", variable=ttype,
                    value=-1).grid(row=9, column=4)
        closebutton = Button(prop, text="Decide!",
                             command=close).grid(row=10, column=0)
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


# bayes-netze
def rainbayes():
    global graph
    global bayesrunbutton
    global probtable
    global probslabel
    global probtable
    global probsvar
    global parameterbutton
    global error
    if neu:
        add_clear_and_window()
    else:
        clear_gui()
    probsvar = StringVar(ki)
    probsvar.set("Choose Node")
    probsvar.trace("w", show_prob)  # reagiert, wenn variable sich aendert!
    # buttons etc:
    bayesrunbutton = Button(ki, text="Run", command=load_sampling)
    bayesrunbutton.grid(row=0, column=4)
    probslabel = Label(ki, text="Show Probabilities for: ")
    probslabel.grid(row=0, column=1)
    probtable = OptionMenu(ki, probsvar, "Probabilities")
    probtable.grid(row=0, column=2)
    parameterbutton = Button(ki, text="Properties", command=properties_bayes)
    parameterbutton.grid(row=0, column=3)
    
    folder = os.path.abspath(os.path.dirname("AIMA.py"))
    folder = folder.split("\\aima")[0]
    folder = folder + "\\bayes"
    name = filedialog.askopenfilename(filetypes=[("Bayes files", "*.bayes")], initialdir = (folder))
    try:
        newnodes = []
        datei = open(name).read()
        szenario = []
        for string in datei.split("\n"):
            szenario.append(string)
        namegraph = szenario[0]
        graph = BayesGraph(namegraph, anzeigefenster, printfenster, ki)
        numberofnodes =int(szenario[1])
        for item in range(2, 2+numberofnodes, 1):
            nodewkeit = []
            szenario[item] = szenario[item].split(";")
            nodename = szenario[item][0]
            nodeebene = int(szenario[item][1])
            nodenumberparents = int(szenario[item][2]) # soviele kanten dazu!
            if nodenumberparents > 0:
                nodeparents = szenario[item][3].split()
                table = szenario[item][4]
            else:
                table = szenario[item][3]
            table = table.split(",")
            for line in range(len(table)):
                nodewkeit.append([])
                for el in table[line].split():
                    try:
                        nodewkeit[line].append(float(el))
                    except:
                        el = el.replace('"', '').strip()
                        nodewkeit[line].append(el.replace("+", ", "))
            # das komplementaer dazu:
            for element in range(len(nodewkeit)):
                komp = round(1- float(nodewkeit[element][-1]), 2)
                nodewkeit[element].append(komp)
            newnodes.append(nodename)
            graph.add_node(nodename, nodewkeit, nodeebene)
            # Jetzt die Kanten:
            node = graph.get_node(nodename)
            for kante in range(nodenumberparents):
                graph.add_edge(node.name(), nodeparents[kante])
                graph.add_edge(nodeparents[kante],node.name())
        zeichne.draw(graph, "", "")
        error = False
        probtable['menu'].delete(0, 'end')
        for node in newnodes:
            probtable["menu"].add_command(label=node,
                                       command=tk._setit(probsvar, node))
    except:
        error = True
        printfenster.insert(END, "Error\n")

# Einstellungen bayes:
def properties_bayes():
    global rejection_sam_var
    
    if not error:
        properties = Toplevel()
        properties.title("Properties")
    
        def show_parents():
    
            def close_save():
                # var belgung iwo speichern
                rejection_sam_var[1] = X.get()
                andereKnoten = ""
                for el in range(len(var)):
                    andereKnoten = andereKnoten + var[el].get() + " "
                rejection_sam_var[2] = andereKnoten
                rejection_sam_var[3] = n.get()
                properties.destroy()
    
            var = []
            j = 2
            v = 0
            # für jeden Knoten ausser dem gewaehlten kann ausgesucht werden,
            # wie er sein soll.
            for node in graph.get_nodes():
                if node.name() != X.get():
                    var.append(StringVar())
                    var[v] = StringVar()
                    try:
                        var[v].set(rejection_sam_var[2].split()[v])
                    except:
                        var[v].set("")
                    Radiobutton(properties, text=node.name(), indicatoron = 0,
                                width = 20,variable=var[v],
                                value=node.name()).grid(row=j, column=1)
                    Radiobutton(properties, text= "-" + node.name(),
                                indicatoron = 0, width = 20,
                                variable=var[v],
                                value = "-" + node.name()).grid(row=j, column=2)
                    j += 1
                    v += 1
            closebutton = Button(properties,
                                 text="Close and Save Values", command=close_save)
            closebutton.grid(row=j, column=1)

        n = IntVar()
        n.set(rejection_sam_var[3])
        nlabel = Label(properties,
                       text="How many iterations?").grid(row=0, column=0)
        nEntry = Entry(properties, textvariable=n).grid(row=0, column=1)
    
        sampleLabel = Label(properties, text="Node to sample:")
        sampleLabel.grid(row=1, column=0)
        X = StringVar()
        X.set(rejection_sam_var[1])
        i = 1
        for node in graph.get_nodes():
            Radiobutton(properties, text=node.name(),
                        variable=X, indicatoron = 0,
                        width = 20,value=node.name(),
                        command=show_parents).grid(row=1, column=i)
            i += 1
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


# neues Fenster mit den Knoteneigenen wkeiten oeffnen:
def show_prob(ki, *args):
    global probsvar
    if not error:
        prob = Tk()
        prob.title(probsvar.get())
        node = graph.get_node(probsvar.get())
        probs = node.get_probs()
        for zeilen in range(len(probs)):
            for spalten in range(len(probs[0])):
                label1 = Label(prob, text=node.name())
                label2 = Label(prob, text= "-" + node.name())
                if len(probs[0]) > 2:
                    label1.grid(row=0, column=1)
                    label2.grid(row=0, column=2)
                else:
                    label1.grid(row=0, column=0)
                    label2.grid(row=0, column=1)
                text = probs[zeilen][spalten]
                label3 = Label(prob, text=text)
                label3.grid(row=zeilen + 1, column=spalten)
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


# samplingalgo laufen lassen
def load_sampling():
    # ausgabe wird in algo zurueckgegeben
    if not error:
        rejection_sam_var[0] = graph
        ausgabe = importiert[algoindex-1].main(rejection_sam_var[0], rejection_sam_var[1],
                                     rejection_sam_var[2].split(), rejection_sam_var[3])
        # rejecion gibt Zahlen zurueck
        anzeigefenster.delete("all")
        zeichne.draw(graph, "", "")
        if isinstance(ausgabe[0], float):  # hier ist rejection sampling gelaufen!
            pos = round(ausgabe[0], 3)
            neg = round(ausgabe[1], 3)
            printfenster.insert(END,
                                "P({0}|{1}) = ({2},{3})".format(
                                    rejection_sam_var[1],
                                    rejection_sam_var[2],
                                    pos, neg))
            printfenster.insert(END, "\n")
            # ausgabe der wkeit
            # zeichnen(erfragter wird blau, bedinungen fuer die anderen gruen/rot)
                                    
            #1. blauer Knoten:
            for node in graph.get_nodes():
                if rejection_sam_var[1] == node.name():
                    x = node.get_x_draw()
                    y = node.get_y_draw()
                    zeichne.zeichne_oval(x, y, x+60, y+40, "Lightblue")
                    zeichne.schreibe_text_anzeige(x+7, y+20, node.name())
                # positive Knoten:
                for item in rejection_sam_var[2].split():
                    if item == node.name():
                        #wird gruen!
                        x = node.get_x_draw()
                        y = node.get_y_draw()
                        zeichne.zeichne_oval(x, y, x+60, y+40, "Green")
                        zeichne.schreibe_text_anzeige(x+7, y+20, node.name())
                    if item == "-"+node.name():
                        #wird rot!
                        x = node.get_x_draw()
                        y = node.get_y_draw()
                        zeichne.zeichne_oval(x, y, x+60, y+40, "Red")
                        zeichne.schreibe_text_anzeige(x+7, y+20, node.name())
        else:
            printfenster.insert(END, "Neuer Durchgang: ")
            for el in ausgabe:
                printfenster.insert(END, el)
                printfenster.insert(END, " ")
                for node in graph.get_nodes():
                    if el == node.name():
                        #wird gruen
                        x = node.get_x_draw()
                        y = node.get_y_draw()
                        zeichne.zeichne_oval(x, y, x+60, y+40, "Green")
                        zeichne.schreibe_text_anzeige(x+7, y+20, node.name())
                    elif el == "-" + node.name():
                        x = node.get_x_draw()
                        y = node.get_y_draw()
                        zeichne.zeichne_oval(x, y, x+60, y+40, "Red")
                        zeichne.schreibe_text_anzeige(x+7, y+20, node.name())
                
            printfenster.insert(END, "\n")
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


# fuer entscheidungsbaume:
def decision_features():
    global graph
    global decidebutton
    global decisiontable
    global decisiontree
    global error
    if neu:
        add_clear_and_window()
    else:
        clear_gui()

    # brauche: besipiele und attribute
    examples = []
    attributes = []
    # buttons etc:
    decidebutton = Button(ki, text="Train",
                          command=lambda: run_decision_algo(examples,
                                                            attributes))
    decidebutton.grid(row=0, column=4)
    decisiontable = Button(ki, text="Show Examples",
                           command=lambda: show_examples_table(examples,
                                                               attributes))
    decisiontable.grid(row=0, column=1)
    decisiontree = Button(ki, text="Show Decisiontree",
                          command=lambda: show_decision_tree(graph))
    decisiontree.grid(row=0, column=3)
    # Als Datei die datei mit den Beispielen laden:
    folder = os.path.abspath(os.path.dirname("AIMA.py"))
    folder = folder.split("\\aima")[0]
    folder = folder + "\\decision"
    name = filedialog.askopenfilename(filetypes=[("Feature files", "*.feat")], initialdir = (folder))
    try:
        datei = open(name).read()
        szenario = []
        for string in datei.split("\n"):
            szenario.append(string)
        name = szenario[0]
        attributes = szenario[2].split()
        numberofexamples = int(szenario[3])
        for i in range(numberofexamples):
            examples.append(szenario[i + 4].split())
        error = False
        printfenster.insert(END, "Examples loaded.\n")
    except:
        printfenster.insert(END, "Error\n")
        error = True


def run_decision_algo(examples, attributes):
    global graph
    global sizedec
    global anzeigefenster

    if not error:
        anzeigefenster.delete("all")
        graph = importiert[algoindex-1].main(graph, examples,
                                attributes, "No decision possible!")
        # wie groß ist baum?
        sizedec = zeichne.draw_decision(graph)
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


def show_examples_table(examples, attributes):
    if not error:
        table = Tk()
        table.title("Examples")
        for at in range(len(attributes)):
            label1 = Label(table, text=attributes[at])
            label1.grid(row=0, column=at + 1)
        label1 = Label(table, text="Decision")
        label1.grid(row=0, column=at + 2)
        for ex in range(len(examples)):
            label2 = Label(table, text=ex + 1)
            label2.grid(row=ex + 1, column=0)
            for e in range(len(examples[ex])):
                label3 = Label(table, text=examples[ex][e])
                label3.grid(row=ex + 1, column=e + 1)
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


def show_decision_tree(graph):
    if not error:
        tree = Tk()
        tree.title("Decision Tree")
        xsize = sizedec[0] + 50 
        ysize = sizedec[1] + 50
        treefenster = Canvas(tree, bg="white", height=ysize, width=xsize)
        treefenster.grid()
        zeichne.set_window(treefenster, "tree")
        zeichne.draw_decision(graph)
        zeichne.set_window(anzeigefenster, "anzeige")
    else:
        printfenster.insert(END, "Cannot execute due to previous error!\n")


# Funktionen, die fuer alle Umgebungen gelten:

# was geschieht, wenn ein Algo ausgewählt wurde
# (gilt fuer alle umgebungen gleich)
def filealgo():
    global directory
    global importiert
    global importiertname
    global algomenu
    global importdict
    global algoindex
    global algoindex
    
    def get_index(name):
        global algoindex
        algoindex = importdict[name] +1
        printfenster.insert(END, ">>")
        printfenster.insert(END, name)
        printfenster.insert(END, "\n")
    folder = os.path.abspath(os.path.dirname("AIMA.py"))
    folder = folder.split("\\aima")[0]
    name = filedialog.askopenfilename(filetypes=[("Python files", "*.py")], 
                                                 initialdir=(folder))
    directory = os.path.abspath(os.path.dirname(name))
    sys.path.append(directory)
    name = name.replace(".", "/").split("/")
    name = name[len(name) - 2]
    import importlib
    importiert.append(importlib.import_module(name))
    importiertname.append(name)
    printfenster.insert(END, ">>")
    printfenster.insert(END, name)
    printfenster.insert(END, "\n")
    newimport = {name: algoindex}
    algoindex += 1
    importdict.update(newimport)
    # den namen ans "Load Algo" pull down anhaengen
    algomenu.add_command(label= name, command= lambda : get_index(name))



# entfernt alles, was bisher im printfenster steht:
def clear():
    # einzelne umgebungen:
    global gesetzt
    global noch_da
    global pfad
    pfad = ""
    noch_da = 4
    gesetzt = False
    
    global rejection_sam_var
    rejection_sam_var = [graph, "", "", 20]
    
    global schwellwertffn
    global hintonnumberffn
    global alphaffn
    global ownexample
    ownexample = ""
    schwellwertffn.set(2.5)
    hintonnumberffn.set(20)
    alphaffn.set(0.2)
    
    
    # fuer alle:
    anzeigefenster.delete("all")
    printfenster.delete(1.0, END)
    if not error:
        zeichne.draw(graph, "", "")
        
    umgebung = graph.__class__.__name__
    
    if umgebung == "FFNetwork":
        matrix = np.empty([15, 15])  # fuer hinton diagramm
        #kantengewichte wieder zufaellig machen!
        for node in graph.get_nodes():
            for edge in node.get_edges():
                weight = random.randint(0, 100) / 100
                edge.set_weight(weight)
            # matrix fuellen:
        for zeile in range(15):
            for spalte in range(15):
                matrix[zeile][spalte] = 0
        for node in graph.get_nodes():
            name = node.name()
            for edge in node.get_edges():
                dest = edge.end().name()
                weight = edge.weight
                # ueberpruefung worein es geschireben wird:
                if name[0] == "I":
                    oben = int(name[1])
                elif name[0] == "H":
                    oben = int(name[1]) + 9
                if dest[0] == "H":
                    runter = int(dest[1]) + 9
                else:
                    runter = 14
                matrix[oben][14- runter] = weight
                matrix[runter][14- oben] = weight
        hinton.hinton(matrix)


# erstellt neues Fenster, das nach 4 Sekunden
# wieder geschlossen wird. (Zb. für Fehlermeldungen)
def new_window(title, nachricht):
    window = Tk()
    window.geometry("350x50")
    window.title(title)
    label = Label(window, text=nachricht).pack()
    window.after(4000, lambda: window.destroy())


def clear_gui():
    global graph
    global startm
    global goalm
    global startlabel
    global goallabel
    global runbutton
    global zerobutton
    global onebutton
    global twobutton
    global probtable
    global backprob
    global probslabel
    global parameterbutton
    global bayesrunbutton
    global probtable
    global examplebutton
    global decidebutton
    global decisiontable
    global decisiontree
    global backproperties
    global algomenu
    global algoindex
    global importdict
    global importiert
    global rejection_sam_var
    global schwellwertffn
    global hintonnumberffn
    global alphaffn

    # falls vorher spiel:
    if zerobutton != "":
        zerobutton.destroy()
        onebutton.destroy()
        twobutton.destroy()
    # falls vorher routenplanung
    if startm != "":
        startm.destroy()
        goalm.destroy()
        runbutton.destroy()
        startlabel.destroy()
        goallabel.destroy()
    # falls vorher ffn
    if backprob != "":
        backprob.destroy()
        backproperties.destroy()
        examplebutton.destroy()
        schwellwertffn.set(2.5)
        hintonnumberffn.set(20)
        alphaffn.set(0.2)
    # falls vorher bayes:
    if bayesrunbutton != "":
        bayesrunbutton.destroy()
        probslabel.destroy()
        probtable.destroy()
        parameterbutton.destroy()
        rejection_sam_var = [graph, "", "", 20] 
        # falls nachher noch ein durchgang
    # falls vorher decide:
    if decidebutton != "":
        decidebutton.destroy()
        decisiontable.destroy()
        decisiontree.destroy()
    # im printfesnter alles loeschen:
    printfenster.delete(1.0, END)
    anzeigefenster.delete("all")
    importdict.clear()
    algoindex = 0
    importdict = {}
    importiert = []
    algomenu.delete(0, END)
    algomenu.add_command(label="Load", command=filealgo)
    algomenu.add_separator()
    
    
def quit_aima():
    ki.destroy()

# Menueleiste mit Load scenario und load algo:
menubar = Menu(ki)
ki.config(menu=menubar)

scenariomenu = Menu(menubar)
menubar.add_cascade(label="Select Application", menu=scenariomenu)

submen = Menu(scenariomenu)
submen.add_command(label="Open Map", command=routefinding)
scenariomenu.add_cascade(label="Routefinding", menu=submen)

submenu = Menu(scenariomenu)
submenu.add_command(label="Matches", command=match_game)
scenariomenu.add_cascade(label="Play Game", menu=submenu)

submenu3 = Menu(scenariomenu)
submenu3.add_command(label="Open Bayesian Networks",
                     command=rainbayes)
scenariomenu.add_cascade(label="Bayesian Network", menu=submenu3)

submenu4 = Menu(scenariomenu)
submenu4.add_command(label="Open Features", command=decision_features)
scenariomenu.add_cascade(label="Decision Trees", menu=submenu4)

submenu2 = Menu(scenariomenu)
submenu2.add_command(label="Open Features",
                     command=restaurantffn)
scenariomenu.add_cascade(label="Feed-Forward-Networks", menu=submenu2)

algomenu = Menu(menubar)
menubar.add_cascade(label="Load algorithm", menu=algomenu)
algomenu.add_command(label="Load", command=filealgo)
algomenu.add_separator()

settingsmenu = Menu(menubar)
menubar.add_command(label="Quit", command=quit_aima)


def add_clear_and_window():
    global printfenster
    global anzeigefenster
    global neu
    clearbutton = Button(ki, text="Clear", command=clear)
    clearbutton.grid(row=0, column=6)

    # Anzeigefenster
    frameanzeige = Frame(ki, width=410, height=410, bd=2, relief=RAISED)
    frameanzeige.grid(row=1, column=0, columnspan=6, rowspan=5)
    frameprint = Frame(ki, width=210, height=410, bd=2, relief=RAISED)
    frameprint.grid(row=1, column=6, columnspan=3, rowspan=6)
    anzeigefenster = Canvas(frameanzeige, bg="white", width=400, height=400)
    anzeigefenster.grid(row=1, column=0, columnspan=6, rowspan=5)
    printfenster = Text(frameprint, width=40, height=25)
    printfenster.grid(row=0, column=6)
    vbar = Scrollbar(frameprint)
    vbar.grid(row=0, column=7, rowspan=6, sticky=N + S)
    vbar.config(command=printfenster.yview)

    zeichne.set_window(anzeigefenster, "anzeige")
    neu = False


ki.mainloop()
