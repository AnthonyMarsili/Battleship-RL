# State space is the indexes (+1) of the ship locations list that are sunk
# The states are represented as tuples (e.x. the state (2,4) represents the state of the game where the 2nd and 4th ships are sunk)
# The initial state is no ships sunk, and that is represented as the tuple (0,)
# The action space is the set of possible shots the agent can take in each staticmethod
# Possible shots in a state are determined by subtracting the coordinates of the sunk ships from the list of all the coordinates on the board
# The actions that were already taken are also accounted for when choosing which action to take from a given state
# Adjusting the learning and exploring rate (exploring rate especially) can allow us to have different difficulties
# This program generates a list of actions that the agent will take to get to the goal state (i.e. all ships sunk)

import numpy as np
import random
from itertools import combinations
import time

class World:
    def __init__(self, userBoard):
        self.gameHeight = 8
        self.gameWidth = 8
        self.playerShipLocations = userBoard # a list of the locations of ships that the agent will attack
        self.shotsTaken = [] # initalizes the list of coordinates that will represent the agent's actions throughout the game
        self.possibleStates = self.getPossibleStates() # will hold a list of the possible states of the game, based on the number of the player's ships
        self.startState = (0,)
        self.currentState = self.startState # set the current state to the start state when this program starts
        self.goalState = self.determineGoalState() # based on the number of player ship's determine what the goal state will look like

    def getPossibleStates(self):
        num = 1 # initializes the number of possible states
        states = [(0,)] # a list of lists indicating the different ships that can be sunk, making up a state
        numberedShipLocations = []

        for i in range(len(self.playerShipLocations)):
            numberedShipLocations.append(i+1)

        for x in range(len(self.playerShipLocations)):
            comb = list(combinations(numberedShipLocations, x + 1))
            num += len(comb)
            for y in range(len(comb)):
                states.append(comb[y])

        return states # this is the list of tuples that represent the different states. E.x. [ (0,), (1,), (2,), (3,), (1,2), (1,3), (2,3), (1,2,3) ]

    def determineGoalState(self):
        goalState = []
        for i in range(len(self.playerShipLocations)):
            goalState.append(i+1)

        return tuple(goalState)

    def getPossibleActions(self): # returns a list of tuples where each tuple is a coordinate on the grid
        possibleActions = []

        for x in range(self.gameHeight):
            for y in range(self.gameWidth):
                possibleActions.append((x,y))

        return possibleActions

    def moveToNewState(self, action): # based on the current state and the action the agent just took, this function determines if it should move to a new state, and what that state would be
        self.shotsTaken.append(action) # register this actions as taken
        sunkNewShip = True # initalize
        reward = -1 # initalize and will be the reward if the shot is a miss
        newState = self.currentState # initalize

        # this part will check if a new ship was sunk and update the state accordingly

        for i in range(len(self.playerShipLocations)):
            if action in self.playerShipLocations[i]: # if we hit a ship
                reward = 0 # will be the reward if the shot is a hit
                for coordinate in self.playerShipLocations[i]: # check to see if we sunk that ship
                    if coordinate not in self.shotsTaken: # if we are still missing one, they still get the reward, but this does not register as a new ship being sunk, and so we do not move to the next state
                        sunkNewShip = False
                        break
                #newState = self.currentState + (i+1,) # NEED A NEW WAY TO MOVE TO THE NEXT STATE
                if sunkNewShip:
                    reward = 1 # will be the reward if the shot was a hit AND a ship was sunk
                    if self.currentState == self.startState: # if we are in the start state, we need to overwrite the tuple (0,) rather than add to it. The possible next states from the start state are (1,) , (2,) ,(3,) , etc.
                        newState = (i+1,)
                    else: # otherwise, we can just append the index of the sunken ship to the current state
                        newState = self.currentState + (i+1,)
                        newState = tuple(sorted(newState)) # we want this representation of the state to be sorted bc of how getPossibleStates works
                    break

        return newState, reward # return the new state (new state will be equal to old state if a new ship was not sunk) and the reward for entering that state


class Agent:
    def __init__(self, a, e, world: World):
        self.alpha = a # learning rate
        self.epsilon = e # the percent you want to explore
        self.world = world # store all the info about the world created in the instance of the World class
        self.gamma = 0.9
        self.Q_values = self.createQTable() # will hold the Q-values for each state-action pair
        self.numOfSteps = 0

    def createQTable(self): # the table that holds the Q-values will be set up as a dictionary where each key is a state and the value is another dictionary where each key is an action in that sate and each value is the Q-value for that state-action pair
        QTable = {}
        for state in self.world.possibleStates:
            QTable[state] = {}
            for x in range(self.world.gameHeight):
                for y in range(self.world.gameWidth):
                    QTable[state][(x,y)] = 0

        return QTable


    def getBestAction(self, state): # in a Q-learning algorithm, there are multiple times in each iteration when we need to determine the best possible action in a state. This function looks for the greatest value in a state's dictionary
        maxVal = np.NINF # initalize
        maxAction = None # initalize
        valuesForAllowedActions = [] # initalize
        allowedActions = self.world.getPossibleActions() # initalize a list of all the possible actions (initalizes to all coordinates on the grid)

        for action in self.world.shotsTaken: # remove any coordinates that have already been chosen from the list of possible actions
            if action in allowedActions:
                allowedActions.remove(action)

        for action in allowedActions: # grab the Q-value for all of the allowed actions from this state
            valuesForAllowedActions.append(self.Q_values[state][action])

        for i in range(len(allowedActions)): # find the allowed action with the highest Q-value for this state
            if valuesForAllowedActions[i] > maxVal:
                maxVal = valuesForAllowedActions[i]
                bestAction = allowedActions[i]

        return bestAction # return the optimal action to take from this state

    def chooseAction(self, state): # this function will select the action that the agent will take in the current state
        allowedActions = self.world.getPossibleActions() # initalize a list of all the possible actions (initalizes to all coordinates on the grid)

        for action in self.world.shotsTaken: # remove any coordinates that have already been chosen from the list of possible actions
            if action in allowedActions:
                allowedActions.remove(action)

        action = None # initializing the return

        randomNum = np.random.rand() # generating a random number to determine if we will choose the optimal action from this state, or explore to find a random action

        # this is the epsilon-greedy policy:
        if(randomNum < self.epsilon): # this is why a higher epislon value will give a higher rate of exloration
            subOptimalActionChoiceIndex = random.randint(0, len(allowedActions) - 1) # not using np here because the random library was more suitable here
            action = allowedActions[subOptimalActionChoiceIndex]
        else:
            action = self.getBestAction(state)

        return action # returns an action that has not been taken before

    def Qlearning(self):
        self.world.currentState = (0,)
        # visited = []
        self.world.shotsTaken = []
        newStateAndReward = None # initialize
        converged = True # currently not using this

        while True: # loop for each step of the episode
            # Choose A from S using the epislon-greedy policy
            chosenAction = self.chooseAction(self.world.currentState)
            # Take A and observe R and S'
            newStateAndReward = self.world.moveToNewState(chosenAction)
            newState = newStateAndReward[0]
            reward = newStateAndReward[1]
            # visited.append(newState) # say we vsited that state
            self.numOfSteps += 1

            if newState == self.world.goalState: # if the next state is the goal, break
                return converged #currently not using this
            # find best action from S'

            bestAction = self.getBestAction(newState)

            oldQ = self.Q_values[self.world.currentState][chosenAction]

            # update current state q-value
            self.Q_values[self.world.currentState][chosenAction] += self.alpha * (reward + self.gamma * self.Q_values[newState][bestAction] - self.Q_values[self.world.currentState][chosenAction]) # perform the update

            if(abs(oldQ - self.Q_values[self.world.currentState][chosenAction]) < 0.001):
                converged = False

            self.world.currentState = newState

def mainAttack(userBoard, diff):
    if (diff == 1):
        eps = 0.8
    elif (diff==2):
        eps = 0.5
    elif (diff==3):
        eps = 0.3
    else:
        eps=0.05

    testWorld = World(userBoard)
    testAgent = Agent(0.9, eps, testWorld)
    for i in range(100):
        result = testAgent.Qlearning()

    return(testWorld.shotsTaken)
