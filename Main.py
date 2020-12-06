# State space is the indexes (+1) of the ship locations list that are sunk
# The states are represented as tuples (e.x. the state (2,4) represents the state of the game where the 2nd and 4th ships are sunk)
# The initial state is no ships sunk, and that is represented as the tuple (0,)
# The action space is the set of possible shots the agent can take in each staticmethod
# Possible shots in a state are determined by subtracting the coordinates of the sunk ships from the list of all the coordinates on the board
# The actions that were already taken are also accounted for when choosing which action to take from a given state
# Adjusting the learning and exploring rate (exploring rate especially) can allow us to have different difficulties
# Right now, it prints the list of actions it would take each iteration to get to the goal state (all ships sunk)

import numpy as np
import random
import board as brd
from itertools import combinations
import time

class World:
    def __init__(self):
        self.board = brd.Board()
        self.gameHeight = 8
        self.gameWidth = 8        #[ [(1,2),(1,3),(1,4)], [(3,4),(3,3),(3,2)], [(5,5),(5,6),(5,7)] ]
        self.playerShipLocations = self.board.ships
        #self.playerShipLocations = [[(6, 0), (5, 0), (4, 0), (3, 0), (2, 0)], [(5, 3), (5, 4), (5, 5), (5, 6)], [(1, 7), (1, 6), (1, 5), (1, 4)], [(7, 5), (7, 6), (7, 7)], [(6, 3), (6, 2), (6, 1)], [(1, 1), (1, 2), (1, 3)], [(7, 3), (7, 2)], [(3, 6), (3, 5)], [(3, 2), (3, 1)], [(4, 5), (4, 4)]]
        self.shotsTaken = []
        self.possibleStates = self.getPossibleStates()
        self.startState = (0,)
        self.currentState = self.startState
        self.goalState = self.determineGoalState()

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

    def getPossibleActions(self):
        possibleActions = []

        for x in range(self.gameHeight):
            for y in range(self.gameWidth):
                #if [x,y] not in self.shotsTaken:
                possibleActions.append((x,y))

        return possibleActions # this is a list of all the coordinates on the grid

    def moveToNewState(self, action):
        self.shotsTaken.append(action) # register this actions as taken
        sunkNewShip = True # initalize
        reward = -1 # initalize and will be the reward if the shot is a miss
        newState = self.currentState # initalize

        # this function should check to see if a new ship was sunk and update the state accordingly

        for i in range(len(self.playerShipLocations)):
            if action in self.playerShipLocations[i]: # if we hit a ship
                reward = 0 # will be the reward if the shot is a hit
                for coordinate in self.playerShipLocations[i]: # check to see if we sunk that ship
                    if coordinate not in self.shotsTaken: # if we are still missing one, they still get the reward, but this does not register as a new ship being sunk, and so we do not move to the next state
                        sunkNewShip = False
                        break
                #newState = self.currentState + (i+1,) # NEED A NEW WAY TO MOVE TO THE NEXT STATE
                if sunkNewShip:
                    reward = 1 # will be the reward if the shot was a hit and a ship was sunk
                    if self.currentState == self.startState: # still need a better way to move to next state
                        newState = (i+1,)
                    else:
                        newState = self.currentState + (i+1,)
                        newState = tuple(sorted(newState))
                    break

        return newState, reward # return the new state (new state will be equal to old state if a new ship was not sunk) and the reward for entering that state


class Agent:
    def __init__(self, a, e, world: World):
        self.alpha = a # learning rate
        self.epsilon = e # the percent you want to explore
        self.world = world
        self.gamma = 0.9
        self.Q_values = self.createQTable()
        self.numOfSteps = 0

    def createQTable(self):
        QTable = {}
        for state in self.world.possibleStates:
            QTable[state] = {}
            for x in range(self.world.gameHeight):
                for y in range(self.world.gameWidth):
                    QTable[state][(x,y)] = 0

        return QTable # returns a dictionary where each key is another dictionary that holds the actions available in that state and the Q-values for each of those actions


    def getBestAction(self, state): # THIS IS CONSTANTLY CHOOSING THE SAME ACTION
        maxVal = np.NINF
        maxAction = None

        valuesForAllowedActions = []
        allowedActions = self.world.getPossibleActions()

        for action in self.world.shotsTaken:
            if action in allowedActions:
                allowedActions.remove(action)

        for action in allowedActions:
            valuesForAllowedActions.append(self.Q_values[state][action])

        for i in range(len(allowedActions)):
            if valuesForAllowedActions[i] > maxVal:
                maxVal = valuesForAllowedActions[i]
                bestAction = allowedActions[i]

        return bestAction # return the optimal action to take from this state

    def chooseAction(self, state):
        allowedActions = self.world.getPossibleActions()

        for action in self.world.shotsTaken:
            if action in allowedActions:
                allowedActions.remove(action)

        action = None # initializing the return

        randomNum = np.random.rand()

        # this is the epsilon-greedy policy:
        if(randomNum < self.epsilon):
            subOptimalActionChoiceIndex = random.randint(0, len(allowedActions) - 1)
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

def main():
    for x in range(1000):
        testWorld = World()
        testAgent = Agent(0.9, 0.01, testWorld)
        #for ship in testWorld.playerShipLocations:
        #    print(ship)
        #print(testWorld.playerShipLocations)
        for i in range(100):
            result = testAgent.Qlearning()
        print(testWorld.shotsTaken) # prints the actions taken in this iteration


if __name__ == '__main__':
    main()
