#import relavant libraries
import csv
import random
from numbers import Number
import ctypes
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.animation as animation
try: from matplotlib import style
except:
    pass


def bubble_sort(list): #function to sort objects by number of times stopped on
    for i, num in enumerate(list): #itterate through indexes of the list
        numstops = num.stops  #numstops is number of stops of the current index
        try: #try to index the next value in list, skip if no more index
            if list[i+1].stops < numstops: #compare num value to each value of i until it is smaller
                list[i] = list[i+1]  #if it is swap the tmp
                list[i+1] = num 
                bubble_sort(list) #call recursively for next index
        except IndexError: #if no more index, exit
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
        #print(list[i].name, "was stepped on ", list[i].stops," times.")
        results.append(list[i].stops)
        i += 1
    #print(results)

def plotgraph(board):
    properties = []
    stops = []
    counter = 0
    while counter < len(board):
        properties.append(board[counter].name)
        stops.append(board[counter].stops)
        counter = counter + 1

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
        self.owner = "Bank"

class Player:
    def __init__(self,name, minbalance):
        self.name = name
        self.balance = 1500
        self.position = 0
        self.jail_pass = 0
        self.jailed = False
        self.minbalance = minbalance
        self.wins = 0

#dice roll
def diceroll(position,doubles):

    dice1 = random.randint(1,6) 
    dice2 = random.randint(1,6)
    totalroll = dice1 + dice2

    if dice1 == dice2: #if double roll
        try:
            doubles = doubles + 1 #increase double count by one
            diceroll(position,doubles)
        except:
            doubles = 1
            diceroll(position,1)
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
    else:
        error = "Errors found are: " + str(error) #still need to clean up the error array
        ctypes.windll.user32.MessageBoxW(0, error, "Warning", 1) #make alert box displaying error messages
        

def createboard(csv_file):
    board = []
    board.clear
    file = open(csv_file) #open file
    csv_file = csv.reader(file) #open file in reader
    next(csv_file) #skips header row

    try:#try to create board
        for row in csv_file: #for each row in the file
            p = row
            base = Property(p[0],p[1],p[2],p[3],p[4]) # create starting property with its properties from csv on the board, in order
            board.append(base)
        print("Board succesfully initialised") #output succesful board initialisation
        return board
    except:
        print("Unkown error, unable to initialise board") #if error found, error passed validation therefore its unkown.

def resetdeck(deck):
    if deck == "community":
        starting_community = {0,"Go to Go and Collect 200","Pay 50","Collect 50","Get Out of Jail Free",10,"Collect 50","Collect 100","Collect 20","Collect 100","Pay 50","Pay 50","Collect 25","Pay $40 per property","Collect 10","Collect 100"} #sorted community deck
        community = [i for i in starting_community] #copy sorted community into starting community that will be shuffled
        community = shuffledeck(community)
        return community
    elif deck == "chance":
        starting_chance = {0,24,11,'Utility','Railroad',"Collect 50","Get out of Jail Free",'Back',10,"Pay 25 per property","Pay 15",5,39,"Pay 50","Collect 50","Collect 100"}#sorted chance deck
        chance = [i for i in starting_chance] #copy sorted chance into starting community that will be shuffled
        chance = shuffledeck(chance)
        return chance




# def monopolyrun():#version of the game where one player continuesly travels around the board
#     #####################################################################
#     # Start menu, input rules and stuff
#     finished = int(input("How many games do you want to simulate?"))
#     turns = int(input("How many turns per game?"))
#     results_sort = 0
#     while not (results_sort == 'y' or results_sort == 'n'):
#         results_sort = input("Sort the array by stops? \n (y/n)>>  ")
#     #####################################################################

#     games_played = 0 #reset how many games have been played
#     while games_played < finished: #while games played is less then set number of games, play another one
        
#         community = resetdeck("community")
#         chance = resetdeck("chance")

#         #starting game declare variables
#         doubles = 0
#         position = 0
#         gos = 0

#         while gos < turns: #while number of gos is less then set, play more turns

#             position = diceroll(position,0) #call diceroll passing the current position

#             if board[position].name == "Chance": #if board position is a chance

#                 card = chance.pop(0)    #take a card from the end of the deck
#                 if len(chance) == 0:    #if the deck is empty, reshuffle from starting community
#                     chance = resetdeck("chance")
                    
#                 if isinstance(card,int):#if the card is integer, move to the position shown by the card
#                     position = card
                
#                 elif card == "Railroad":
#                     while board[position].type != "railroad":#move to next closesed railroad
#                         position = (position+1)%40

#                 elif card == "Utility": #if card is utility
#                     while board[position].type != "utility":#move to next closesed utility
#                         position = (position+1)%40
                
#                 elif card == "Back":#if card is back, move three positions backwards
#                     position = position - 3
#                 else:
#                     position = position
                        
            
#             elif board[position].name == "Community chest": #if stepped on Community community
#                 card = community.pop(0)#pull community card from top of deck
#                 if len(community) == 0:#if deck is empty, reshuffle
#                     community = resetdeck("community")
#                 if isinstance(card,int):
#                     position = card
#                 else:
#                     position = position
            
#             if board[position].name == "Go to Jail":#if card is go to jail, move to position 10 (Jail)
#                 position = 10
            
#             board[position].stops += 1 #add one stop to position where the player ends his turn
#             print(board[position].name) #print position at which the player ended that turn)
#             gos += 1 #increment gos
#         games_played +=1 #after a game is ended, incremenet number of games played

#     if results_sort == 'y':
#         sortedresults(board)
#     elif results_sort == 'n':
#         showresults(board)
#     else:
#         print('Error')
    

def getposition(board,chance, community, player):

    position = player.position
    position = diceroll(position,0) #call diceroll passing the current position

    if board[position].name == "Chance": #if board position is a chance
        card = chance.pop(0)    #take a card from the end of the deck
        if len(chance) == 0:    #if the deck is empty, reshuffle from starting community
            chance = resetdeck("chance")
        if isinstance(card,int):#if the card is integer, move to the position shown by the card
            position = card
        elif card == "Utility": #if card is utility
            while board[position].type != "utility":#move to next closesed utility
                position = (position+1)%40
                if position == 0:
                    player.balance = player.balance + 200
        elif card == "Railroad":
            while board[position].type != "railroad":#move to next closesed railroad
                position = (position+1)%40
                if position == 0:
                    player.balance = player.balance + 200
        elif card == "Back":#if card is back, move three positions backwards
            position = position - 3

        

    elif board[position].name == "Community chest": #if stepped on Community community
        card = community.pop(0)#pull community card from top of deck
        if len(community) == 0:#if deck is empty, reshuffle
            community = resetdeck("community")
        if isinstance(card,int):
            position = card
        
        elif card == "Go to Go and Collect 200":
            position = 0
            player.balance = player.balance + 200

        elif card == "Pay 50":
            player.balance = player.balance - 50

        elif card == "Get out of Jail Free":
            player.jail_pass = 1

        elif card == "Pay 15":
            player.balance = player.balance - 15
        
        elif card == "Collect 50":
            player.balance = player.balance + 50

        elif card == "Collect 100":
            player.balance = player.balance + 100
        
        elif card == "Collect 20":
            player.balance = player.balance + 20
        
        elif card == "Pay $40 per property":
            #TODO
            pass
        elif card == "Collect 10":
            player.balance = player.balance + 10

    
    if board[position].name == "Go to Jail":#if card is go to jail, move to position 10 (Jail)
        position = 10
        player.jailed = True
        if player.jail_pass > 0:#use get out of jail card
            player.jailed = False
            player.jail_pass = player.jail_pass - 1

    
    if position >=40:#get 200 after passing go
        player.balance = player.balance + 200
    position = position%40
    board[position].stops += 1 #add one stop to position where the player ends his turn
    
    return(position) #print position at which the player ended that turn)




def strategymonopoly():

############################################################OPTIONS##############################################################################
    #initiate number of players
    validation = False
    while validation == False:
        n_players = input("How many players do you want to simulate? (Must be an integer) \n >>")
        try:
            n_players = int(n_players)
            if n_players < 2:
                print("Only one player selected. Do you want to simulate just one player traveling around the board? (y/n)")
                answer = input(">>")
                if answer == "y":
                    monopolyrun()
                    validation == True
                else:
                    while validation == False:
                        print("Try inputing a number of players again (min 2)")
                        try:
                            answer = int(input("How many players do you want to simulate? (Must be an integer) \n >>"))
                            if answer >= 2:
                                n_players = answer
                                validation = True
                            else:
                                RuntimeError
                        except:
                            validation = False
                    
            n_players = int(n_players)
            validation = True
            print("Number of players is ", n_players)
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
            if players_with_minbalance > n_players:
                print("Input cannot be more then the number of players")
                players_with_minbalance = "error"
            
            players_with_minbalance = int(players_with_minbalance)
            validation = True
            print("Number of players with minimal balance ", players_with_minbalance)
        except:
            validation = False
   
    players = []
    playercounter = 0
    i = 0

    #create players
    while i < players_with_minbalance:
        player = Player(playercounter+1,(random.randint(0,15)*100))
        players.append(player)
        i = i + 1
        playercounter = playercounter + 1

    while playercounter < n_players:
        player = Player(playercounter+1,0)
        players.append(player)
        playercounter = playercounter + 1
    
    #print all the players and their atributes
    i = 0    
    print("The player list is as follows:")
    for i in range (0,len(players)):
        print("_________________________________________________________")
        print("Player name: Player", players[i].name)
        print("Player minbalance = ", players[i].minbalance)
        i = i + 1
    
    n_games = input("How many games do you wish to simulate?")
    validation = False
    while validation == False:
        try:
            if(int(n_games)>0):
                validation = True
            else:
                n_games = "error"
            n_games = int(n_games)
        except:
            n_games = int(input("How many games do you wish to simulate? (Must be a positive integer)"))
################################################################################################################################################

    gamesplayed = 0
    boardsum = []
    text_file = open("Output.txt", "w")
    while gamesplayed < n_games :
        #start new game
        #reset players game values, 
        #keeping their strategy and wins
        k = 0 #counters
                
        board = createboard("properties.csv")
        player = players[k]
        while k < len(players):
            player = players[k]
            player.balance = 1500
            player.position = 0
            player.jail_pass = 0
            player.jailed = False
            k = k + 1


        community = resetdeck("community")
        chance = resetdeck("chance")
        playersout = []
        k = 0 #counter
        i = 0 #counter of player
        j = 0 #counter
        gos = 0
        position = 0
        turn = 0
        

        #while there are more then 1 player left (when there is one, that one is the winner)
        while len(players)>1:
            #assign the correct class of player[i] to player for this turn
            player = players[i]
            #get position of player
            if player.jailed == False:#if the player is not in jail, if he is, skip turn
                
                player.position = getposition(board,chance,community,player)
                
                print("Player_",player.name, " is on position ", board[player.position].name)#print
                message = str("\nPlayer_" + str(player.name) + " is on position " + str(board[player.position].name))
                text_file.write(message)

                if len(chance) == 0:    #if the deck is empty, reshuffle from starting community
                    chance = resetdeck("chance")
                if len(community) == 0:    #if the deck is empty, reshuffle from starting community
                    community = resetdeck("community")
                
                #if the board type is not a base item, it can be bought)
                if board[player.position].type != "base":
                    
                    if(board[player.position].owner != "Bank"): #if the bank is not the owner, a player is
                        player.balance = player.balance - int(board[player.position].rent)  #player pays rent
                        j = 0
                        while players[j].name != board[player.position].owner:  #find the player who's property this is
                            j = (j + 1)%len(players)
                        players[j].balance = players[j].balance + int(board[player.position].rent)#pay that player the rent
                        print("Player_", player.name, " payed ", int(board[player.position].rent), "$ to ", "Player_",players[j].name)
                        message = "\nPlayer_"+ str(player.name)+ " payed "+ str(board[player.position].rent)+ "$ to Player_" + str(players[j].name)
                        text_file.write(message)
                        
                        j = 0#reset j

                    if board[player.position].owner == "Bank":#if the bank owns the property
                        #player buys property
                        if player.balance > int(board[player.position].cost):#if player has enough money
                            if (int(player.balance) - int(board[player.position].cost)) > player.minbalance:#if the players minimum balance atribute is lower then the money he will have after buying the property
                                board[player.position].owner = player.name#trasnfer ownership to player
                                player.balance = player.balance - int(board[player.position].cost)#player pays the cost of property
                                print("Player_", player.name," bought ", board[player.position].name)#output the purchase in terminal
                                message = str("\nPlayer_"+ str(player.name)+" bought "+ str(board[player.position].name))
                                text_file.write(message)
                            else:
                                pass#player does not have enough money to buy the property
            
                elif board[player.position].type == "base":#if the property cannot be bought
                    #if the property cannot be bought, player pays the fee of it (in case of Go fee is -200 which ads 200 to the players budget)
                            player.balance = player.balance - int(board[player.position].rent)
                print("_________________________________________________________This was turn number ",gos, "In game ",gamesplayed + 1 )  
                message = str("\n_________________________________________________________This was turn number "+ str(gos) + "In game "+ str(gamesplayed + 1))
                text_file.write(message)   

                if player.balance < 0:#if the player is bankrupt
                    j = 0
                    while j < 40:#transfer ownership of bakrupt player to the player he ows rent
                        if board[j].owner == player.name:
                            board[j].owner = board[player.position].owner
                        j = (j + 1)
                    print("Player_",player.name," could not pay Player", board[player.position].owner , " and has lost.")
                    message = str("\nPlayer_" + str(player.name) +" could not pay Player"+ str(board[player.position].owner) + " and has lost.")
                    text_file.write(message)
                    playersout.append(player)
                    players.pop(i)#remove player from game
                    i = (i-1)%len(players)#mod used to circle back to 
                                        #first player if the player was last in array
                else:
                    i = (i + 1)%len(players)

            else:#remove player from jail after skipped turn
                player.jailed = False
            gos = gos + 1

        print("Winner = ", players[0].name)
        text_file.write("\nWinner = " + str(players[0].name))
        players[0].wins = players[0].wins + 1
        gamesplayed = gamesplayed + 1
        players = players + playersout
        playersout.clear
        while k < len(board):
            try:
                boardsum[k].stops = boardsum[k].stops + board[k].stops
            except IndexError:
                boardsum = board
                k = 100
                print(boardsum)
            k = k + 1
        print(boardsum)
    
    #sort players by number of wins
    counter = len(players)
    # Traverse through all array elements
    for i in range(counter):
        # Last i elements are already in place
        for j in range (0,counter - i - 1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if players[j].wins < players[j+1].wins:
                players[j], players[j+1] = players[j+1], players[j]


    for i in range(0,counter):
        print("Wins of player ", players[i].name, ": ", players[i].wins)    
        #add sum of each visitt of property after all games
    sortedresults(boardsum)
    plotgraph(boardsum)
    plt.close()


#verify the csv file, and initialise board
verify("properties.csv")
strategymonopoly()
