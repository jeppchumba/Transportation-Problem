#!/usr/bin/python

import os
import math
import heapq


class Graph:

    def __init__(self,vertex_name):

        self.__adjacent_vertices=list()
        self.__vertex_name=vertex_name

        #set to infinity as the sentinel
        self.distance=math.inf
        self.known=False
        self.path=None

    def getAdjacentVertex(self):
        return self.__adjacent_vertices

    def getVertexName(self):
        return self.__vertex_name

    def addAdjacentVertex(self,vertex,cost=0):
        self.__adjacent_vertices.append((vertex,cost))

    def showAdjacentVertices(self):

        for adjacent_vertex in self.__adjacent_vertices:
            print(adjacent_vertex[0],end=",")

        print()

    def __str__(self):
        return str(self.__vertex_name)

    def __lt__(self,other):
        return self.distance < other.distance
