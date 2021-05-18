import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import matplotlib
from sqlalchemy.sql.expression import column
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
        #self.geometry('%dx%d' % (self.winfo_screenwidth(),self.winfo_screenheight()))
        container = tk.Frame(self)
        #self.geometry('1920x1080')
        self.geometry('1080x1920')

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

    #Canvas for similar contributions graph.
    similar_contrib_label_text = None
    similar_contrib_label = None
    similar_contrib_figure = None
    similar_contrib_ax = None
    similar_contrib_canvas = None

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

    #Search similar contributions.
    similar_contrib_label_text = None
    similar_contrib_label = None
    similar_contrib_text_box = None
    similar_contrib_search_button = None

    #Action type.
    action_type_found_text = None
    action_type_found_text_label = None
    action_type_found_text_box = None
    


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

        self.top_contrib_figure = Figure(figsize=(4,10), dpi=100)
        self.top_contrib_ax = self.top_contrib_figure.add_subplot(111)
        self.top_contrib_canvas = FigureCanvasTkAgg(self.top_contrib_figure, self)

        self.top_contrib_canvas.draw()
        self.top_contrib_canvas.get_tk_widget().grid(column = 0, row = 1, rowspan = 100)

        self.generate_top_contributors()
        
        #Searched contributor.
        self.single_contrib_label_text = tk.StringVar(self)
        self.single_contrib_label_text.set('Contributor')
        self.single_contrib_label = tk.Label(self, textvariable=self.single_contrib_label_text)
        self.single_contrib_label.grid(column = 3, row = 0, sticky = 'nw')

        self.single_contrib_figure = Figure(figsize=(4,10), dpi=100)
        self.single_contrib_ax = self.single_contrib_figure.add_subplot(111)
        self.single_contrib_canvas = FigureCanvasTkAgg(self.single_contrib_figure, self)

        self.single_contrib_canvas.draw()
        self.single_contrib_canvas.get_tk_widget().grid(column = 3, row = 1,rowspan=100)

        #Similar issues Graph.
        self.similar_contrib_label_text = tk.StringVar(self)
        self.similar_contrib_label_text.set('Similar Actions')
        self.similar_contrib_label = tk.Label(self, textvariable=self.similar_contrib_label_text)
        self.similar_contrib_label.grid(column = 4, row = 0, sticky = 'nw', padx=(50,0))

        self.similar_contrib_figure = Figure(figsize=(4,10), dpi=100)
        self.similar_contrib_ax = self.similar_contrib_figure.add_subplot(111)
        self.similar_contrib_canvas = FigureCanvasTkAgg(self.similar_contrib_figure, self)

        self.similar_contrib_canvas.draw()
        self.similar_contrib_canvas.get_tk_widget().grid(column = 4, row = 1,rowspan=100, padx=(50,0))
        
        #Repository Names.
        self.rep_label_text = tk.StringVar(self)
        self.rep_label_text.set('Repository Names')
        self.rep_label = tk.Label(self, textvariable=self.rep_label_text)
        self.rep_label.grid(column = 1, row = 0, sticky = 'nw', columnspan=2)

        self.rep_text_box = tk.Text(self, height = 1, width = 60)
        #self.rep_text_box.configure(state='disabled')
        #self.rep_text_box.grid(column = 1, row = 1, sticky = 'nw')
        self.set_repository_names()

        #List contributors.
        self.contrib_label_text = tk.StringVar(self)
        self.contrib_label_text.set('Display Repository Contributors')
        self.contrib_label = tk.Label(self, textvariable=self.contrib_label_text)
        self.contrib_label.grid(column = 1, row = 2, sticky = 'nw', columnspan=2)
        self.contrib_text_box = tk.Text(self, height = 1, width = 50)
        self.contrib_text_box.grid(column = 1, row = 3, sticky = 'nw', columnspan=2)
        self.contrib_search_button = tk.Button(self, text='Search', command=lambda:self.search_contributors())
        self.contrib_search_button.grid(column = 2, row = 3, sticky = 'ne')
        self.contrib_found_text_box = tk.Text(self, height = 30, width = 60)
        #self.contrib_found_text_box.configure(state='disabled')
        self.contrib_found_text_box.grid(column = 1, row = 4, sticky = 'nw', columnspan=2)

        #Display Action types text.
        self.action_type_found_text = tk.StringVar(self)
        self.action_type_found_text.set('Action Types')
        self.action_type_found_text_label = tk.Label(self, textvariable=self.action_type_found_text)
        self.action_type_found_text_label.grid(column = 1, row = 5, sticky = 'nw', columnspan = 2)
        self.action_type_found_text_box = tk.Text(self, height = 3, width = 60)

        self.set_action_types()
        

        #Search similar contributor. 
        self.similar_contrib_label_text = tk.StringVar(self)
        self.similar_contrib_label_text.set('Display Recommended Contributors by Action')
        self.similar_contrib_label = tk.Label(self, textvariable=self.similar_contrib_label_text)
        self.similar_contrib_label.grid(column = 1, row = 7, sticky = 'nw', columnspan=2)
        self.similar_contrib_text_box = tk.Text(self, height = 1, width = 50)
        self.similar_contrib_text_box.grid(column = 1, row = 8, sticky = 'nw', columnspan=2)
        self.similar_contrib_search_button = tk.Button(self, text='Search', command=lambda:self.search_similar_issues())
        self.similar_contrib_search_button.grid(column = 2, row = 8, sticky = 'ne')

        #Search single contributor. 
        self.single_contrib_label_text = tk.StringVar(self)
        self.single_contrib_label_text.set('Display Single Contributor Metrics')
        self.single_contrib_label = tk.Label(self, textvariable=self.single_contrib_label_text)
        self.single_contrib_label.grid(column = 1, row = 9, sticky = 'nw', columnspan=2)
        self.single_contrib_text_box = tk.Text(self, height = 1, width = 50)
        self.single_contrib_text_box.grid(column = 1, row = 10, sticky = 'nw', columnspan=2)
        self.single_contrib_search_button = tk.Button(self, text='Search', command=lambda:self.search_single_contributor())
        self.single_contrib_search_button.grid(column = 2, row = 10, sticky = 'ne')

        
        self.__repo_name = 'augur'

        self.single_contrib_ax.clear()
        self.similar_contrib_ax.clear()


    def set_repository_names(self):
        repo_names = self.data_manager.list_repos()

        repo_string = ''
        for repo in repo_names[:len(repo_names) - 1]:
            repo_string += repo + ', '
        repo_string += repo_names[-1]

        self.rep_text_box.insert('insert', repo_string)
        self.rep_text_box.configure(state='disabled')
        self.rep_text_box.grid(column = 1, row = 1, sticky = 'nw', columnspan = 2)

    def set_action_types(self):
        action_types = self.data_manager.get_action_types()

        action_string = ''
        for action in action_types[:len(action_types) - 1]:
            action_string += action + ', '
        action_string += action_types[-1]

        self.action_type_found_text_box.insert('insert', action_string)
        self.action_type_found_text_box.configure(state='disabled')
        self.action_type_found_text_box.grid(column = 1, row = 6, sticky = 'nw', columnspan = 2)

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
        self.single_contrib_ax.clear()

        self.__contrib_name = self.single_contrib_text_box.get('1.0', 'end').rstrip()
        self.single_contrib_text_box.delete('1.0','end')
        labels,data = self.data_manager.get_pie_data_by_name(self.__contrib_name)
        
        self.single_contrib_ax.pie(data, labels=labels)
        self.single_contrib_canvas.draw()        

    def search_similar_issues(self,threshold=10):
        self.similar_contrib_ax.clear()

        self.__action_name = self.similar_contrib_text_box.get('1.0', 'end').rstrip()
        self.similar_contrib_text_box.delete('1.0','end')

        self.data_manager.search_similar_contributions(self.similar_contrib_ax, self.__repo_name, self.__action_name,threshold)
        self.similar_contrib_canvas.draw()  
