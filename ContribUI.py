import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import matplotlib
matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import numpy as np
import re

from sys import platform
import os

class ContribUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

    def initialize(self, data_manager):
        container = tk.Frame(self)
        self.geometry('1150x650')
        container.pack(fill=tk.BOTH,expand=True)

        self.frames = {}
        self.frames[StartPage] = StartPage(container,self, data_manager)
        self.frames[StartPage].grid(row=0,column=0,sticky='nsew')

        self.show_frame(StartPage)
        

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()


class StartPage(tk.Frame):
    
    #The data manager
    data_manager = None
    
    #Canvases for both top contributor and single contributor graphs.
    top_contrib_label_text = None
    top_contrib_label = None    
    top_contrib_figure = None
    top_contrib_ax = None
    top_contrib_canvas = None

    single_contrib_label_text = None
    single_contrib_label = None
    single_contrib_figure = None
    single_contrib_ax = None
    single_contrib_canvas = None

    #Repository Names label and text box.
    rep_label_text = None
    rep_label = None
    rep_text_text = None
    rep_text_box = None

    #List contributors label, input, and go button
    contrib_label_text = None
    contrib_label = None
    contrib_name_text_box = None
    contrib_search_button = None
    contrib_found_text = None
    contrib_found_text_box = None

    #single contributor search.
    single_contrib_label_text = None
    single_contrib_label = None
    single_contrib_text_box = None
    single_contrib_search_button = None


    def __init__(self, parent, controller, data_manager):
        tk.Frame.__init__(self,parent)
        self.data_manager = data_manager

        plt.ion()

        #Create the contributor graphing system.

        #Top contributors.
        self.top_contrib_label_text = tk.StringVar(self)
        self.top_contrib_label_text.set('Top Contributors')
        self.top_contrib_label = tk.Label(self, textvariable=self.top_contrib_label_text)
        self.top_contrib_label.grid(column = 0, row = 0, sticky = 'nw')

        self.top_contrib_figure = Figure(figsize=(5,3), dpi=100)
        self.top_contrib_ax = self.top_contrib_figure.add_subplot(111)
        self.top_contrib_canvas = FigureCanvasTkAgg(self.top_contrib_figure, self)

        self.top_contrib_canvas.draw()
        self.top_contrib_canvas.get_tk_widget().grid(column = 0, row = 1)

        self.generate_top_contributors()

        #Searched contributor.
        self.single_contrib_label_text = tk.StringVar(self)
        self.single_contrib_label_text.set('Contributor')
        self.single_contrib_label = tk.Label(self, textvariable=self.single_contrib_label_text)
        self.single_contrib_label.grid(column = 0, row = 2, sticky = 'nw')

        self.single_contrib_figure = Figure(figsize=(5,3), dpi=100)
        self.single_contrib_ax = self.single_contrib_figure.add_subplot(111)
        self.single_contrib_canvas = FigureCanvasTkAgg(self.single_contrib_figure, self)

        self.single_contrib_canvas.draw()
        self.single_contrib_canvas.get_tk_widget().grid(column = 0, row = 3)

        #Repository Names.
        self.rep_label_text = tk.StringVar(self)
        self.rep_label_text.set('Repository Names')
        self.rep_label = tk.Label(self, textvariable=self.rep_label_text)
        self.rep_label.grid(column = 1, row = 0, sticky = 'nw')

        self.rep_text_box = tk.Text(self, height = 1, width = 60)
        #self.rep_text_box.configure(state='disabled')
        #self.rep_text_box.grid(column = 1, row = 1, sticky = 'nw')

        #List contributors.
        self.contrib_label_text = tk.StringVar(self)
        self.contrib_label_text.set('List Contributors')
        self.contrib_label = tk.Label(self, textvariable=self.contrib_label_text)
        self.contrib_label.grid(column = 1, row = 2, sticky = 'nw')
        self.contrib_text_box = tk.Text(self, height = 1, width = 60)
        self.contrib_text_box.grid(column = 1, row = 3, sticky = 'nw')
        self.contrib_search_button = tk.Button(self, text='Search', command=lambda:self.search_contributors())
        self.contrib_search_button.grid(column = 2, row = 3, sticky = 'nw')
        self.contrib_found_text_box = tk.Text(self, height = 5, width = 60)
        #self.contrib_found_text_box.configure(state='disabled')
        self.contrib_found_text_box.grid(column = 1, row = 4, sticky = 'nw')

        #Search single contributor. 
        self.single_contrib_label_text = tk.StringVar(self)
        self.single_contrib_label_text.set('Repository Names')
        self.single_contrib_label = tk.Label(self, textvariable=self.rep_label_text)
        self.single_contrib_label.grid(column = 1, row = 5, sticky = 'nw')
        self.single_contrib_text_box = tk.Text(self, height = 1, width = 60)
        self.single_contrib_text_box.grid(column = 1, row = 6, sticky = 'nw')
        self.single_contrib_search_button = tk.Button(self, text='Search', command=lambda:self.search_single_contributor())
        self.single_contrib_search_button.grid(column = 2, row = 6, sticky = 'nw')

        self.set_repository_names()
        #self.

    def set_repository_names(self):
        repo_names = self.data_manager.list_repos()

        repo_string = ''
        for repo in repo_names[:len(repo_names) - 1]:
            repo_string += repo + ', '
        repo_string += repo_names[-1]

        self.rep_text_box.insert('insert', repo_string)
        self.rep_text_box.configure(state='disabled')
        self.rep_text_box.grid(column = 1, row = 1, sticky = 'nw')

        
    def search_contributors(self):
        self.__repo_name = self.contrib_text_box.get('1.0', 'end').rstrip()
        self.contrib_text_box.delete('1.0','end')
        
        contrib_names = self.data_manager.list_names(self.__repo_name)
        
        contrib_string = ''
        if len(contrib_names) > 0:
            for name in contrib_names[:len(contrib_names) - 1]:
                contrib_string += (name + ', ') if name != None else ''
            contrib_string += contrib_names[-1]

        self.contrib_found_text_box.configure(state='normal')
        self.contrib_found_text_box.delete('1.0','end')
        self.contrib_found_text_box.insert('insert', contrib_string)
        self.contrib_found_text_box.configure(state='disabled')


    def generate_top_contributors(self, threshold=10):
        self.data_manager.display_most_contributions(self.top_contrib_ax,threshold)

    
    def search_single_contributor(self):
        self.__contrib_name = self.single_contrib_text_box.get('1.0', 'end').rstrip()
        self.single_contrib_text_box.delete('1.0','end')
        
        labels,data = self.data_manager.get_pie_data_by_name(self.__contrib_name)
        print(labels)
        print(data)

        self.single_contrib_ax.pie(data, labels=labels)
        
        
