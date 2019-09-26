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
    def __init__(self,name, cost, type, rent, color):
        self.name = name
        self.cost = cost
        self.type = type
        self.rent = rent
        self.color = color
        self.stops = 0

class Player:
    def __init__(self,name, preforder, minbalance):
        self.name = name
        self.balance = 1500
        self.position = 0
        self.jail_pass = 0
        self.preforder = preforder
        self.minbalance = minbalance

#dice roll
def diceroll(position):
    
    dice1 = random.randint(1,6) 
    dice2 = random.randint(1,6)
    totalroll = dice1 + dice2

    if dice1 == dice2: #if double roll
        try:
            doubles = doubles + 1 #increase double count by one
            diceroll(position)
        except:
            doubles = 1
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
    return list

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
        color = row[4]

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
            base = Property(p[0],p[1],p[2],p[3],p[4]) # create starting property with its properties from csv on the board, in order
            board.append(base)
        print("Board succesfully initialised") #output succesful board initialisation
    except:
        print("Unkown error, unable to initialise board") #if error found, error passed validation therefore its unkown.

def resetdeck(deck):
    if deck == "community":
        starting_community = [0,"Go to Go and Collect 200","Pay 50","Collect 50","Get Out of Jail Free",10,"Collect 50","Collect 100","Collect 20","Collect 100","Pay 50","Pay 50","Collect 25","Pay $40 per property","Collect 10","Collect 100"] #sorted community deck
        community = [i for i in starting_community] #copy sorted community into starting community that will be shuffled
        community = shuffledeck(community)
        return community
    elif deck == "chance":
        starting_chance = [0,24,11,'Utility','Railroad',"Collect 50","Get out of Jail Free",'Back',10,"Pay 25 per property","Pay 15",5,39,"Pay each player 50","Collect 50","Collect $100"]#sorted chance deck
        chance = [i for i in starting_chance] #copy sorted chance into starting community that will be shuffled
        chance = shuffledeck(chance)
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
        
        community = resetdeck("community")
        chance = resetdeck("chance")

        #starting game declare variables
        doubles = 0
        position = 0
        gos = 0

        while gos < turns: #while number of gos is less then set, play more turns

            position = diceroll(position) #call diceroll passing the current position

            if board[position].name == "Chance": #if board position is a chance

                card = chance.pop(0)    #take a card from the end of the deck
                if len(chance) == 0:    #if the deck is empty, reshuffle from starting community
                    chance = resetdeck("chance")
                if card != 40:#if card is a card that moves a player (40 is a placeholder card that keeps the player on the community community square)
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
            
            elif board[position].name == "Community community": #if stepped on Community community
                card = community.pop(0)#pull community card from top of deck
                if len(community) == 0:#if deck is empty, reshuffle
                    community = resetdeck("community")
                if card != 40:#if card is a card that moves a player (40 is a placeholder card that keeps the player on the community community square)
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
    

def position(chance, community, player):

    position = diceroll(position) #call diceroll passing the current position

    if board[position].name == "Chance": #if board position is a chance

        card = chance.pop(0)    #take a card from the end of the deck
        if len(chance) == 0:    #if the deck is empty, reshuffle from starting community
            chance = resetdeck("chance")
        if card != 40:#if card is a card that moves a player (40 is a placeholder card that keeps the player on the community community square)
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
    
    elif board[position].name == "Community community": #if stepped on Community community
        card = community.pop(0)#pull community card from top of deck
        if len(community) == 0:#if deck is empty, reshuffle
            community = resetdeck("community")
        if card != 40:#if card is a card that moves a player (40 is a placeholder card that keeps the player on the community community square)
            position = card
    
    if board[position].name == "Go to Jail":#if card is go to jail, move to position 10 (Jail)
        position = 10
    
    board[position].stops += 1 #add one stop to position where the player ends his turn
    print(board[position].name) #print position at which the player ended that turn)
    gos += 1 #increment gos




def strategymonopoly():

    #initiate number of players
    validation = False
    while validation == False:
        n_players = input("How many players do you want to simulate? (Must be an integer) \n >>")
        try:
            n_players = int(n_players)
            if n_players < 2:
                print("Must be at least 2 players")
                n_players = "error"
            n_players = int(n_players)
            validation = True
            print("Number of players is ", n_players)
        except:
            validation = False

    validation = False
    while validation == False:
        players_with_logic = input("How many players have prefered properties? \n >>")
        try:
            players_with_logic = int(players_with_logic)
            if players_with_logic < 0:
                print("Input must be a positive integer, try again. \n ")
                players_with_logic = "error"
            if players_with_logic > n_players:
                print("Number exceeds the total number of players, which is ", n_players)
                players_with_logic = "error"
            players_with_logic = int(players_with_logic)
            validation = True
            print("Number of players with prefered properties ", players_with_logic)
        except:
            validation = False

    validation = False
    while validation == False:
        players_with_minbalance = input("How many players have a minimum balance?\n >>")
        try:
            players_with_minbalance = int(players_with_minbalance)
            if players_with_minbalance < 0:
                print("Input must be a positive integer, try again.\n")
                players_with_minbalance = "error"
            if (players_with_minbalance + players_with_logic) > n_players:
                print("Number or players exceeds the total number of players, Players available = ", (n_players - players_with_logic))
                players_with_minbalance = "error"
            players_with_minbalance = int(players_with_minbalance)
            validation = True
            print("Number of players with minimal balance ", players_with_minbalance)
        except:
            validation = False

    validation = False
    while validation == False:
        players_with_both = input("How many player with both prefered properties and minimum balance?\n >>")
        try:
            players_with_both = int(players_with_both)
            if players_with_both < 0:
                print("Input must be a positive integer, try again.\n")
                players_with_both = "error"
            available = n_players - players_with_logic - players_with_minbalance
            if players_with_both > (available):
                print("Number of players exceeds the possible number, Players available = ", (available))
                players_with_both = "error"
            players_with_both = int(players_with_both)
            validation = True
            print("Number of players with both atributes is ", players_with_both)
            dummies = n_players - players_with_logic - players_with_minbalance - players_with_both
            print("Players left with random no strategy (buy every property they can afford) is ", dummies)
        except:
            validation = False
    
    
    players = []
    playercounter = 0
    i = 0

    while i < players_with_logic:
        player = Player(playercounter+1,True,0)
        players.append(player)
        i = i + 1
    playercounter = playercounter + i

    i = 0
    while i < players_with_minbalance:
        player = Player(playercounter+1,False,random.randint(0,100))
        players.append(player)
        i = i + 1
    playercounter = playercounter + i

    i = 0
    while i < players_with_both:
        player = Player(playercounter+1,True,random.randint(0,100))
        players.append(player)
        i = i + 1
    playercounter = playercounter + i

    while playercounter < n_players:
        player = Player(playercounter+1,False,random.randint(0,1500))
        players.append(player)
        playercounter = playercounter + 1
    

    i = 0    
    print("The player list is as follows:")
    for i in range (0,len(players)):
        print("_________________________________________________________")
        print("Player name: Player", players[i].name)
        print("Player has prefered properties: ", players[i].preforder)
        print("Player minbalance = ", players[i].minbalance)

        i = i + 1
#add change atributes for each player
#make function to call with (player,variable to change, change to value)



    







strategymonopoly()
#verify the csv file, and initialise board
#verify("properties.csv")
#monopolyrun()
#plotgraph()
##############
