import numpy as np
import random as rando
import pprint
np.set_printoptions(suppress=True, precision=2, linewidth=140)
import time
import os

class Cube:
    def __init__(self,parent):
        self.parent = parent
        self.new_cube()
        self.file_save_location = os.getcwd().replace("\\","/")+'/misc/last_solve_attempt.npy'
    def new_cube(self):
        self.cube = np.array([[-1., -1., -1., -1., -1., -1.,  6.,  6.,  6., -1., -1., -1.],
                              [-1., -1., -1., -1., -1., -1.,  6.,  6.,  6., -1., -1., -1.],
                              [-1., -1., -1., -1., -1., -1.,  6.,  6.,  6., -1., -1., -1.],
                              [ 1.,  1.,  1.,  2.,  2.,  2.,  3.,  3.,  3.,  4.,  4.,  4.],
                              [ 1.,  1.,  1.,  2.,  2.,  2.,  3.,  3.,  3.,  4.,  4.,  4.],
                              [ 1.,  1.,  1.,  2.,  2.,  2.,  3.,  3.,  3.,  4.,  4.,  4.],
                              [-1., -1., -1., -1., -1., -1.,  5.,  5.,  5., -1., -1., -1.],
                              [-1., -1., -1., -1., -1., -1.,  5.,  5.,  5., -1., -1., -1.],
                              [-1., -1., -1., -1., -1., -1.,  5.,  5.,  5., -1., -1., -1.]],np.int32)
    def solve(self,backup=True):
        if backup: np.save(self.file_save_location,self.cube)
        self.make_plus_sign()
        self.orient_plus_sign()
        self.solve_top_corners()
        self.solve_middle_edges()
        self.parent.display.update_stickers()
    def load(self):
        try: self.cube = np.load(self.file_save_location)
        except: print("Failed to load cube.")
        self.parent.display.update_stickers()
    def move(self,move_type=None):
        move_type = move_type.upper()
        if move_type == "R":
            self.turn_cube("R")
            self.move("F")
            self.turn_cube("L")
        elif move_type == "R'":
            self.turn_cube("R")
            self.move("F'")
            self.turn_cube("L")
        elif move_type == "L":
            self.turn_cube("L")
            self.move("F")
            self.turn_cube("R")
        elif move_type == "L'":
            self.turn_cube("L")
            self.move("F'")
            self.turn_cube("R")
        elif move_type == "U":
            self.turn_cube("U")
            self.move("F")
            self.turn_cube("D")
        elif move_type == "U'":
            self.turn_cube("U")
            self.move("F'")
            self.turn_cube("D")
        elif move_type == "D":
            self.turn_cube("D")
            self.move("F")
            self.turn_cube("U")
        elif move_type == "D'":
            self.turn_cube("D")
            self.move("F'")
            self.turn_cube("U")
        elif move_type == "F":
            self.cube[2:7,5:10]=np.rot90(self.cube[2:7,5:10],-1)
        elif move_type == "F'":
            self.cube[2:7,5:10]=np.rot90(self.cube[2:7,5:10],1)
        elif move_type == "B":
            self.turn_cube("B")
            self.move("F")
            self.turn_cube("B")
        elif move_type == "B'":
            self.turn_cube("B")
            self.move("F'")
            self.turn_cube("B")
        # cube check
        number, counts = np.unique(self.cube,return_counts=True)
        counts = dict(zip(number, counts))
        for i in range(1,7):
            if counts[i]!=9: 
                print("self.cube:\n" + str(self.cube))
                1/0
        # print("self.cube:\n" + str(self.cube))
        self.edge_check()
    def turn_cube(self,face=None):
        face = face.upper()
        print("face: " + str(face))
        # specify which face becomes the front
        if face == "X": face = "B"
        elif face == "X'": face == "U"
        elif face == "Y": face == "R"
        elif face == "Y'": face == "L"
        if face == "R":
            self.cube[3:6,:]=np.roll(self.cube[3:6,:],-3,axis=1)
            self.cube[0:3,6:9]=np.rot90(self.cube[0:3,6:9],-1)
            self.cube[6:9,6:9]=np.rot90(self.cube[6:9,6:9],1)
        elif face == "L":
            self.cube[3:6,:]=np.roll(self.cube[3:6,:],3,axis=1)
            self.cube[0:3,6:9]=np.rot90(self.cube[0:3,6:9],1)
            self.cube[6:9,6:9]=np.rot90(self.cube[6:9,6:9],-1)
        elif face == "U":
            self.cube[:,6:9]=np.roll(self.cube[:,6:9],3,axis=0)
            self.cube[3:6,:3],self.cube[0:3,6:9]=self.cube[0:3,6:9][::-1,::-1].copy(),self.cube[3:6,:3][::-1,::-1].copy()
            self.cube[3:6,3:6]=np.rot90(self.cube[3:6,3:6],-1)
            self.cube[3:6,9:]=np.rot90(self.cube[3:6,9:],1)
        elif face == "D":
            self.cube[:,6:9]=np.roll(self.cube[:,6:9],-3,axis=0)
            self.cube[3:6,:3],self.cube[6:,6:9]=np.fliplr(np.flipud(self.cube[6:,6:9])).copy(),np.fliplr(np.flipud(self.cube[3:6,:3])).copy()
            self.cube[3:6,3:6]=np.rot90(self.cube[3:6,3:6],1)
            self.cube[3:6,9:]=np.rot90(self.cube[3:6,9:],-1)
        elif face == "B":
            self.cube[3:6,:]=np.roll(self.cube[3:6,:],6,axis=1)
            self.cube[0:3,6:9]=np.rot90(self.cube[0:3,6:9],2)
            self.cube[6:9,6:9]=np.rot90(self.cube[6:9,6:9],2)
        elif face == "Z":
            self.cube[3:6,6:9]=np.rot90(self.cube[3:6,6:9],-1)
            self.cube[3:6,:3]=np.rot90(self.cube[3:6,:3],1)
            self.cube[3:6,3:6],self.cube[:3,6:9],self.cube[3:6,9:],self.cube[6:,6:9]=np.rot90(self.cube[6:,6:9],-1).copy(),np.rot90(self.cube[3:6,3:6],-1).copy(),np.rot90(self.cube[:3,6:9],-1).copy(),np.rot90(self.cube[3:6,9:],-1).copy()
        elif face == "Z'":
            self.cube[3:6,6:9]=np.rot90(self.cube[3:6,6:9],1)
            self.cube[3:6,:3]=np.rot90(self.cube[3:6,:3],-1)
            self.cube[3:6,3:6],self.cube[:3,6:9],self.cube[3:6,9:],self.cube[6:,6:9]=np.rot90(self.cube[:3,6:9],1).copy(),np.rot90(self.cube[3:6,9:],1).copy(),np.rot90(self.cube[6:,6:9],1).copy(),np.rot90(self.cube[3:6,3:6],1).copy()
    def shuffle(self):
        move_set = ("R","R'","L","L'","U","U'","D","D'","F","F'")
        number_of_moves = rando.randint(15,45)
        for i in range(number_of_moves):
            self.move(rando.choice(move_set))
    def do_algorithm(self,alg):
        alg = alg.split(",")
        for move in alg:
            self.move(move)
    def edge_check(self):
        # ar=np.zeros((9,12))
        locations=[[[0,6],[3,3],[3,2]],
                   [[0,7],[3,1]],
                   [[0,8],[3,0],[3,11]],
                   [[1,6],[3,4]],
                   [[1,8],[3,10]],
                   [[2,6],[3,6],[3,5]],
                   [[2,7],[3,7]],
                   [[2,8],[3,8],[3,9]],
                   [[4,0],[4,11]],
                   [[4,2],[4,3]],
                   [[4,5],[4,6]],
                   [[4,8],[4,9]],
                   [[6,6],[5,6],[5,5]],
                   [[6,7],[5,7]],
                   [[6,8],[5,8],[5,9]],
                   [[7,6],[5,4]],
                   [[7,8],[5,10]],
                   [[8,6],[5,3],[5,2]],
                   [[8,7],[5,1]],
                   [[8,8],[5,0],[5,11]]]
        for i, loc_set in enumerate(locations):
            check = None
            for loc in loc_set:
                if check is None: check = self.cube[loc[0],loc[1]]
                elif self.cube[loc[0],loc[1]] == check: 
                    bad_ar = np.zeros((9,12))
                    for loc1 in loc_set: bad_ar[loc1[0],loc1[1]]=1
                    print("bad cube.")
                    print("bad_ar:\n" + str(bad_ar))
                    self.parent.display.update_stickers()
                    self.parent.display.update_grid()
                    print(self.cube)
                    1/0
    def make_plus_sign(self):
        top_middle_color = self.cube[1,7]
        locations = [[0,7],[1,8],[2,7],[1,6]]
        done_locations = [self.cube[loc[0],loc[1]] == top_middle_color for loc in locations]
        while False in done_locations:
            # move edge pieces up where can
            # position 1 - top front edge
            if top_middle_color in (self.cube[4,5],self.cube[6,7],self.cube[4,9]):
                while top_middle_color == self.cube[2,7]: self.move("U")
                while top_middle_color != self.cube[2,7]: self.move("F")
            # position 2 - top left edge
            elif top_middle_color in (self.cube[4,6],self.cube[7,6],self.cube[4,2]):
                while top_middle_color == self.cube[1,6]: self.move("U")
                while top_middle_color != self.cube[1,6]: self.move("L")
            # position 3 - top rear edge
            elif top_middle_color in (self.cube[4,3],self.cube[8,7],self.cube[4,11]):
                while top_middle_color == self.cube[0,7]: self.move("U")
                while top_middle_color != self.cube[0,7]: self.move("B")
            # position 4 - top right edge
            elif top_middle_color in (self.cube[4,8],self.cube[7,8],self.cube[4,0]):
                while top_middle_color == self.cube[1,8]: self.move("U")
                while top_middle_color != self.cube[1,8]: self.move("R")
            # get inaccessible edges
            # front bottom
            elif top_middle_color in [self.cube[5,7],self.cube[3,7]]:
                while top_middle_color == self.cube[2,7]: self.move("U")
                self.move("F")
            # right bottom
            elif top_middle_color in [self.cube[5,10],self.cube[3,10]]:
                while top_middle_color == self.cube[1,8]: self.move("U")
                self.move("R")
            # left bottom
            elif top_middle_color in [self.cube[5,4],self.cube[3,4]]:
                while top_middle_color == self.cube[1,6]: self.move("U")
                self.move("L")
            elif top_middle_color in [self.cube[5,1],self.cube[3,1]]:
                while top_middle_color == self.cube[0,7]: self.move("U")
                self.move("B")
            done_locations = [self.cube[loc[0],loc[1]] == top_middle_color for loc in locations]
    def orient_plus_sign(self):
        def switch_top_front_and_top_right_edges(): self.do_algorithm("R',U',R,U,R'")
        correct_in_a_row = 0
        while correct_in_a_row < 4:
            if self.cube[3,7] != self.cube[4,7]:
                correct_in_a_row = 0
                switch_top_front_and_top_right_edges()
            else:
                correct_in_a_row += 1
            self.turn_cube("R")
    def solve_top_corners(self):
        top_middle_color = self.cube[1,7]
        def corners_solved():
            c=self.cube
            c1 = c[3,8]==c[4,7] and c[3,9]==c[4,10]
            c2 = c[3,11]==c[4,10]and c[3,0]==c[4,1]
            c3 = c[3,2]==c[4,1] and c[3,3]==c[4,4]
            c4 = c[3,5]==c[4,4] and c[3,6]==c[4,7]
            return c1 and c2 and c3 and c4
        while not corners_solved():
            if top_middle_color in self.cube[5,:] or top_middle_color in self.cube[6:,6:9]:
                while not np.any(self.cube[5:7,8:10] == top_middle_color):
                    self.turn_cube("R")
                corner_piece = self.cube[5:7,8:10]
                needed_corner_colors = [self.cube[4,7],self.cube[4,10]]
                while not ((needed_corner_colors[0] in corner_piece) and (needed_corner_colors[1] in corner_piece)):
                    self.turn_cube("L")
                    self.move("D'")
                    corner_piece = self.cube[5:7,8:10]
                    needed_corner_colors = [self.cube[4,7],self.cube[4,10]]
                if self.cube[5,8] == top_middle_color:
                    self.do_algorithm("F,D,F'")
                elif self.cube[5,9] == top_middle_color:
                    self.do_algorithm("R',D',R")
                elif self.cube[6,8] == top_middle_color:
                    self.do_algorithm("R',D,D,R,D,R',D',R")
            elif np.any(self.cube[3,:] == top_middle_color):
                while self.cube[3,8] == self.cube[4,7]:
                    self.turn_cube("R")
                if self.cube[3,8] == top_middle_color:
                    self.do_algorithm("F,D,F',D',F,D,F'")
                elif self.cube[3,9] == top_middle_color:
                    self.do_algorithm("R',D',R,D',R',D',R")
                else:
                    self.do_algorithm("R',D',R")
            else:
                while self.cube[3,8] == self.cube[4,7]:
                    self.turn_cube("R")
                self.do_algorithm("R',D',R")
    def solve_middle_edges(self):
        bottom_middle_color = self.cube[7,7]
        def middle_edges_solved():
            c=self.cube
            e1=c[4,8]==c[4,7] and c[4,9]==c[4,10]
            e2=c[4,11]==c[4,10]and c[4,0]==c[4,1]
            e3=c[4,2]==c[4,1] and c[4,3]==c[4,4]
            e4=c[4,5]==c[4,4] and c[4,6]==c[4,7]
            return e1 and e2 and e3 and e4
        while not middle_edges_solved():
            if bottom_middle_color not in self.cube[4,:]:
                self.do_algorithm("F,D,F',D',R',D',R")
            else:
                while bottom_middle_color in self.cube[[0,8],7]:
                    self.move("D'")
                front_middle_color = self.cube[4,7]
                while front_middle_color not in self.cube[[0,8],7]:
                    self.move("D");self.turn_cube("Y'")
                    front_middle_color = self.cube[4,7]
                    input("self.cube[4,7]: " + str(self.cube[4,7]))
                left_middle_color = self.cube[4,4]
                if self.cube[5,1] == left_middle_color:
                    self.do_algorithm("F',D',F,D,L,D,L'")
                else:
                    self.do_algorithm("F,D,F',D',R',D',R")
            self.parent.display.update_stickers()
            return
