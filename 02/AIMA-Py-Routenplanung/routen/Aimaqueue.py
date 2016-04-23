# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:14:45 2015

@author: EG
"""

#Aimaqueue.py V. 150417

class Queue():
    def __init__(self):
        self.elements = []

    def put(self, new_element):
        self.elements.append(new_element)

    def empty(self):
        if len(self.elements) == 0:
            return True
        else:
            return False


class FiFoQueue(Queue):
    def __init__(self):
        Queue.__init__(self)

    def put(self, new_element):
        Queue.put(self, new_element)

    def get(self):
        return (self.elements.pop(0))

    def empty(self):
        Queue.empty(self)


class LiFoQueue(Queue):
    def __init__(self):
        Queue.__init__(self)

    def put(self, new_element):
        Queue.put(self, new_element)

    def get(self):
        return (self.elements[-1])

    def empty(self):
        Queue.empty(self)


class SortedQueue(Queue):
    def __init__(self):
        Queue.__init__(self)

    def put(self, new_element):
        Queue.put(self, new_element)

    def get(self):
# your code
# your code
# your code
# your code
# your code
# your code
        return() #your return argument

    def empty(self):
        Queue.empty(self)
