# Gabriel Bettio | 20010878 | 15gb24@queensu.ca | CMPE365
# 'I certify that this submission contains my own work, except as noted.'


# Read file, determine number of destinations and total number of flights
file1 = open("2019_Lab_2_flights_real_data.txt", "r")
firstLine = file1.readline().split()
numCity = int(firstLine[0])
numFlt = sum(1 for line in open("2019_Lab_2_flights_real_data.txt")) - 1

# Variable Inputs for flight departure and destination
tarDep = 78              # Target Departure City (78)
tarDest = 8             # Target Destination City (08)

# Deals with special case where departure and destination cities are the same
if tarDep == tarDest:
    print 'No need to go anywhere!'
    exit()

# Split file to generate flight information matrix (OrigMatrix)
lines = file1.readlines()
OrigMatrix = [0 for x in range(numFlt)]
for x in range(numFlt):
    OrigMatrix[x] = [int(z) for z in lines[x].split()]

# Generate 2D matrix of lists to later become weighted adjacency matrix
W = [[[] for x in range(numCity)] for y in range(numCity)]

# Cycle through original matrix to populate adjacency matrix with arrival and departure time tuples
for x in range(numFlt):
    if W[OrigMatrix[x][0]][OrigMatrix[x][1]]:
        tup = (OrigMatrix[x][2], OrigMatrix[x][3])
        W[OrigMatrix[x][0]][OrigMatrix[x][1]].append(tup)
    else:
        W[OrigMatrix[x][0]][OrigMatrix[x][1]] = [tuple((OrigMatrix[x][2], OrigMatrix[x][3]))]

# Initialize lists used in Dijkstra's Algorithm
Cost = [(0, 0)]
Reached = [None] * numCity
Estimate = [None] * numCity
Candidate = [None] * numCity
Predecessor = [-1] * numCity
Reached[tarDep] = True

# Set initial conditions for departure city
for x in range(numCity):
    if not Reached[x]:
        Reached[x] = False

for x in range(numCity):
    if W[tarDep][x] != []:
        Estimate[x] = W[tarDep][x]
        Candidate[x] = True
        Predecessor[x] = tarDep
    else:
        Estimate[x] = [(0, float("inf"))]
        Candidate[x] = False


# Dijkstra's Algorithm Implementation

# Run while loop until algorithm has reached destination city
while not Reached[tarDest]:

    bestEst = (0, float("inf"))

    # Determine next flight based on the flight with lowest arrival time
    # Two for loops required since certain flights have multiple weights
    for x in range(numCity):
        for y in range(len(Estimate[x])):
            if Candidate[x] and Estimate[x][y][1] < bestEst[1]:
                m = x
                n = y
                bestEst = Estimate[x][y]

    # if multiple flights on same line, ensure correct tuple is chosen
    if len(Estimate[m]) > 1:
        Cost.append(Estimate[m][n])
        Estimate[m] = [Estimate[m][n]]

    # Case where there is only one tuple in the Estimate list
    else:
        Cost.append(Estimate[m][0])

    # Set shortest path vertex to reached and make is no longer a candidate
    Reached[m] = True
    Candidate[m] = False

    # Check for condition that there are no more candidates since the desired node is unreachable (exit while loop)
    if bestEst == (0, float("inf")):
        break

    # Update Estimates based on information from the shortest path chosen above
    # Check that cell is populated and that the city has not yet been reached
    # Separate into case where cell has multiple tuples versus when a cell has a single tuple
    # If multiple tuples exist, for loop is required to iterate through each tuple
    # Verify that cell has lower arrival time than current Estimate and that the departure is after the previous arrival
    # time
    for i in range(numCity):
        if W[m][i] != [] and Reached[i] == False:
            if len(W[m][i]) > 1:
                for j in range(len(W[m][i])):
                    if W[m][i][j][1] < Estimate[i][0][1] and Cost[len(Cost) - 1][1] < W[m][i][j][0]:
                        Estimate[i] = [W[m][i][j]]
                        Candidate[i] = True
                        Predecessor[i] = m
                        v = i

            # Case where there is a single tuple
            else:
                if W[m][i][0][1] < Estimate[i][0][1] and Cost[len(Cost) - 1][1] < W[m][i][0][0]:
                    Estimate[i] = W[m][i]
                    Candidate[i] = True
                    Predecessor[i] = m
                    v = i

# Function designed to output correct flight path from Departure city to Destination city
def flightPath(listPred, departureCity, destinationCity, bestEstimate):

    # Initial conditions
    previous = destinationCity
    string = 'Optimal route from {} to {}\n\n'.format(departureCity,destinationCity)
    text = ['\nArrive at {} at time {}'.format(destinationCity, Cost[len(Cost) - 1][1])]

    # Case where destination city is unreachable
    if bestEst == (0, float("inf")):
        return 'There is no possible connection from {} to {}'.format(departureCity,destinationCity)

    # Work backwards from destination city to departure city using predecessor list
    while previous != departureCity:
        text.append('Fly From {} to {} \n'.format(listPred[previous], previous))
        previous = listPred[previous]

    # Put all expressions generated from previous while loop into a single string to be printed
    q = len(text) - 1
    while q >= 0:
        string += text[q]
        q = q - 1


    return string


# Call function flightPath to print desired route
print flightPath(Predecessor, tarDep, tarDest, bestEst)

