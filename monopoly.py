#import relavant libraries
import csv
import random
from numbers import Number
import ctypes
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.animation as animation
from matplotlib import style


#board is empty until the .csv is imported
board = []

def bubble_sort(list): #function to sort objects by number of times stopped on
    for i, num in enumerate(list): #itterate through indexes of the list
        numstops = num.stops  #numstops is number of stops of the current index
        try: #try to index the next value in list, skip if no more index
            if list[i+1].stops < numstops: #compare num value to each value of i until it is smaller
                list[i] = list[i+1]  #if it is swap the twp
                list[i+1] = num 
                bubble_sort(list) #call recursively for next index
        except IndexError: #if no more index, exit, change to if len = 1
            pass
    return list #return sorted list


def showresults(list):
    results = [] #initiate empty array to store results
    i = 0 #i is a counter
    while i < len(list):#loop for every index in board[]
        print(list[i].name, "was stepped on ", list[i].stops," times.")#print the number of stops
        results.append(list[i].stops)#add number of stops in the array
        i += 1
    print(results)

def sortedresults(list):
    results = []
    i = 0
    bubble_sort(list)
    while i < len(list):
        print(list[i].name, "was stepped on ", list[i].stops," times.")
        results.append(list[i].stops)
        i += 1
    print(results)

def plotgraph():
    properties = []
    stops = []
    i = 0
    while i < len(board):
        properties.append(board[i].name)
        stops.append(board[i].stops)
        i = i + 1

    y_pos = np.arange(len(properties))
    plt.bar(y_pos, stops, align='center', alpha=0.5)
    plt.xticks(y_pos, properties,rotation='vertical')
    plt.ylabel('Stops')
    plt.title('Property')
    plt.show()


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
        print("Unkown error, unable to initialise board") #if error found, error passed validation therefore its unkown.

def resetdeck(deck):
    if deck == "chest":
        master_chest = [0,40,40,40,40,10,40,40,40,40,40,40,40,40,40,40] #sorted chest deck
        chest = [i for i in master_chest] #copy sorted chest into new chest that will be shuffled
        shuffledeck(chest)
        return chest
    elif deck == "chance":
        master_chance = [0,24,11,'Utility','Railroad',40,40,'Back',10,40,40,5,39,40,40,40]#sorted chance deck
        chance = [i for i in master_chance] #copy sorted chance into new chest that will be shuffled
        shuffledeck(chance)
        return chance





def monopolyrun():#version of the game where one player continuesly travels around the board
    #####################################################################
    # Start menu, input rules and stuff
    finished = int(input("How many games do you want to simulate?"))
    turns = int(input("How many turns per game?"))
    results_sort = 0
    while not (results_sort == 'y' or results_sort == 'n'):
        results_sort = input("Sort the array by stops? \n (y/n)>>  ")
    #####################################################################

    games_played = 0 #reset how many games have been played
    while games_played < finished: #while games played is less then set number of games, play another one
        
        chest = resetdeck("chest")
        chance = resetdeck("chance")

        #new game declare variables
        doubles = 0
        position = 0
        gos = 0

        while gos < turns: #while number of gos is less then set, play more turns

            position = diceroll(position) #call diceroll passing the current position

            if board[position].name == "Chance": #if board position is a chance
                card = chance.pop(0)    #take a card from the end of the deck
                if len(chance) == 0:    #if the deck is empty, reshuffle from master chest
                    resetdeck(chance)
                if card != 40:  #if card is not "go to Go" (index 0 = 40%40)
                    if isinstance(card,int):#if the card is integer, move to the position shown by the card
                        position = card
                    elif card == "Utility": #if card is utility
                        while board[position].type != "utility":#move to next closesed utility
                            position = (position+1)%40
                    elif card == "Railroad":
                        while board[position].type != "railroad":#move to next closesed railroad
                            position = (position+1)%40
                    elif card == "Back":#if card is back, move three positions backwards
                        position = position - 3
            
            elif board[position].name == "Community Chest": #if stepped on Community chest
                card = chest.pop(0)#pull chest card from top of deck
                if len(chest) == 0:#if deck is empty, reshuffle
                    resetdeck(chest)
                if card != 40:#if card is not "go to Go" (index 0 = 40%40)
                    position = card
            
            if board[position].name == "Go to Jail":#if card is go to jail, move to position 10 (Jail)
                position = 10
            
            board[position].stops += 1 #add one stop to position where the player ends his turn
            print(board[position].name) #print position at which the player ended that turn)
            gos += 1 #increment gos
        games_played +=1 #after a game is ended, incremenet number of games played

    if results_sort == 'y':
        sortedresults(board)
    elif results_sort == 'n':
        showresults(board)
    else:
        print('Error')
    













#verify the csv file, and initialise board
verify("properties.csv")
monopolyrun()
plotgraph()
##############
