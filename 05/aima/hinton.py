# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""

import matplotlib.patches as mpatches
import pylab as p
import numpy as n
 
def _add_centered_square(ax, xy, area, **kwargs):
    size = n.sqrt(area)
    loc = n.asarray(xy) - size/2.
    rect = mpatches.Rectangle(loc, size, size, **kwargs)
    ax.add_patch(rect)


def normalize_values(a):
    sum = 0
    for xy, val in n.ndenumerate(a):
        sum += abs(val)
    if any(val > 1 for xy, val in n.ndenumerate(a)):
        for xy, val in n.ndenumerate(a):
            a[xy] = float(val/sum)*10  # da es sonst zu klein ist.
    return a
    
    
 
def hinton(a, ax=None):
    """
    Draw a Hinton diagram for the 2D array `a` on the axes.

    Elements of `a` should range between -1 and 1. Each element will
    be represented by a square which is white for positive values, or
    black for negative values, with an area proportional to its
    magnitude.

    """
    a = normalize_values(a)
    p.clf()
    if ax is None:
        ax = p.gca()
    ax.patch.set_facecolor('gray')
    # gibt position des Elements, val des Elements
    for xy, val in n.ndenumerate(a):
        color = 'white' if val > 0 else 'black'
        _add_centered_square(ax, n.asarray(xy),  # asarray: convert input in array
                             abs(val), color=color)
        # parameter: ax = , n.asarray(xy)= an stelle, an der es hin soll.
    
    ax.autoscale_view()
    ax.set_xlabel("from: 0 = I1, 1 = I2, ... 9 = I10,10 = H1,13 = H4, 14 = O")
    ax.set_ylabel("to: 0 = O, 1 = H4, 4 = H1, 5 = I10, ... 14 = I1")