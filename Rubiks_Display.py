from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import Canvas,Tk,ttk,Label,Entry,Button,mainloop,Text,Frame,IntVar,Checkbutton,Grid
import os
import numpy as np
from tkinter import filedialog
import math
import random
import time

class Display:
    def __init__(self, parent):
        self.stickers={}
        self.parent = parent
        self.main_font = ("Courier", 22, "bold")
        self.max_win_size = (1111,755)
        self.canvas_dimension = min(((self.max_win_size[0]-40)/2,self.max_win_size[1]-230))
        self.canvas_image_counter = 0
        self.im = {}
        self.setup_window()
        self.init_picture()
        self.black='black'
        self.orange= "#FF7604"
        self.blue="#0153DA"
        self.red="#DC0101"
        self.green="#2CA031"
        self.yellow="#FAEF01"
        self.create_stickers()
        self.make_grid()
    def open_images(self):
        pil_img = Image.open('source/icons/play.gif').resize((80,80), Image.ANTIALIAS)
        self.play_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/icons/pause.gif').resize((80,80), Image.ANTIALIAS)
        self.pause_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/icons/close.gif').resize((80,80), Image.ANTIALIAS)
        self.close_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/icons/accept.gif').resize((80,80), Image.ANTIALIAS)
        self.accept_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/icons/refresh.gif').resize((80,80), Image.ANTIALIAS)
        self.refresh_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/icons/random.gif').resize((80,80), Image.ANTIALIAS)
        self.random_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/icons/next.gif').resize((80,80), Image.ANTIALIAS)
        self.step_photo=ImageTk.PhotoImage(pil_img)
        pil_img = Image.open('source/icons/folder_browse.gif').resize((80,80), Image.ANTIALIAS)
        self.open_photo=ImageTk.PhotoImage(pil_img)
    def setup_window(self):
        # initial setup
        self.primary_window = Tk()
        self.open_images()
        self.primary_window.wm_title("Rubiks_Main")
        self.primary_window.geometry('1111x777-1+0')
        # self.primary_window.geometry('1274x960+1274-1055')
        self.primary_window.minsize(width=100, height=30)
        self.primary_window.maxsize(width=self.max_win_size[0], height=self.max_win_size[1])
        
        # canvases
        self.im_frame = ttk.Frame(self.primary_window)
        self.im_frame.grid(row=0,column=0,columnspan=4,sticky="nsew")
        self.im_frame.columnconfigure(0, weight=1)
        self.im_frame.rowconfigure(0, weight=1)
        self.primary_window.columnconfigure(0, weight=1)
        self.primary_window.rowconfigure(0, weight=1)
        
        self.canvas1 = Canvas(self.im_frame,
                                width=self.canvas_dimension,
                                height=self.canvas_dimension,
                                background='black')
        self.canvas1.grid(row=0, column=0, sticky="ns")
        
        self.canvas2 = Canvas(self.im_frame,
                                width=self.canvas_dimension,
                                height=self.canvas_dimension,
                                background='black')
        self.canvas2.grid(row=0, column=1, sticky="ns")
        
        # buttons
        self.all_buttons_frame = ttk.Frame(self.primary_window)
        self.all_buttons_frame.grid(row=2,column=0,columnspan=2)
        #
        self.buttons_frame = ttk.Frame(self.all_buttons_frame)
        self.buttons_frame.grid(row=2,column=0,columnspan=2)
        #
        Button(self.buttons_frame,
               command=self.shuffle,
               image=self.random_photo,
               width="80",height="80").grid(row=0,column=3)
        #
        Button(self.buttons_frame,
               command=self.parent.cube.solve,
               image=self.accept_photo,
               width="80",height="80").grid(row=0,column=4)
        #
        Button(self.buttons_frame,
               command=self.refresh,
               image=self.refresh_photo,
               width="80",height="80").grid(row=0,column=6)
        #
        Button(self.buttons_frame,
               command=self.parent.cube.load,
               image=self.open_photo,
               width="80",height="80").grid(row=0,column=7)
        # cube move buttons
        self.move_buttons_frame = ttk.Frame(self.all_buttons_frame)
        self.move_buttons_frame.grid(row=3,column=0,columnspan=2)
        for x in range(6): Grid.columnconfigure(self.move_buttons_frame,x,weight=1)
        #
        Button(self.move_buttons_frame,
               command=lambda: self.move("R"),
               text='R',
               font=self.main_font,).grid(row=0,column=0)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("L"),
               text='L',
               font=self.main_font,).grid(row=0,column=1)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("U"),
               text='U',
               font=self.main_font,).grid(row=0,column=2)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("D"),
               text='D',
               font=self.main_font,).grid(row=0,column=3)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("F"),
               text='F',
               font=self.main_font,).grid(row=0,column=4)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("B"),
               text='B',
               font=self.main_font,).grid(row=0,column=5)
        #
        # CCW buttons
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("R'"),
               text="R'",
               font=self.main_font,).grid(row=1,column=0)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("L'"),
               text="L'",
               font=self.main_font,).grid(row=1,column=1)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("U'"),
               text="U'",
               font=self.main_font,).grid(row=1,column=2)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("D'"),
               text="D'",
               font=self.main_font,).grid(row=1,column=3)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("F'"),
               text="F'",
               font=self.main_font,).grid(row=1,column=4)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.move("B'"),
               text="B'",
               font=self.main_font,).grid(row=1,column=5)
        # turn cube buttons
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.turn("D"),
               text="X",
               font=self.main_font,).grid(row=2,column=0)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.turn("U"),
               text="X'",
               font=self.main_font,).grid(row=2,column=1)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.turn("R"),
               text="Y",
               font=self.main_font,).grid(row=2,column=2)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.turn("L"),
               text="Y'",
               font=self.main_font,).grid(row=2,column=3)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.turn("Z"),
               text="Z",
               font=self.main_font,).grid(row=2,column=4)
        #
        Button(self.move_buttons_frame,
               command=lambda:  self.turn("Z'"),
               text="Z'",
               font=self.main_font,).grid(row=2,column=5)
        # self.grid_image_frame = ttk.Frame(self.primary_window)
        # self.grid_image_frame.grid(row=2,column=3,columnspan=2)
        self.grid_canvas_size = .8*self.canvas_dimension,.8*self.canvas_dimension * 9 / 12
        self.grid_canvas = Canvas(self.primary_window,
                                  width=self.grid_canvas_size[0],
                                  height=self.grid_canvas_size[1],
                                  background='black')
        self.grid_canvas.grid(row=2,column=3,columnspan=2)
        # button bindings
        self.primary_window.bind("U", lambda event: self.move("U"))
        self.primary_window.bind("u", lambda event: self.move("U"))
        self.primary_window.bind("<Control-U>", lambda event: self.move("U'"))
        self.primary_window.bind("<Control-u>", lambda event: self.move("U'"))
        #
        self.primary_window.bind("D", lambda event: self.move("D"))
        self.primary_window.bind("d", lambda event: self.move("D"))
        self.primary_window.bind("<Control-D>", lambda event: self.move("D'"))
        self.primary_window.bind("<Control-d>", lambda event: self.move("D'"))
        #
        self.primary_window.bind("R", lambda event: self.move("R"))
        self.primary_window.bind("r", lambda event: self.move("R"))
        self.primary_window.bind("<Control-R>", lambda event: self.move("R'"))
        self.primary_window.bind("<Control-r>", lambda event: self.move("R'"))
        #
        self.primary_window.bind("L", lambda event: self.move("L"))
        self.primary_window.bind("l", lambda event: self.move("L"))
        self.primary_window.bind("<Control-L>", lambda event: self.move("L'"))
        self.primary_window.bind("<Control-l>", lambda event: self.move("L'"))
        #
        self.primary_window.bind("F", lambda event: self.move("F"))
        self.primary_window.bind("f", lambda event: self.move("F"))
        self.primary_window.bind("<Control-F>", lambda event: self.move("F'"))
        self.primary_window.bind("<Control-f>", lambda event: self.move("F'"))
        #
        self.primary_window.bind("B", lambda event: self.move("B"))
        self.primary_window.bind("b", lambda event: self.move("B"))
        self.primary_window.bind("<Control-B>", lambda event: self.move("B'"))
        self.primary_window.bind("<Control-b>", lambda event: self.move("B'"))
    def shuffle(self):
        # self.parent.cube.new_cube()
        self.parent.cube.shuffle()
        self.update_stickers()
    def move(self,direction):
        self.parent.cube.move(direction)
        self.update_stickers()
    def turn(self,direction):
        self.parent.cube.turn_cube(direction)
        self.update_stickers()
    def refresh(self):
        self.parent.cube.new_cube()
        self.update_stickers()
        # for i in range(10000):
            # print("check iteration: " + str(i),end="\r")
            # self.shuffle()
            # self.parent.cube.solve(backup=False)
    def init_picture(self):
        # corner points
        self.corners = {}
        self.corners['A']=np.array([self.canvas_dimension*.1,self.canvas_dimension*.3224])
        self.corners['B']=np.array([self.canvas_dimension*.5,self.canvas_dimension*.14])
        self.corners['C']=np.array([self.canvas_dimension*.9,self.canvas_dimension*.3224])
        self.corners['D']=np.array([self.canvas_dimension*.5,self.canvas_dimension*.51])
        self.corners['E']=np.array([self.canvas_dimension*.105,self.canvas_dimension*.69])
        self.corners['F']=np.array([self.canvas_dimension*.5,self.canvas_dimension*.9])
        self.corners['G']=np.array([self.canvas_dimension*.895,self.canvas_dimension*.69])
        front_side_points=['A','B','C','D','E','F','G']
        back_side_points=['H','I','J','K','L','M','N']
        for i,point in enumerate(back_side_points):
            self.corners[point]=np.copy(self.corners[front_side_points[i]])
            self.corners[point][1]=self.canvas_dimension-self.corners[point][1]
        # edge vectors... see source/vector reference.png for exhibit
        self.edge_vectors={}
        # front side
        self.edge_vectors['AB'] = self.corners['B'] - self.corners['A']
        self.edge_vectors['BC'] = self.corners['C'] - self.corners['B']
        self.edge_vectors['AD'] = self.corners['D'] - self.corners['A']
        self.edge_vectors['DC'] = self.corners['C'] - self.corners['D']
        self.edge_vectors['AE'] = self.corners['E'] - self.corners['A']
        self.edge_vectors['EF'] = self.corners['F'] - self.corners['E']
        self.edge_vectors['FG'] = self.corners['G'] - self.corners['F']
        self.edge_vectors['DF'] = self.corners['F'] - self.corners['D']
        self.edge_vectors['CG'] = self.corners['G'] - self.corners['C']
        # back side
        self.edge_vectors['HI'] = self.corners['I'] - self.corners['H']
        self.edge_vectors['IJ'] = self.corners['J'] - self.corners['I']
        self.edge_vectors['HK'] = self.corners['K'] - self.corners['H']
        self.edge_vectors['KJ'] = self.corners['J'] - self.corners['K']
        self.edge_vectors['LH'] = self.corners['H'] - self.corners['L']
        self.edge_vectors['LM'] = self.corners['M'] - self.corners['L']
        self.edge_vectors['MN'] = self.corners['N'] - self.corners['M']
        self.edge_vectors['MK'] = self.corners['K'] - self.corners['M']
        self.edge_vectors['NJ'] = self.corners['J'] - self.corners['N']
        # reverse vectors
        for vector in dict(self.edge_vectors):
            self.edge_vectors[vector[::-1]]=-1*self.edge_vectors[vector]
    def create_stickers(self):
        def equation(pt1,pt2):
            if pt1[0]==pt2[0]: m='inf'
            elif pt1[0] < pt2[0]: m=(pt2[1]-pt1[1])/(pt2[0]-pt1[0])
            else: m=(pt1[1]-pt2[1])/(pt1[0]-pt2[0])
            if m=='inf': 
                b=pt1[0]
            else: b=m*-pt1[0]+pt1[1]
            answer = m,b
            # print("answer: " + str(answer))
            return m,b
        def intersection(e1,e2):
            m1,b1=e1
            m2,b2=e2
            # print("equations " + str(e1) + str(e2))
            if m1== m2:
                print("Bad equations; these lines do not intersect: " + str(e1) + str(e2))
                1/0
            elif m1=='inf':
                x = b1
                y = m2*x + b2
            elif m2=='inf':
                x = b2
                y = m1*x + b1
            else:
                new_eq=np.array([(-m1/m2)*m2,(-m1/m2)*b2])
                new_b = b1+new_eq[1]
                new_y = 1+(-m1/m2)
                y = new_b/new_y
                x = (y-b1)/m1
            answer = np.array([x,y])
            return answer
        self.stickers = []
        for row in range(9):
            col_list = []
            for col in range(12):
                col_list.append([None])
            self.stickers.append(col_list)
        # TOP (top side of the left cube, BLACK)
        for row in range(3):
            for col in range(3):
                corners={}
                line1 = equation(self.corners['A']+(col)/3*self.edge_vectors['AB'],self.corners['D']+(col)/3*self.edge_vectors['DC'])
                line2 = equation(self.corners['A']+row/3*self.edge_vectors['AD'],self.corners['B']+row/3*self.edge_vectors['BC'])
                corners[0] = intersection(line1,line2)
                line1 = equation(self.corners['A']+(col+1)/3*self.edge_vectors['AB'],self.corners['D']+(col+1)/3*self.edge_vectors['DC'])
                line2 = equation(self.corners['A']+row/3*self.edge_vectors['AD'],self.corners['B']+row/3*self.edge_vectors['BC'])
                corners[1] = intersection(line1,line2)
                line1 = equation(self.corners['A']+(col+1)/3*self.edge_vectors['AB'],self.corners['D']+(col+1)/3*self.edge_vectors['DC'])
                line2 = equation(self.corners['A']+(row+1)/3*self.edge_vectors['AD'],self.corners['B']+(row+1)/3*self.edge_vectors['BC'])
                corners[2] = intersection(line1,line2)
                line1 = equation(self.corners['A']+col/3*self.edge_vectors['AB'],self.corners['D']+col/3*self.edge_vectors['DC'])
                line2 = equation(self.corners['A']+(row+1)/3*self.edge_vectors['AD'],self.corners['B']+(row+1)/3*self.edge_vectors['BC'])
                corners[3] = intersection(line1,line2)
                coords = list(corners[0])+list(corners[1])+list(corners[2])+list(corners[3])
                self.stickers[row][6+col]=self.canvas1.create_polygon(coords,outline="white",fill=self.black,width=3)
        # LEFT (left side of the left cube, ORANGE)
        for row in range(3):
            for col in range(3):
                corners={}
                line1 = equation(self.corners['A']+col/3*self.edge_vectors['AD'],self.corners['E']+col/3*self.edge_vectors['EF'])
                line2 = equation(self.corners['A']+(row)/3*self.edge_vectors['AE'],self.corners['D']+(row)/3*self.edge_vectors['DF'])
                corners[0] = intersection(line1,line2)
                line1 = equation(self.corners['A']+col/3*self.edge_vectors['AD'],self.corners['E']+col/3*self.edge_vectors['EF'])
                line2 = equation(self.corners['A']+(row+1)/3*self.edge_vectors['AE'],self.corners['D']+(row+1)/3*self.edge_vectors['DF'])
                corners[1] = intersection(line1,line2)
                line1 = equation(self.corners['A']+(col+1)/3*self.edge_vectors['AD'],self.corners['E']+(col+1)/3*self.edge_vectors['EF'])
                line2 = equation(self.corners['A']+(row+1)/3*self.edge_vectors['AE'],self.corners['D']+(row+1)/3*self.edge_vectors['DF'])
                corners[2] = intersection(line1,line2)
                line1 = equation(self.corners['A']+(col+1)/3*self.edge_vectors['AD'],self.corners['E']+(col+1)/3*self.edge_vectors['EF'])
                line2 = equation(self.corners['A']+row/3*self.edge_vectors['AE'],self.corners['D']+row/3*self.edge_vectors['DF'])
                corners[3] = intersection(line1,line2)
                coords = list(corners[0])+list(corners[1])+list(corners[2])+list(corners[3])
                self.stickers[3+row][col+3]=self.canvas1.create_polygon(coords,outline="white",fill=self.orange,width=3)
        # FRONT (right side of the left cube, GREEN)
        for row in range(3):
            for col in range(3):
                corners={}
                line1 = equation(self.corners['D']+col/3*self.edge_vectors['DC'],self.corners['F']+col/3*self.edge_vectors['FG'])
                line2 = equation(self.corners['D']+(row)/3*self.edge_vectors['DF'],self.corners['C']+(row)/3*self.edge_vectors['CG'])
                corners[0] = intersection(line1,line2)
                line1 = equation(self.corners['D']+col/3*self.edge_vectors['DC'],self.corners['F']+col/3*self.edge_vectors['FG'])
                line2 = equation(self.corners['D']+(row+1)/3*self.edge_vectors['DF'],self.corners['C']+(row+1)/3*self.edge_vectors['CG'])
                corners[1] = intersection(line1,line2)
                line1 = equation(self.corners['D']+(col+1)/3*self.edge_vectors['DC'],self.corners['F']+(col+1)/3*self.edge_vectors['FG'])
                line2 = equation(self.corners['D']+(row+1)/3*self.edge_vectors['DF'],self.corners['C']+(row+1)/3*self.edge_vectors['CG'])
                corners[2] = intersection(line1,line2)
                line1 = equation(self.corners['D']+(col+1)/3*self.edge_vectors['DC'],self.corners['F']+(col+1)/3*self.edge_vectors['FG'])
                line2 = equation(self.corners['D']+row/3*self.edge_vectors['DF'],self.corners['C']+row/3*self.edge_vectors['CG'])
                corners[3] = intersection(line1,line2)
                coords = list(corners[0])+list(corners[1])+list(corners[2])+list(corners[3])
                self.stickers[row+3][6+col]=self.canvas1.create_polygon(coords,outline="white",fill=self.green,width=3)
        # BOTTOM (bottom of the right cube, YELLOW)
        for row in range(3):
            for col in range(3):
                corners={}
                line1 = equation(self.corners['I']+col/3*self.edge_vectors['IH'],self.corners['J']+col/3*self.edge_vectors['JK'])
                line2 = equation(self.corners['I']+(row)/3*self.edge_vectors['IJ'],self.corners['H']+(row)/3*self.edge_vectors['HK'])
                corners[0] = intersection(line1,line2)
                line1 = equation(self.corners['I']+col/3*self.edge_vectors['IH'],self.corners['J']+col/3*self.edge_vectors['JK'])
                line2 = equation(self.corners['I']+(row+1)/3*self.edge_vectors['IJ'],self.corners['H']+(row+1)/3*self.edge_vectors['HK'])
                corners[1] = intersection(line1,line2)
                line1 = equation(self.corners['I']+(col+1)/3*self.edge_vectors['IH'],self.corners['J']+(col+1)/3*self.edge_vectors['JK'])
                line2 = equation(self.corners['I']+(row+1)/3*self.edge_vectors['IJ'],self.corners['H']+(row+1)/3*self.edge_vectors['HK'])
                corners[2] = intersection(line1,line2)
                line1 = equation(self.corners['I']+(col+1)/3*self.edge_vectors['IH'],self.corners['J']+(col+1)/3*self.edge_vectors['JK'])
                line2 = equation(self.corners['I']+row/3*self.edge_vectors['IJ'],self.corners['H']+row/3*self.edge_vectors['HK'])
                corners[3] = intersection(line1,line2)
                coords = list(corners[0])+list(corners[1])+list(corners[2])+list(corners[3])
                self.stickers[row+6][6+col]=self.canvas2.create_polygon(coords,outline="white",fill=self.yellow,width=3)
        # RIGHT (right side of the right cube, RED)
        for row in range(3):
            for col in range(3):
                corners={}
                line1 = equation(self.corners['L']+col/3*self.edge_vectors['LM'],self.corners['H']+col/3*self.edge_vectors['HK'])
                line2 = equation(self.corners['L']+(row)/3*self.edge_vectors['LH'],self.corners['M']+(row)/3*self.edge_vectors['MK'])
                corners[0] = intersection(line1,line2)
                line1 = equation(self.corners['L']+col/3*self.edge_vectors['LM'],self.corners['H']+col/3*self.edge_vectors['HK'])
                line2 = equation(self.corners['L']+(row+1)/3*self.edge_vectors['LH'],self.corners['M']+(row+1)/3*self.edge_vectors['MK'])
                corners[1] = intersection(line1,line2)
                line1 = equation(self.corners['L']+(col+1)/3*self.edge_vectors['LM'],self.corners['H']+(col+1)/3*self.edge_vectors['HK'])
                line2 = equation(self.corners['L']+(row+1)/3*self.edge_vectors['LH'],self.corners['M']+(row+1)/3*self.edge_vectors['MK'])
                corners[2] = intersection(line1,line2)
                line1 = equation(self.corners['L']+(col+1)/3*self.edge_vectors['LM'],self.corners['H']+(col+1)/3*self.edge_vectors['HK'])
                line2 = equation(self.corners['L']+row/3*self.edge_vectors['LH'],self.corners['M']+row/3*self.edge_vectors['MK'])
                corners[3] = intersection(line1,line2)
                coords = list(corners[0])+list(corners[1])+list(corners[2])+list(corners[3])
                self.stickers[row+3][9+col]=self.canvas2.create_polygon(coords,outline="white",fill=self.red,width=3)
        # BACK (left side of the right cube, BLUE)
        for row in range(3):
            for col in range(3):
                corners={}
                line1 = equation(self.corners['M']+col/3*self.edge_vectors['MN'],self.corners['K']+col/3*self.edge_vectors['KJ'])
                line2 = equation(self.corners['M']+(row)/3*self.edge_vectors['MK'],self.corners['N']+(row)/3*self.edge_vectors['NJ'])
                corners[0] = intersection(line1,line2)
                line1 = equation(self.corners['M']+col/3*self.edge_vectors['MN'],self.corners['K']+col/3*self.edge_vectors['KJ'])
                line2 = equation(self.corners['M']+(row+1)/3*self.edge_vectors['MK'],self.corners['N']+(row+1)/3*self.edge_vectors['NJ'])
                corners[1] = intersection(line1,line2)
                line1 = equation(self.corners['M']+(col+1)/3*self.edge_vectors['MN'],self.corners['K']+(col+1)/3*self.edge_vectors['KJ'])
                line2 = equation(self.corners['M']+(row+1)/3*self.edge_vectors['MK'],self.corners['N']+(row+1)/3*self.edge_vectors['NJ'])
                corners[2] = intersection(line1,line2)
                line1 = equation(self.corners['M']+(col+1)/3*self.edge_vectors['MN'],self.corners['K']+(col+1)/3*self.edge_vectors['KJ'])
                line2 = equation(self.corners['M']+row/3*self.edge_vectors['MK'],self.corners['N']+row/3*self.edge_vectors['NJ'])
                corners[3] = intersection(line1,line2)
                coords = list(corners[0])+list(corners[1])+list(corners[2])+list(corners[3])
                self.stickers[row+3][col]=self.canvas2.create_polygon(coords,outline="white",fill=self.blue,width=3)
    def update_stickers(self):
        cube=self.parent.cube.cube
        top_coords = []
        for col in range(3,9):
            for row in range(0,6):
                top_coords.append([row,col])
        for row in range(9):
            for col in range(12):
                if self.stickers[row][col] is not None:
                    if [row,col] in top_coords: canv = self.canvas1
                    else: canv = self.canvas2
                    if   cube[row,col]==1:canv.itemconfig(self.stickers[row][col],fill=self.blue)
                    elif cube[row,col]==2:canv.itemconfig(self.stickers[row][col],fill=self.orange)
                    elif cube[row,col]==3:canv.itemconfig(self.stickers[row][col],fill=self.green)
                    elif cube[row,col]==4:canv.itemconfig(self.stickers[row][col],fill=self.red)
                    elif cube[row,col]==5:canv.itemconfig(self.stickers[row][col],fill=self.yellow)
                    elif cube[row,col]==6:canv.itemconfig(self.stickers[row][col],fill=self.black)
        self.update_grid()
    def make_grid(self):
        size=self.grid_canvas_size
        # for row in range(1,9):
            # start=[0,row*size[0]/9]
            # end=[size[0],row*size[0]/9]
            # self.grid_canvas.create_line(start+end,fill='white',width=3)
        # for col in range(1,12):
            # start=[col*size[1]/12,0]
            # end=[col*size[1],size[1]]
            # self.grid_canvas.create_line(start+end,fill='white',width=3)
        self.grid_stickers = []
        for row in range(9):
            col_list = []
            for col in range(12):
                col_list.append([None])
            self.grid_stickers.append(col_list)
        cube = self.parent.cube.cube
        canv = self.grid_canvas
        for row in range(9):
            for col in range(12):
                if   cube[row,col]==1:color = self.blue
                elif cube[row,col]==2:color = self.orange
                elif cube[row,col]==3:color = self.green
                elif cube[row,col]==4:color = self.red
                elif cube[row,col]==5:color = self.yellow
                elif cube[row,col]==6:color = self.black
                else: color = 'gray'
                p0=[col*size[0]/12,row*size[1]/9,]
                p1=[col*size[0]/12,(row+1)*size[1]/9]
                p2=[(col+1)*size[0]/12,(row+1)*size[1]/9]
                p3=[(col+1)*size[0]/12,row*size[1]/9]
                coords=p0+p1+p2+p3
                self.grid_stickers[row][col]=canv.create_polygon(coords,outline="white",fill=color,width=3)
    def update_grid(self):
        canv = self.grid_canvas
        cube = self.parent.cube.cube
        for row in range(9):
            for col in range(12):
                if self.grid_stickers[row][col] is not None:
                    if   cube[row,col]==1:canv.itemconfig(self.grid_stickers[row][col],fill=self.blue)
                    elif cube[row,col]==2:canv.itemconfig(self.grid_stickers[row][col],fill=self.orange)
                    elif cube[row,col]==3:canv.itemconfig(self.grid_stickers[row][col],fill=self.green)
                    elif cube[row,col]==4:canv.itemconfig(self.grid_stickers[row][col],fill=self.red)
                    elif cube[row,col]==5:canv.itemconfig(self.grid_stickers[row][col],fill=self.yellow)
                    elif cube[row,col]==6:canv.itemconfig(self.grid_stickers[row][col],fill=self.black)
    def update_generation_entry(self):
        val = str(self.parent.generation_number)
        self.generation_entry.config(state="normal")
        self.generation_entry.delete(0,'end')
        self.generation_entry.insert('end',val)
        self.generation_entry.config(state='disabled')
    def update_alive_entry(self):
        val = str(self.parent.number_alive)
        if val != self.alive_entry.get():
            self.alive_entry.config(state="normal")
            self.alive_entry.delete(0,'end')
            self.alive_entry.insert('end',val)
            self.alive_entry.config(state='disabled')
    def update_high_score_entry(self):
        val = str(int(self.parent.best_adjusted_fitness//.0001))
        self.high_score.config(state="normal")
        self.high_score.delete(0,'end')
        self.high_score.insert('end',val)
        self.high_score.config(state='disabled')
    def play_button_func(self):
        self.parent.pause = False
        self.parent.main_queue.put(self.parent.play)
    def pause_button_func(self):
        if self.parent.pause: self.parent.pause = False
        else: self.parent.pause = True
    def step(self):
        self.parent.pause_step = True
        self.parent.pause = True
        if self.parent.main_queue.empty() and not self.parent.game_over:
            self.parent.main_queue.put(self.parent.play)
    def close(self):
        # self.primary_window.destroy()
        self.parent.close()
    def create_bg(self):
        self.maze_bg = Image.open('source/maze.png')
        self.maze_bg = ImageTk.PhotoImage(self.maze_bg)
    def update_display(self,im):
        self.im[self.canvas_image_counter] = ImageTk.PhotoImage(im)
        self.the_canvas.create_image((0,0),anchor='nw',image=self.im[self.canvas_image_counter])
        if self.canvas_image_counter == 0: self.canvas_image_counter = 1
        else: self.canvas_image_counter = 0