#!/usr/bin/python

import tkinter as tk
from tkinter import Canvas, ttk
from tkinter.constants import Y
from PIL import Image,ImageTk

import towns_graph as tg



class GUI:
    

    def configureRootWindow(self):
        self.__root_window.geometry("750x400")

    def __init__(self):

        self.__root_window=tk.Tk()
        self.configureRootWindow()
        
        self.__root_window.title("Optimal Path")

        self.__main_frame=tk.Frame(self.__root_window)
        self.__info_frame=tk.Frame(self.__main_frame)

        self.__town_graph=tg.TownGraph(num_vertices=7)
        self.__town_graph.createGraph()
        self.__town_graph.printGraph()

        self.createGui()
      
        self.__main_frame.pack(fill='x', expand=False)
        self.__main_frame.columnconfigure(10, weight=1)
        self.__main_frame.rowconfigure(0, weight=1)

        self.__info_frame.place(x=600,y=55)
        # self.__info_frame.grid(row=0, column=0, pady=1)
        self.__main_frame.grid()
        
        self.searchtype = None #our global search variable
        self.startpt = None #our global startpoint variable
        self.endpt = None #our global endpoint variable

        self.__root_window.mainloop()
     

    def createGui(self,pin_start_end=None,new_path=None,new_distance=None,search=None,start=None,end=None):
        ################################################################################
        #using tk.canvas instead, more items

        img_path = 'provinces.png'
        self.__img = ImageTk.PhotoImage(Image.open(img_path).resize((350,350)))
        
        self.__newcanvas = tk.Canvas(self.__main_frame,width=700,height=400,)
        newimg = self.__newcanvas.create_image(200, 200, image=self.__img)

        ########### pins
        self.__newcanvas.create_oval(155, 240, 165, 250,fill="blue") #nairobi
        self.__newcanvas.create_oval(165, 220, 175, 230,fill="blue") #thika
        self.__newcanvas.create_oval(125, 210, 135, 220,fill="blue") #nakuru
        self.__newcanvas.create_oval(65, 200, 75, 210,fill="blue") #kisumu
        self.__newcanvas.create_oval(265, 200, 275, 210,fill="blue") #Garissa
        self.__newcanvas.create_oval(265, 335, 275, 345,fill="blue") #Mombasa
        self.__newcanvas.create_oval(280, 305, 290, 315,fill="blue") #Malindi

            #draw the connecting lines
        if pin_start_end is not None:
            line = self.__newcanvas.create_line(pin_start_end, fill="purple", width=4)

            # position order
            self.__newcanvas.tag_lower(line)
            self.__newcanvas.tag_lower(newimg)
            # 

        self.__newcanvas.create_text(505,50,text="Start : ",font=('Helvetica','10','bold'))
        self.__newcanvas.create_text(500,80,text="Destination:\nCity",font=('Helvetica','10','bold'))


        #comboboxes for selecting the start town and the destination town
        self.start_options = ["Nairobi","Nakuru","Garissa","Mombasa","Kisumu","Thika","Malindi"]
        self.end_options = ["Nairobi","Nakuru","Garissa","Mombasa","Kisumu","Thika","Malindi"]
        
        # Variable to keep track of the option selected in OptionMenu
        self.__start_town_var = tk.StringVar()
        self.__target_town_var = tk.StringVar()

        # Set the default value of the variable (variables in __init__ )
        if start == None:
            self.__start_town_var.set("Start Point")        
            self.__target_town_var.set("End Point")
        else:
            self.__start_town_var.set(start)        
            self.__target_town_var.set(end)

        self.__start_town1 =tk.OptionMenu(self.__main_frame, self.__start_town_var, *self.start_options)
        self.__end_town2 =tk.OptionMenu(self.__main_frame, self.__target_town_var, *self.end_options)
        
        self.__start_town1.configure(textvariable=self.__start_town_var,width=15,)
        self.__end_town2.configure(textvariable=self.__target_town_var,width=15)

        self.__start_town1.place(x=550,y=35)
        self.__end_town2.place(x=550,y=65)
        

        # search choices
        self.__bfs_btn1=ttk.Button(self.__main_frame,text="BFS",width=10,command=lambda: self.searchAlgorithm(algorithm="BFS"))
        self.__dfs_btn1=ttk.Button(self.__main_frame,text="DFS",width=10,command=lambda: self.searchAlgorithm(algorithm="DFS"))
        self.__a_search1=ttk.Button(self.__main_frame,text="A*S",width=10,command=lambda: self.searchAlgorithm(algorithm="A*S"))
        self.__bfs_btn1.place(x=450,y=150)
        self.__dfs_btn1.place(x=535,y=150)
        self.__a_search1.place(x=620,y=150)


        ##########################################################################################

        #clear button,
        self.__clear_btn=ttk.Button(self.__main_frame,text="Clear/Reset",
        command=lambda: self.createGui(pin_start_end=None,new_path=None,new_distance=None,search=None,start=None,end=None)) 

        #display distance and path and search type
        self.__newcanvas.create_text(540,190,text=search,font=('Helvetica','9'))
        self.__newcanvas.create_text(490,220,text=new_distance,font=('Helvetica','10','bold'))
        self.__newcanvas.create_text(550,240,text=new_path,font=('Helvetica','9','bold'))
        

        #############################################################
        # canvas positioning
        self.__clear_btn.place(x=610,y=300)
        self.__newcanvas.grid(row=1,column=0)




    def searchAlgorithm(self,algorithm):
        self.__town_graph.setStartVertex(vertex_idx=(self.__town_graph.mapVertexIndex(self.__start_town_var.get()))-1)
        self.startpt = self.__start_town_var.get() 
        self.endpt = self.__target_town_var.get()

        if algorithm=="BFS":
            #self.searchtype = "*Breadth First Search is NOT Optimal"
            print("Using BFS")
            self.__town_graph.breadthFirstSearch()
        elif algorithm=="DFS":
            #self.searchtype = "*Depth First Search is NOT Optimal"
            print("Using DFS")
            self.__town_graph.depthFirstSearch()
        elif algorithm=="A*S":
            #self.searchtype = "*A-Star Search is most optimal"
            print("Using A*S")
            self.__town_graph.AStarSearch()
        else:
            print("Algorithm not implemented")
            return

       # self.__distance_var.set("Distance: 700")
       # self.__path_var.set("Path: Nairobi to Mombasa to Lamu to Kisumu to Nyeri to Nairobi to Mombasa")

        # self.__town_graph.print_Path(self.__distance_var,self.__path_var)
        # print("start: "+ self.__start)
        # print("target: "+ self.__end)
        self.__town_graph.printDestinationPath(self.endpt)
        self.Get_routes()

    def Get_routes(self):
        self.__routes = self.__town_graph.hello() #added to pick vertices

        pin_start = [0,0]
        pin_location = [0,0]
        pin_end = [0,0]
        new_path = None
        new_distance = None

        self.__dict2 = {} #to save routes
        self.__dict2["routes"] = []
        self.__dict2["routes"] = self.__routes
        for p in self.__dict2["routes"]:
                pin_start.clear()
                pin_location.clear()
                pin_end.clear()

                new_path = p["path2"]
                new_distance = p["dist"]

                # start cordinates
                if str(p['path'][0]) == "Nakuru": pin_start.append(131), pin_start.append(215)
                elif str(p['path'][0]) == "Thika": pin_start.append(171), pin_start.append(225)
                elif str(p['path'][0]) == "Kisumu": pin_start.append(71), pin_start.append(205)
                elif str(p['path'][0]) == "Nairobi": pin_start.append(161), pin_start.append(245)
                elif str(p['path'][0]) == "Garissa": pin_start.append(271), pin_start.append(205)
                elif str(p['path'][0]) == "Mombasa": pin_start.append(271), pin_start.append(341)
                elif str(p['path'][0]) == "Malindi": pin_start.append(285), pin_start.append(310)

                if len(p["path"]) >= 2:
                    if str(p['path'][1]) == "Nakuru": pin_end.append(131), pin_end.append(215)
                    elif str(p['path'][1]) == "Thika": pin_end.append(171), pin_end.append(225)
                    elif str(p['path'][1]) == "Kisumu": pin_end.append(71), pin_end.append(205)
                    elif str(p['path'][1]) == "Nairobi": pin_end.append(161), pin_end.append(245)
                    elif str(p['path'][1]) == "Garissa": pin_end.append(271), pin_end.append(205)
                    elif str(p['path'][1]) == "Mombasa": pin_end.append(271), pin_end.append(341)
                    elif str(p['path'][1]) == "Malindi": pin_end.append(285), pin_end.append(310)

                if len(p["path"]) >= 3:
                    if str(p['path'][2]) == "Nakuru": pin_end.append(131), pin_end.append(215)
                    elif str(p['path'][2]) == "Thika": pin_end.append(171), pin_end.append(225)
                    elif str(p['path'][2]) == "Kisumu": pin_end.append(71), pin_end.append(205)
                    elif str(p['path'][2]) == "Nairobi": pin_end.append(161), pin_end.append(245)
                    elif str(p['path'][2]) == "Garissa": pin_end.append(271), pin_end.append(205)
                    elif str(p['path'][2]) == "Mombasa": pin_end.append(271), pin_end.append(341)
                    elif str(p['path'][2]) == "Malindi": pin_end.append(285), pin_end.append(310)

                # end cordinates
                if str(p['path'][-1]) == "Nakuru": pin_end.append(131), pin_end.append(215)
                elif str(p['path'][-1]) == "Thika": pin_end.append(171), pin_end.append(225)
                elif str(p['path'][-1]) == "Kisumu": pin_end.append(71), pin_end.append(205)
                elif str(p['path'][-1]) == "Nairobi": pin_end.append(161), pin_end.append(245)
                elif str(p['path'][-1]) == "Garissa": pin_end.append(271), pin_end.append(205)
                elif str(p['path'][-1]) == "Mombasa": pin_end.append(271), pin_end.append(341)
                elif str(p['path'][-1]) == "Malindi": pin_end.append(285), pin_end.append(310)

                

        # print(self.__routes)
        pin_start_end = pin_start + pin_end
        new_path = "Path: From " + str(new_path)
        new_distance = "Distance: " + str(new_distance)
        # print(new_path)
        # print(new_distance)
        search = self.searchtype
        start = self.startpt
        end = self.endpt
        self.searchtype=None
        self.startpt=None
        self.endpt=None
        # print("v1: " + str(pin_start_end))
        self.createGui(pin_start_end,new_path,new_distance,search,start,end)
          
GUI()