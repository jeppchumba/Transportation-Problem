#!/usr/bin/python

import os
import math
#import heapq #needed if we want to use a priority queue
import graph
import tkinter as tk


class TownGraph:

    def __init__(self,num_vertices):

        self.__graph_vertices=[graph.Graph(vertex_name=i+1) for i in range(num_vertices)]
        self.path_str=None

        self.__dict1 = {} #to save routes
        self.__dict5 = {} #to save routes
        self.__dict1["routes"] = []
        self.__dict5["routes"] = []
        self.count=0

        #constant dictionary mapping each vertex number to the name of a town
        #change if the number of vertices changes
        self.__vertex_map=[
                            "None",
                            "Nakuru",
                            "Thika",
                            "Kisumu",
                            "Nairobi",
                            "Garissa",
                            "Mombasa",
                            "Malindi"
                            ]
        self.__idx_map={
                "Nakuru":1,
                "Thika":2,
                "Kisumu":3,
                "Nairobi":4,
                "Garissa":5,
                "Mombasa":6,
                "Malindi":7
                }

    def mapVertexIndex(self,vertex_name:str):
        return self.__idx_map[vertex_name]


    def getGraphVertices(self):
        return self.__graph_vertices

    def addEdge(self,v:graph.Graph,adj_v:graph.Graph,cost:int):
        #where v is a vertex and adj_v is the corresponding adjacent vertex 
        #cost is basically the distance or whatever
        self.__graph_vertices[v-1].addAdjacentVertex(vertex=self.__graph_vertices[adj_v-1],cost=cost)

    def createGraph(self):
        #basically adding edges and their costs
        #this is doing it manually

       # Test digraph
       # self.addEdge(v=1,adj_v=2,cost=2)
       # self.addEdge(1,4,1)
       # self.addEdge(2,4,3)
       # self.addEdge(2,5,10)
       # self.addEdge(3,1,4)
       # self.addEdge(3,6,5)
       # self.addEdge(4,3,2)
       # self.addEdge(4,5,2)
       # self.addEdge(4,6,8)
       # self.addEdge(4,7,4)
       # self.addEdge(5,7,6)
       # self.addEdge(7,6,1)

       #town graph
       self.addEdge(v=1,adj_v=2,cost=166)
       self.addEdge(1,3,185)
       self.addEdge(1,4,166)
       self.addEdge(1,5,495)
       #self.addEdge(2,1,166)
       self.addEdge(2,4,45)
       self.addEdge(2,5,322)
       self.addEdge(3,1,185)
       self.addEdge(3,4,346)
       #self.addEdge(3,6,829)
       self.addEdge(4,1,166)
       self.addEdge(4,2,45)
       self.addEdge(4,3,346)
       self.addEdge(4,5,373)
       self.addEdge(4,6,490)
       #self.addEdge(4,7,466)
       self.addEdge(5,1,495)
       self.addEdge(5,2,322)
       self.addEdge(5,4,373)
       self.addEdge(5,7,347)
       #self.addEdge(6,3,829)
       self.addEdge(6,4,490)
       self.addEdge(6,7,115)
       #self.addEdge(7,4,466)
       self.addEdge(7,5,347)
       self.addEdge(7,6,115)

    def setStartVertex(self,vertex_idx):
        self.__start_vertex=self.__graph_vertices[vertex_idx]


    def setSentinel(self):
        for vertex in self.__graph_vertices:
            vertex.distance=math.inf
            vertex.known=False
            vertex.path=None

    def findMinimumVertex(self):
        #best would be to use a priority queue
        #but using a priority queue is a bit complicated
        cost=math.inf
        mcv=None #minimum cost vertex

        for vertex in self.__graph_vertices:
            if vertex.distance<cost and not vertex.known:
                cost=vertex.distance
                mcv=vertex

        return mcv
    
    def printPath(self,vertex,path_str=None):

        if vertex.path:
            self.printPath(vertex.path)
            if self.path_str is not None: 
                self.path_str+=" to "
            print(" to",end=" ")

        if self.path_str is not None: self.path_str+=self.__vertex_map[vertex.getVertexName()]

        print(self.__vertex_map[vertex.getVertexName()],end="")

    def print_Path(self,distance_var:tk.StringVar=None,path_var:tk.StringVar=None):
        self.path_str=""
        print("Prints the path and their costs from all vertices to the source")
        print("V-vertex, D-distance/cost, P-Path")


        for vertex in self.__graph_vertices:
            self.path_str=""
            print("V:%s (%s) D:%d P:("%(vertex,self.__vertex_map[vertex.getVertexName()],vertex.distance),end="")
            self.printPath(vertex)
            print(")")
            
            distance_var.set("Distance: %d"%(vertex.distance))
            path_var.set("Path: "+self.path_str)

    def printDestinationPath(self,destination_str_name,distance_var:tk.StringVar=None,path_var:tk.StringVar=None):
        self.path_str=""
        destination_vertex = self.__graph_vertices[self.__idx_map[destination_str_name]-1]

        print("V:%s (%s) D:%d Path:("%(destination_vertex,self.__vertex_map[destination_vertex.getVertexName()],destination_vertex.distance),end="")
        self.printPath(destination_vertex)
        print(")")

        # distance_var.set("Distance: %d"%(destination_vertex.distance))
        # path_var.set("Path: "+self.path_str)

        self.count += 1
        x = {
                "id": self.count,
                "path": str(self.path_str).split(" to "),
                "path2": str(self.path_str),
                "dist": destination_vertex.distance
            }
        self.__dict1["routes"].append(x)

        

    def hello(self):
        return self.__dict1["routes"]
        

    def showPath(self):
        v=None

        print("The path are from the vertex with cost=0")
        print("v-vertex,d-distance from vertex with cost=0,p-pah to vertex with cost 0")


        for i,vertex in enumerate(self.__graph_vertices):
            v=vertex.path

            if v==None:
                print("v=%d d=%d p=already there"%(i+1,vertex.distance))
            else: 
                print("v=%d d=%d p=%s"%(i+1,vertex.distance,v))

    def breadthFirstSearch(self):
        #for breadth first search we use a queue
        #using python list basically append and then use pop(index=0)


        queue=list()

        self.setSentinel()

        self.__start_vertex.distance=0
        queue.append(self.__start_vertex)

        while len(queue)>0:
            vertex=queue.pop(0)

            for adjacent_vertex_tuple in vertex.getAdjacentVertex():
                adjacent_vertex=adjacent_vertex_tuple[0]
                edge_cost=adjacent_vertex_tuple[1]
                if adjacent_vertex.distance==math.inf:
                    adjacent_vertex.distance=vertex.distance+edge_cost
                    adjacent_vertex.path=vertex
                    queue.append(adjacent_vertex)

    def depthFirstSearch(self):
        #for depth first search we use a stack
        #using python list basically append and then use pop()

        stack=list()

        self.setSentinel()

        self.__start_vertex.distance=0
        stack.append(self.__start_vertex)

        while len(stack)>0:
            vertex=stack.pop()

            for adjacent_vertex_tuple in vertex.getAdjacentVertex():
                adjacent_vertex=adjacent_vertex_tuple[0]
                edge_cost=adjacent_vertex_tuple[1]
                if adjacent_vertex.distance==math.inf:
                    adjacent_vertex.distance=vertex.distance+edge_cost
                    adjacent_vertex.path=vertex
                    stack.append(adjacent_vertex)

    #A* search which uses the same concept of uniform cost search is basically the dijkstra_algorithm
    def AStarSearch(self):
        num_vertices=len(self.__graph_vertices)
        no_unknowns=num_vertices

        self.setSentinel()

        self.__start_vertex.distance=0

        while no_unknowns:
            mcv=self.findMinimumVertex()
            mcv.known=True
            no_unknowns-=1

            for adjacent_vertex_tuple in mcv.getAdjacentVertex():
                adjacent_vertex=adjacent_vertex_tuple[0]

                if not adjacent_vertex.known:
                    #cost of edge (mcv,adjacent_vertex)
                    cost_mcv_adjacent_vertex=adjacent_vertex_tuple[1]

                    if (mcv.distance+cost_mcv_adjacent_vertex<adjacent_vertex.distance):
                        adjacent_vertex.distance=mcv.distance+cost_mcv_adjacent_vertex
                        adjacent_vertex.path=mcv
    
    def printGraph(self):

        for vertex in self.__graph_vertices:
            print(vertex,"--------------->",end=" ")
            vertex.showAdjacentVertices()

    




if __name__=="__main__":
    print("Enter the number of vertices: ",end="")
    n=int(input())

    town_graph=TownGraph(num_vertices=n)
    vertices=town_graph.getGraphVertices()

    for vertex in town_graph.getGraphVertices():
        while True:
            print("Enter the vertices adjacent to ",vertex," -1 to quit")
            vert=int(input())

            if vert==-1:
                break

            print("Enter the cost associated with the edge (%s,%d): "%(vertex,vert),end="")
            cost=int(input())

            vertex.addAdjacentVertex(vertex=vertices[vert-1],cost=cost)

    os.system("clear")

    print("Vertex ...............> adjacent vertices")

    town_graph.printGraph()

    town_graph.setStartVertex(0)
    print("using breadth first search algorithm")
    town_graph.breadthFirstSearch()
    town_graph.print_Path()

    print("using depth first search algorithm")
    town_graph.depthFirstSearch()
    town_graph.print_Path()

    print("using A* Search")
    town_graph.AStarSearch()
    town_graph.print_Path()
