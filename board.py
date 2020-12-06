# -*- coding: utf-8 -*-
'''
playing space: 8x8
               64 states: 30 of which are 'hits'

10 ships: 4 two space 'destroyers'
          3 three space 'cruisers' 
          2 four space 'battleships'
          1 five space 'carrier'

Constraints: ships cannot be diagonal
            cannot overlap ships
            ships cannot go off board
'''
import numpy as np

'''
Class for battleship board construction
Creates board object which places ships randomly and stores the ship locations
'''
class Board:
    def __init__(self):
        self.board = self.buildBoard(8)
        self.ships = []
        self.fillBoard()
        
        
    '''
    @PARAM integer
    @PURPOSE create 2D array of size n
    @return 2D array
    '''
    def buildBoard(self, size):
        brd = []
        for row in range(size):
            cols = []
            for col in range(size):
                cols.append('_')
            brd.append(cols[:])
        return brd
    
    
    '''
    @PARAM None
    @PURPOSE place ships within the board
    @return None
    '''
    def fillBoard(self):
        #1 carrier
        location, direction = self.chooseLocation(5) #choose location and direction
        self.placeShip(location, direction, 5) #place ship into board
        
        #2 battleships
        for i in range(2): #for number of ships
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


    '''
    @PARAM random location in board, random direction, size of ship
    @PURPOSE iterate through ship size and place each ship on board state by state
    @return None
    '''
    def placeShip(self, loc, direction, size):
        ship = [] #list to save ship loactions
        for i in range(size):
            if direction == 'up':
                self.board[loc[0] + i][loc[1]] = 'X'
                ship.append((loc[0] + i, loc[1])) #add index to ship location
                
            elif direction == 'right':
                self.board[loc[0]][loc[1] + i] = 'X'
                ship.append((loc[0], loc[1] + i))
                
            elif direction == 'down':
                self.board[loc[0] - i][loc[1]] = 'X'
                ship.append((loc[0] - i, loc[1]))
                
            elif direction == 'left':
                self.board[loc[0]][loc[1] - i] = 'X'
                ship.append((loc[0], loc[1] - i))
        self.ships.append(ship) #add list of tuples (ship's postions) to ship list
        

    '''
    @PARAM integer (size of ship)
    @PURPOSE chooses a random location, if location is invalid program will
            keep choosing new locations till a valid one is found
    @return None
    '''
    def chooseLocation(self, size):
        loc = np.random.randint(8, size = 2) #choose 2 random integers
        possibleLoc, direction = self.validateLocation(size, loc) #check validity
        
        while possibleLoc != True: #while location is not valid
            #generate new random location, and test validity of it
            loc = np.random.randint(8, size = 2)
            possibleLoc, direction = self.validateLocation(size, loc)
            
        return loc, direction


    '''
    @PARAM integer (size of ship), array of 2 integers (starting location of ship placement)
    @PURPOSE create 2D array of size n
    @return boolean (if location is valid), string (direction chosen)
    '''
    def validateLocation(self, size, loc):
        possibleLocation = True
        direction = self.getDir() #choose random direction
        dirTried = []
        legalPlace = self.pathCheck(size, loc, direction) #check if possible to place
        
        while legalPlace != True: #not possible, try new direction
            if ('up' in dirTried) and ('down' in dirTried) and ('right' in dirTried) and ('down' in dirTried): #all directions tried, not possible
                possibleLocation = False #location not possible
                break
            dirTried.append(direction)
            newDir = self.getDir()
            while (newDir == direction):
                newDir = self.getDir()
            direction = newDir
            legalPlace = self.pathCheck(size, loc, direction)
        return possibleLocation, direction


    '''
    @PARAM None
    @PURPOSE choose random direction
    @return string containing direction
    '''
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
        
    
    '''
    @PARAM int (size of ship), array of ints (position chosen), string (direction chosen)
    @PURPOSE check to see if path is clear to place ship
    @return boolean (true if path clear, false if path blocked)
    '''
    def pathCheck(self, size, pos, direction):
        if direction == 'up':
            for ind in range(size):
                if ((pos[0] + ind) > 7) or (self.board[pos[0] + ind][pos[1]] != '_'): #if out of bounds, or state is occupied
                    return False #path blocked
                
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    