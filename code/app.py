#!/usr/bin/python2
# -*- coding: iso-8859-1 -*-
import numpy as np
import matplotlib
import psycopg2
import math
from connect import connect
import networkx as nx
import matplotlib.pyplot as plt
gX = connect()
cur = gX.cur

matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from Tkinter import *
import Tkinter as Tk
import sys

class simpleapp_tk(Tk.Tk):
    def __init__(self,parent):
        Tk.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()



    def get_graph():
        query = "select * from testedges"
        cur.execute(query)
        G=nx.Graph()
        position={}
        edgelist = cur.fetchall()
        G.add_weighted_edges_from(edgelist)

        #pos=nx.spring_layout(G)
        query = "select cluster_id from clusters"
        cur.execute(query)
        value = cur.fetchall()
        values =[val[0] for val in value]
        print values,G.nodes()
        query = "select node_id from clusters"
        cur.execute(query)
        l_values = cur.fetchall()
        for i in range(0,len(l_values)):
            position[l_values[i][0]] = ((-1)^(values[i]%3)*10*values[i]*int(100*np.random.random())+i*10,((-1)^(values[i]%4)*10*values[i]*int(100*np.random.random())))

        nx.draw(G, position, ax=a, node_label = l_values, cmap=plt.get_cmap('jet'), node_color=values)
    
        return nx

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('my application')
    app.mainloop()
