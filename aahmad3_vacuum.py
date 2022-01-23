from typing import TYPE_CHECKING
from vacuum import VacuumAgent
import random

class Aahmad3VacuumAgent(VacuumAgent):
    list_track = []
    def __init__(self):
        super().__init__()
        self.history_status = []
        self.history_location = []
        self.history_move = []
        self.count = 0
        self.track = 0
        self.not_bumped = True
        self.dirty = 0
        self.right = 25
        self.left = 25
        self.up = 25
        self.down = 25
        self.right2 = 33
        self.left2 = 33
        self.down2 = 33
        self.up2 = 33
        self.count2 = 0
        self.bumped = False
        self.dir_list = ["u", "d", "r", "l"]
        self.range = 0
        self.first = 2500
        self.second = 5000
        self.third = 7500
        self.num_dict = {}
        self.mem_dict = {}
        self.clean = 0


        # any initialization you want to do here

    def manipulation(self, move):
        moves = ["Right", "Up", "Down", "Left"]
        rand = random.randrange(0, len(moves) - 2)
        other_rand = random.randrange(0, len(moves) - 1)
        self.count2 = self.count2 + 1
        move = None
        if self.count2 <2:
            if self.history_move[len(self.history_move) - 1] == "Right":
                other_move = moves[rand]
                self.history_move.append(other_move)
                return other_move
            else:
                some_move = moves[other_rand]
                self.history_move.append(some_move)
                return some_move
        elif self.history_location[len(self.history_location) - 1] == "Bump":
            self.bumped = True
            self.not_bumped = False
            move = self.bump_walls()

        else:
            move = self.bump_walls()

        if self.count2 > 0:
            self.history_move.append(move)

            return move

    def bump_walls(self):
        move = self.history_move[len(self.history_move) - 1]
        last_move = None
        if len(self.history_move) - 2 > -1: 
            last_move = self.history_move[len(self.history_move) - 2]
        if last_move == "Suck":
            last_move = self.history_move[len(self.history_move) - 3]

        if move == "Suck":
            move = self.history_move[len(self.history_move) - 2]

        
        if self.bumped == True:


            if move == "Up":
                self.dir_list[0] = "Up"
                self.dir_list[1] = "Right"
                self.dir_list[2] = "Left"
                self.dir_list[3] = "Down"
            elif move == "Down":
                self.dir_list[0] = "Down"
                self.dir_list[1] = "Right"
                self.dir_list[2] = "Left"
                self.dir_list[3] = "Up"
            elif move == "Right":
                self.dir_list[0] = "Right"
                self.dir_list[1] = "Up"
                self.dir_list[2] = "Down"
                self.dir_list[3] = "Left"

            elif move == "Left":
                self.dir_list[0] = "Left"
                self.dir_list[1] = "Up"
                self.dir_list[2] = "Down"
                self.dir_list[3] = "Right"
            
            self.mem_dict[self.dir_list[0]] = 100
            self.mem_dict[self.dir_list[1]] = 2750
            self.mem_dict[self.dir_list[2]]= 2750

            self.bumped = False
            self.range = 7000
        if self.not_bumped ==  True:
            self.track = self.track + 1
            self.dir_list[0] = "Left"
            self.dir_list[1] = "Up"
            self.dir_list[2] = "Down"
            self.dir_list[3] = "Right"
            self.set_probability()
            self.range = 7500

        self.num_dict = self.mem_dict.copy()
        if move == "Down":
            self.num_dict["Up"] = 0
        elif move == "Right":
            self.num_dict["Left"] = 0
        elif move == "Up":
            self.num_dict["Down"] = 0
        elif move == "Left":
            self.num_dict["Right"] = 0

        rand = random.randint(0, self.range)
        first = self.num_dict[self.dir_list[0]]
        second = self.num_dict[self.dir_list[0]] + self.num_dict[self.dir_list[1]]
        third = self.num_dict[self.dir_list[2]] + self.num_dict[self.dir_list[1]] + self.num_dict[self.dir_list[0]]
        if rand < first:
            return self.dir_list[0]
        elif rand < second:
            return self.dir_list[1]
        elif rand <= third:
            return self.dir_list[2]
        else:
            return self.dir_list[3]

    

    def set_probability(self):
        self.mem_dict[self.dir_list[0]] = 2500
        self.mem_dict[self.dir_list[1]] = 2500
        self.mem_dict[self.dir_list[2]]= 2500
        self.mem_dict[self.dir_list[3]]= 2500
              
                

    def program(self, percept):
        moves = ["Right", "Left", "Up", "Down"]
        rand = random.randrange(0, len(moves))
        
        self.history_status.append(percept[0])

        self.history_location.append(percept[1])
        self.count = self.count + 1

        if percept[0] == "Dirty":
            self.history_move.append("Suck")
            return "Suck"
        else:
            move = moves[rand]
            if self.count == 1:
                self.history_move.append(move)
                
                return move
            
            else:
                for i in range(len(self.history_status)):
                    if self.history_status[i] == "Clean":
                        self.clean = self.clean + 1
                        self.dirty = 0
                    if self.clean >= 150 and self.count >= 100:
                        return "NoOp"
                    if self.clean >= 150 and self.count >= 200:
                        return "NoOp"
                    if self.count >= 540:
                        return "NoOp"
                    if self.history_status[i] == "Dirty":
                        self.clean = 0
                        self.dirty = self.dirty + 1

                final_data = self.manipulation(self.history_move[len(self.history_move) - 1])

                return final_data