# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 12:17:43 2020

@authors: Jared Taylor, 20075820;
          Joe Momma, 42006969
"""
class Board:
    def __init__(self):
        self.grid = []
        self.ships = []

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

if __name__ == '__main__':
    main()