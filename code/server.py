#!/usr/bin/python2
import numpy as np
import matplotlib
import psycopg2
import math
from connect import connect
from abstract import abstract
import networkx as nx
import matplotlib.pyplot as plt
from kmeans import cluster_all
from clearC import clearCluster
gX = connect()
cur = gX.cur
from clear import clearTemp
from pic import *
from ttk import *
matplotlib.use('TkAgg')

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from Tkinter import *
import Tkinter as Tk
import ttk
import sys
from extra import degree
#from Tkinter import *

G=nx.Graph()
kmeans = 0
stat={"Min. Degree ":0, "Max. Degree":0, "Average Degree":0, "Deviation Degree":0}
class MyDialog:

    def __init__(self, parent):

        top = self.top = Toplevel(parent)
        Label(top, text="Number of Cluster").pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        kmeans = self.e.get()
        clearCluster()
        clearTemp()
        power(0.0000001)
        cluster_all(kmeans)
        print"Done Clustering"
        self.top.destroy()


def destroy(e): sys.exit()

def get_degree():
    deg = degree()
    stat['Min. Degree '] = deg[0]
    stat['Max. Degree'] = deg[1]
    stat['Average Degree'] = deg[2]
    stat['Deviation Degree'] = deg[3]
    listbox.delete(0,END)
    listbox.insert(END, "Graph Degre Statistics")
    listbox.insert(END, "======================")
    for item in ["Min. Degree ", "Max. Degree", "Average Degree", "Deviation Degree"]:
        listbox.insert(END, item+" : "+str(stat[item]))
        print item

def get_abstract():
    data = abstract()
    print(data)
    #G.clear()
    weights = np.asarray([tupl[2] for tupl in data])
    weights[weights<14] = 0
    G.add_weighted_edges_from(data)
    post =nx.random_layout(G)
    nx.draw_networkx(G, pos=post, ax=a,with_labels=True)
    
def clear_graph():
    G.clear()
    a.clear()
def get_graph():
    query = "select * from testedges"
    cur.execute(query)
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
    nx.draw(G,  ax=a, node_label = l_values, with_labels=True, font_size=8,cmap=plt.get_cmap('jet'), node_color=values)

def do_pic():
    print "About to be Cleared"
    clearTemp()
    thresh = 0.000001
    print "Cleared"
    listbox.delete(4)
    iter_n = power(thresh)
    listbox.insert(END,"PIC Iteration :"+str(iter_n))

if __name__ == '__main__':
    root = Tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    style = ttk.Style()
    def hello():
        print "hello!"
    
    f = Figure(figsize=(5,4), dpi=100)
    a = f.add_subplot(111)

    #root.bind("<Destroy>", destroy)
    m1 = PanedWindow()
    m1.pack(fill=BOTH, expand=1,side='left')
   

    canvas = FigureCanvasTkAgg(f, master=m1)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    menubar = Menu(root)
    filemenu = Menu(menubar)
    compmenu = Menu(menubar)
    statmenu = Menu(menubar)
    clustmenu = Menu(menubar)
    menubar.add_cascade(label="File",menu=clustmenu)
    menubar.add_cascade(label="Cluster",menu=clustmenu)
    menubar.add_cascade(label="Compute",menu=compmenu)
    menubar.add_cascade(label="Statistics",menu=statmenu)
    statmenu.add_command(label="Degree Statistics",command=get_degree)
    clustmenu.add_command(label="Total Cluster",command=get_graph)
    clustmenu.add_command(label="Abstract Cluster",command=get_abstract)
    clustmenu.add_command(label="Clear Cluster",command=clear_graph)
    compmenu.add_command(label="Do PIC",command=do_pic)
    root.config(menu=menubar)
    
    toolbar = NavigationToolbar2TkAgg( canvas, root )
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
    m2 = PanedWindow()
    m1.add(m2)
    m2.pack(fill=None, expand=0,side='top')
    listbox = Listbox(master=m2,height = 20)
    listbox.pack()

    listbox.insert(END, "Graph Degre Statistics")
    listbox.insert(END, "======================")

    for item in ["Min. Degree ", "Max. Degree", "Average Degree", "Deviation Degree"]:
        listbox.insert(END, item+" : "+str(stat[item]))
        print stat

    separator = Frame(height=2, bd=1, relief=SUNKEN,master=m2)
    separator.pack(fill=Tk.X, padx=1, pady=1)
    '''
    e = Entry(m2)
    e.pack()

    e.focus_set()

    def ecallback():
        print e.get()

    b = Button(m2, text="get", width=10, command=ecallback)
    b.pack()'''
    button = MyDialog(root)
    button = Tk.Button(master=m2, text='Quit', command=sys.exit)
    button.pack(side=Tk.BOTTOM)
    
    Tk.mainloop()
