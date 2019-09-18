import csv
from numbers import Number


class Property:
    def __init__(self,name, cost, type, rent):
        self.name = name
        self.cost = cost
        self.type = type
        self.rent = rent
        self.stops = 0

#starting atributes
wallet = 1000
board = []
rollvalues = [2,3,4,5,6,7,3,4,5,6,7,8,4,5,6,7,8,9,5,6,7,8,9,10,6,7,8,9,10,11,7,8,9,10,11,12]

n = 0

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


verify("properties.csv")