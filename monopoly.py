#import relavant libraries
import csv
import random
from numbers import Number
import ctypes

board = []


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

    if dice1 == dice2: #if double roll
        doubles = doubles + 1 #increase double count by one
    else:
        doubles = 0
    if doubles >= 3: #if three doubles in a row, go to jail
        position = 10
        return position
    else:
        position = (position+totalroll)%40 #position is the position + roll, %40 allows continues travel around the board
        return position

def shuffledeck(list): #Fisher-Yates Shuffle applied
    #how many times to repeat the process, more iterations more shuffled the deck is
    pointer = len(list) - 1 #index of last value in array
    while pointer >= 0:     #loop for all values up to and including index 0
        i = pointer         #i is the value the current pointer is pointing at
        j = random.randint(0,pointer) #j is a random integer in the range from 0 to index of pointer
        temp = list[i] #store data at pointer to temp var
        list[i]=list[j] #swap the pointed data with the data in the random index
        list[j]=temp #add temp to the index of the data that was moved to pointer
        pointer = pointer - 1 #shuffle next index

def verify(csv_file): #verifies all the data is correct data type
    filename= csv_file #pass csv_file name to filename var
    file = open(filename) #open the file called by the name passed
    csv_file = csv.reader(file) #open file in reader
    next(csv_file) #skip the header row
    error = [] #array that will collect errors
    types = ["base","street","railroad","utility"] #accepted values for type

    for row in csv_file:  #assign each row in csv to variable with meaningful name
        name = row[0]
        cost = row[1]
        type = row[2]
        rent = row[3]

        try: #try convert cost to int from str
            cost = int(cost)
        except: #if cannot convert to int, add to errors
            message = "cost is not an interger" + " in square " + name
            error.append(message)

        if not type in types: #if type is not one of the acceptable ones, add error to array
            message = "type is not an correct type" + " in square " + name
            error.append(message)

        try: #try convert rent into integer
            rent = int(rent)
        except:#if cannot, add error to 
            message = "rent is not an interger" +  " in square " + name
            error.append(message)

    if len(error) < 1: #if there is no error close the file and createboard
        file.close()
        createboard(filename)
    else:
        error = "Errors found are: " + str(error) #still need to clean up the error array
        ctypes.windll.user32.MessageBoxW(0, error, "Warning", 1) #make alert box displaying error messages
        

def createboard(csv_file):
    file = open(csv_file) #open file
    csv_file = csv.reader(file) #open file in reader
    next(csv_file) #skips header row

    try:#try to create board
        for row in csv_file: #for each row in the file
            p = row
            base = Property(p[0],p[1],p[2],p[3]) # create new property with its properties from csv on the board, in order
            board.append(base)
        print("Board succesfully initialised") #output succesful board initialisation
    except:
        print("Unkown error, unable to initialise board")


#verify the csv file, and initialise board
verify("properties.csv")
#starting money
wallet = 1000
#board is empty until the .csv is imported

#####################################################################
# Start menu, input rules and stuff
finished = int(input("How many games do you want to simulate?"))
turns = int(input("How many turns per game?"))
#####################################################################


games_played = 0
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