import csv
import random
from random import shuffle
from numbers import Number



#starting money
wallet = 1000
#board is empty until the .csv is imported
board = []

games_played = 0

doubles = 0

finished = int(input("How many games do you want to simulate?"))
turns = int(input("How many turns per game?"))

#class initalises each square with its properties
class Property:
    def __init__(self,name, cost, type, rent):
        self.name = name
        self.cost = cost
        self.type = type
        self.rent = rent
        self.stops = 0

#dice roll
def diceroll(position):
    doubles = 0
    dice1 = random.randint(1,6) 
    dice2 = random.randint(1,6)
    totalroll = dice1 + dice2

    if dice1 == dice2:
        doubles = doubles + 1
    else:
        doubles = 0
    if doubles >= 3:
        position = 10
        return position
    else:
        position = (position+totalroll)%40
        return position

def shuffledeck(list):
    #how many times to repeat the process
    iteration = random.randint(2,50)
    temp = 0
    while iteration > 0:
        #random index i change positions with random index j
        for i in range (1, len(list)):
            for j in range (1,len(list)):
                temp = list[i]
                list[i]=list[j]
                list[j]=temp
            iteration = iteration - 1


def verify(csv_file):
    filename= csv_file
    file = open(filename)
    csv_file = csv.reader(file)
    next(csv_file)
    row_Num = 0
    error = []
    types = ["base","street","railroad","utility"]

    for row in csv_file:
        name = row[0]
        cost = row[1]
        type = row[2]
        rent = row[3]

        try:
            cost = int(cost)
        except:
            error.append("cost is not an interger")

        if not type in types:
            error.append("type is not an correct type")

        try:
            rent = int(rent)
        except:
            error.append("rent is not an interger")

    if len(error) < 1:
        file.close()
        createboard(filename)
    else:
        print(error)

def createboard(csv_file):
    file = open(csv_file)
    csv_file = csv.reader(file)
    next(csv_file) #skips header row

    for row in csv_file:
        p = row
        base = Property(p[0],p[1],p[2],p[3])
        board.append(base)
    print("Board succesfully initialised")

#verify the csv file, initialise board
verify("properties.csv")


while games_played < finished:

    master_chest = [0,40,40,40,40,10,40,40,40,40,40,40,40,40,40,40]
    chest = [i for i in master_chest]
    shuffledeck(chest)
    
    master_chance = [0,24,11,'Utility','Railroad',40,40,'Back',10,40,40,5,39,40,40,40]
    chance = [i for i in master_chance]
    shuffledeck(chance)
    
    doubles = 0
    position = 0
    gos = 0

    while gos < turns:
        position = diceroll(position)

        if board[position].name == "Chance":
            card = chance.pop(0)
            if len(chance) == 0:
                chance = [i for i in master_chance]
                shuffledeck(chance)
            if card != 40:
                if isinstance(card,int):
                    position = card
                elif card == "Utility":
                    while board[position].type != "utility":
                        position = (position+1)%40
                elif card == "Railroad":
                    while board[position].type != "railroad":
                        position = (position+1)%40
                elif card == "Back":
                    position = position - 3
        
        elif board[position].name == "Community Chest":
            card = chest.pop(0)
            if len(chest) == 0:
                chest = [i for i in master_chest]
                shuffledeck(chest)
            if card != 40:
                position = card
        
        if board[position].name == "Go to Jail":
            position = 10
        
        board[position].stops += 1
        print(board[position].name)
        gos += 1
    games_played +=1

results = []
i = 0
while i < len(board):
    print(board[i].name, "stepped: ", board[i].stops)
    results.append(board[i].stops)
    i += 1
print(results)