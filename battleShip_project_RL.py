# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:17:43 2020

@authors: Jared Taylor, 20075820;
          Joe Momma, 42006969
"""

'''
playing space: 8x8
               64 states: 30 of which are 'hits'

10 ships: 4 two space 'destroyers'
          3 three space 'cruisers' 
          2 four space 'battleships'
          1 five space 'carrier'

Constraints: ships cannot be diagonal
'''
import numpy as np

class Board:
    def __init__(self):
        self.board = self.buildBoard(8)
        self.ships = []
        
    def buildBoard(self, size):
        brd = []
        for row in range(size):
            cols = []
            for col in range(size):
                cols.append('_')
            brd.append(cols[:])
        return brd
    
    def fillBoard(self):
        #1 carrier
        location, direction = self.chooseLocation(5)
        self.placeShip(location, direction, 5)
        
        #2 battleships
        for i in range(2):
            location, direction = self.chooseLocation(4)
            self.placeShip(location, direction, 4)
        
        #3 cruisers
        for i in range(3):
            location, direction = self.chooseLocation(3)
            self.placeShip(location, direction, 3)
            
        #4 destroyers
        for i in range(4):
            location, direction = self.chooseLocation(2)
            self.placeShip(location, direction, 2)

    def placeShip(self, loc, direction, size):
        ship = []
        for i in range(size):
            if direction == 'up':
                self.board[loc[0] + i][loc[1]] = 'X'
                ship.append((loc[0] + i, loc[1]))
            elif direction == 'right':
                self.board[loc[0]][loc[1] + i] = 'X'
                ship.append((loc[0], loc[1] + i))
            elif direction == 'down':
                self.board[loc[0] - i][loc[1]] = 'X'
                ship.append((loc[0] - i, loc[1]))
            elif direction == 'left':
                self.board[loc[0]][loc[1] - i] = 'X'
                ship.append((loc[0], loc[1] - i))
        self.ships.append(ship)
        

    def chooseLocation(self, size):
        loc = np.random.randint(8, size = 2)
        possibleLoc, direction = self.validateLocation(size, loc)
        while possibleLoc != True: #while loaction is not valid
            #generate new random location, and test validity of it
            loc = np.random.randint(8, size = 2)
            possibleLoc, direction = self.validateLocation(size, loc)
            
            
        
        return loc, direction

    def validateLocation(self, size, loc):
        possibleLocation = True
        direction = self.getDir()
        dirTried = []
        legalPlace = self.pathCheck(size, loc, direction) #check if possible to place
        while legalPlace != True: #not possible, try new direction
            if ('up' in dirTried) and ('down' in dirTried) and ('right' in dirTried) and ('down' in dirTried): #all directions tried, not possible
                possibleLocation = False
                break
            dirTried.append(direction)
            newDir = self.getDir()
            while (newDir == direction):
                newDir = self.getDir()
            direction = newDir
            legalPlace = self.pathCheck(size, loc, direction)
        return possibleLocation, direction

    def getDir(self):
        direction = np.random.randint(4)
        if direction == 0:
            return 'up'
        elif direction == 1:
            return 'right'
        elif direction == 2:
            return 'down'
        elif direction == 3:
            return 'left'
        
    def pathCheck(self, size, pos, direction):
        if direction == 'up':
            for ind in range(size):
                if ((pos[0] + ind) > 7) or (self.board[pos[0] + ind][pos[1]] != '_'):
                    return False
                
        elif direction == 'right':
            for ind in range(size):
                if ((pos[1] + ind) > 7) or (self.board[pos[0]][pos[1] + ind] != '_'):
                    return False
                
        elif direction == 'down':
            for ind in range(size):
                if ((pos[0] - ind) < 0) or (self.board[pos[0] - ind][pos[1]] != '_'):
                    return False
                
        elif direction == 'left':
            for ind in range(size):
                if ((pos[1] - ind) < 0) or (self.board[pos[0]][pos[1] - ind] != '_'):
                    return False
        
        #path is clear
        return True
'''
Cannot revisit a node
'''
class Agent:
    def __init__(self):
        self.Q = {}
        
    #when agent recieves +1 reward (aka a hit)
    def attackMode():
        None
        
    #when agent recieves reward of -1 (miss)
    def explore():
        None

def main():
    env = Board()
    agent = Agent()
    env.fillBoard()
    print(env.board)
    xCnt = 0
    rCnt = 0
    for row in env.board:
        iCnt = 0
        for ind in row:
            if env.board[rCnt][iCnt] == 'X':
                xCnt += 1
            iCnt += 1
        rCnt += 1
    print('# of ship states: ', xCnt) #count of hit spaces
    print('ship locations: ', env.ships)
    

if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    