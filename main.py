'''
    CISC 453 - Assignment 4

    Reinforcement Learning AI-GUI
'''

from tkinter import *
import board as brd
import copy
import genAttacks as agentAttack
import time
import os
import sys

root = Tk()
root.geometry("560x800")
root.minsize(560,800)
root.maxsize(560,800)
C = Canvas(root, bg= 'blue', height=800, width=560)
bgImg = PhotoImage(master = C, file='battleshipBG.png')
bgLabel = Label(root, image=bgImg)
bgLabel.place(x=0, y=0, relwidth=1, relheight=1)

#Attacking placement--------------------------------------------------------

def easyClick(event):
    easyButton.configure(bg="#bababa")
    medButton.configure(bg="white")
    hardButton.configure(bg="white")
    vhardButton.configure(bg="white")
    aLabel.diff=1
                        
def medClick(event):
    easyButton.configure(bg="white")
    medButton.configure(bg="#bababa")
    hardButton.configure(bg="white")
    vhardButton.configure(bg="white")
    aLabel.diff=2    
                 
def hardClick(event):
    easyButton.configure(bg="white")
    medButton.configure(bg="white")
    hardButton.configure(bg="#bababa")
    vhardButton.configure(bg="white")
    aLabel.diff=3
    
def vhardClick(event):
    easyButton.configure(bg="white")
    medButton.configure(bg="white")
    hardButton.configure(bg="white")
    vhardButton.configure(bg="#bababa")
    aLabel.diff=4
    

def getShipsLeft(x, y):
    #mark ship index as hit if hit
    shipCnt = 0
    for ship in aLabel.botShips:
        indCnt = 0
        for ind in ship:
            if ind == (x, y):
                aLabel.botShips[shipCnt][indCnt] = 'hit'
            indCnt += 1
        shipCnt += 1
    
    #calc number of ships left
    carriers = 0
    destroyers = 0
    battleships = 0
    cruisers = 0
    for i in aLabel.botShips:
        if len(i) == 5:
            dead = True
            for coord in i:
                if coord != 'hit':
                    dead = False
            if dead != True:
                carriers += 1
        elif len(i) == 4:
            dead = True
            for coord in i:
                if coord != 'hit':
                    dead = False
            if dead != True:
                battleships += 1
        elif len(i) == 3:
            dead = True
            for coord in i:
                if coord != 'hit':
                    dead = False
            if dead != True:
                cruisers += 1
        elif len(i) == 2:
            dead = True
            for coord in i:
                if coord != 'hit':
                    dead = False
            if dead != True:
                destroyers += 1
        eCarrierNum.configure(text = carriers)
        eBattleshipNum.configure(text = battleships)
        eCruiserNum.configure(text = cruisers)
        eDestroyerNum.configure(text = destroyers)
        
        
        
    

#Event Handler for clicking on an attacking cell
def onAClick(event):
    if (aLabel.done!=True):
        if(aLabel.gameDone != True):
            if(subBut.complete==True):
                #take shot
                
                aLabel.start=True
                for y in range(0,8):
                    for x in range (0,8):
                        if buttonsB[(x,y)] == event.widget:
                            xSpot=x
                            ySpot=y
    
                if (buttonsB[(xSpot,ySpot)].cget('text')!="X") or (buttonsB[(xSpot,ySpot)].cget('text')!=" "):
                    
                    buttonsB[(xSpot,ySpot)].shot=True
                    hit = False
                    for ship in agentSL:
                        for piece in ship:
                            if (xSpot,ySpot) == piece:
                                hit=True
                    if (hit==True):
                        buttonsB[(xSpot,ySpot)].configure(text="X")
                        aLabel.configure(text="HIT!")
                        aLabel.place(x=280,y=305)
                        buttonsB[(xSpot,ySpot)].configure(bg="red")
                        aLabel.Uhits+=1
                        if(aLabel.Uhits==30):
                            wOrL('w') #You Win
    
                    else:
                        buttonsB[(xSpot,ySpot)].configure(text=" ")
                        aLabel.configure(text="MISS")
                        aLabel.place(x=280,y=305)
                        buttonsB[(xSpot,ySpot)].configure(bg="cyan")
                        
                    agentAtt(aLabel.clickC)
    
                    aLabel.clickC +=1
                    
                #update number of enemy ship types left
                getShipsLeft(xSpot, ySpot)
        else:
            if (aLabel.done!=True):
                aLabel.configure(text="Submit your ship placements below first!")

#Event handler for Mouse hovering over attack cells
def onAClickE(event):
    if (aLabel.done!=True):
        if (event.widget.cget('bg')!="red")and(event.widget.cget('bg')!="cyan"):
            event.widget.configure(bg="#e0e0e0")

#Event handler for mouse leaving hover area of attack cells
def onAClickL(event):
    if (aLabel.done!=True):
        if (event.widget.cget('bg')!="red")and(event.widget.cget('bg')!="cyan"):
            event.widget.configure(bg="white")

#Defensive placement---------------------------------------------------------------------

def restart(event):
    python = sys.executable
    os.execl(python, python, * sys.argv)

def close(event):
    popup.destroy()
    root.destroy()

def popopWorL(msg):    
    global popup
    popup = Tk()
    popup.wm_title("!")
    popup.configure(width=200,height=70)
    label = Label(popup, text=msg)
    label.place(x=18,y=10)
    aLabel.done=True
    replayBut = Button(popup, width=10,height=1, text="Replay")
    replayBut.place(x=15,y=37)
    replayBut.bind("<Button-1>",restart)
    closeBut = Button(popup, width=10,height=1, text="Exit")
    closeBut.place(x=100,y=37)
    closeBut.bind("<Button-1>",close)
    popup.mainloop()
    
#Function to display if User won or Lost against the Agent
def wOrL(result):
    aLabel.gameDone = True
    if result == 'w':
        popopWorL("You WON! Thanks for playing!") 
    else:
        popopWorL("You LOST! Thanks for playing!")

#Function to place Agent's missiles
def agentAtt(i):

    aAtt=aLabel.aAttack[i]

    if buttonsD[(aAtt)].cget('text')=="X":
        buttonsD[(aAtt)].configure(bg="red")
        aLabel.Ahits+=1
        if (aLabel.Ahits==30):
            wOrL('l')
    else:
        buttonsD[(aAtt)].configure(bg="cyan")

#Destroyer is going to be placed
def desClick(event):
    destroyerButton.configure(bg="#bababa")
    cruiserButton.configure(bg="white")
    battleButton.configure(bg="white")
    carrierButton.configure(bg="white")

    destroyerButton.value=True
    cruiserButton.value=False
    battleButton.value=False
    carrierButton.value=False

#Cruiser is going to be Placed
def cruClick(event):
    destroyerButton.configure(bg="white")
    cruiserButton.configure(bg="#bababa")
    battleButton.configure(bg="white")
    carrierButton.configure(bg="white")
    destroyerButton.value=False
    cruiserButton.value=True
    battleButton.value=False
    carrierButton.value=False

#BattleShip is going to be placed
def batClick(event):
    destroyerButton.configure(bg="white")
    cruiserButton.configure(bg="white")
    battleButton.configure(bg="#bababa")
    carrierButton.configure(bg="white")
    destroyerButton.value=False
    cruiserButton.value=False
    battleButton.value=True
    carrierButton.value=False

#Carrier is going to be placed
def carClick(event):
    destroyerButton.configure(bg="white")
    cruiserButton.configure(bg="white")
    battleButton.configure(bg="white")
    carrierButton.configure(bg="#bababa")
    destroyerButton.value=False
    cruiserButton.value=False
    battleButton.value=False
    carrierButton.value=True

#Function to change rotation of ship placement
def rotate(event):
    if event.widget.cget('text') ==u"\u2192":
        rotationButton.value = 's'
        event.widget.configure(text=u"\u2193")
    else:
        rotationButton.value = 'e'
        event.widget.configure(text=u"\u2192")

#When the user submits their ship placement
def subOnClick(event):
    if (aLabel.done!=True):
        if (desCount.cget('text')==0 and cruCount.cget('text')==0 and batCount.cget('text')==0 and carCount.cget('text')==0 and aLabel.start==False):
            aLabel.aAttack = agentAttack.mainAttack(defArray.value, aLabel.diff)
            event.widget.complete=True
            aLabel.configure(text="Time to attack! Choose a cell above to place a missile on that cell")
            aLabel.place(x=120,y=305)
        else:
            err.place(x=220,y=420)
            err.configure(text="Not all ships are placed")

#Event on leaving submit button w mouse
def subOnL(event):
    if (aLabel.done!=True):
        err.place(x=230,y=420)
        err.configure(text="")

#Function to clear board and default the values
def clearBoard(event):
    if (aLabel.done!=True):
        if (subBut.complete!=True):
            for y in range(0,8):
                for x in range(0,8):
                    buttonsD[(x,y)].configure(text="")
                    buttonsD[(x,y)].value = True
                    buttonsD[(x,y)].set = False
            desCount.configure(text=4)
            cruCount.configure(text=3)
            batCount.configure(text=2)
            carCount.configure(text=1)

#Function for placing the ships
shipsPlaced=[]
def onDClick(event):
    if (aLabel.done!=True):
        
        if(aLabel.diff != 0):
            for y in range(0,8):
                for x in range (0,8):
                    if buttonsD[(x,y)] == event.widget:
                        xSpot=x
                        ySpot=y
            if(buttonsD[(xSpot,ySpot)].value == True):
                if destroyerButton.value == True and desCount.cget('text')!=0 and buttonsD[(xSpot,ySpot)].set == False:
                    if rotationButton.value =='e':
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot+1,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot+1,ySpot)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot+1,ySpot)]
                        defArray.value.append(ship)
        
                        if (desCount.cget('text')==4):
                            desCount.configure(text=3)
                        elif (desCount.cget('text')==3):
                            desCount.configure(text=2)
                        elif (desCount.cget('text')==2):
                            desCount.configure(text=1)
                        elif (desCount.cget('text')==1):
                            desCount.configure(text=0)
        
                    else:
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot+1)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot,ySpot+1)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot,ySpot+1)]
                        defArray.value.append(ship)
        
                        if (desCount.cget('text')==4):
                            desCount.configure(text=3)
                        elif (desCount.cget('text')==3):
                            desCount.configure(text=2)
                        elif (desCount.cget('text')==2):
                            desCount.configure(text=1)
                        elif (desCount.cget('text')==1):
                            desCount.configure(text=0)
        
                elif cruiserButton.value == True and cruCount.cget('text')!=0 and buttonsD[(xSpot,ySpot)].set == False:
                    if rotationButton.value =='e' and err.cget('text')!="No intersecting ships!":
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot+1,ySpot)].configure(text="X")
                        buttonsD[(xSpot+2,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot+1,ySpot)].set= True
                        buttonsD[(xSpot+2,ySpot)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot+1,ySpot),(xSpot+2,ySpot)]
                        defArray.value.append(ship)
        
                        if (cruCount.cget('text')==3):
                            cruCount.configure(text=2)
                        elif (cruCount.cget('text')==2):
                            cruCount.configure(text=1)
                        elif (cruCount.cget('text')==1):
                            cruCount.configure(text=0)
                    elif rotationButton.value =='s' and err.cget('text')!="No intersecting ships!":
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot+1)].configure(text="X")
                        buttonsD[(xSpot,ySpot+2)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot,ySpot+1)].set= True
                        buttonsD[(xSpot,ySpot+2)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot,ySpot+1),(xSpot,ySpot+2)]
                        defArray.value.append(ship)
        
                        if (cruCount.cget('text')==3):
                            cruCount.configure(text=2)
                        elif (cruCount.cget('text')==2):
                            cruCount.configure(text=1)
                        elif (cruCount.cget('text')==1):
                            cruCount.configure(text=0)
                elif battleButton.value == True and batCount.cget('text')!=0 and buttonsD[(xSpot,ySpot)].set == False:
                    if rotationButton.value =='e' and err.cget('text')!="No intersecting ships!":
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot+1,ySpot)].configure(text="X")
                        buttonsD[(xSpot+2,ySpot)].configure(text="X")
                        buttonsD[(xSpot+3,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot+1,ySpot)].set= True
                        buttonsD[(xSpot+2,ySpot)].set= True
                        buttonsD[(xSpot+3,ySpot)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot+1,ySpot),(xSpot+2,ySpot),(xSpot+3,ySpot)]
                        defArray.value.append(ship)
        
        
                        if (batCount.cget('text')==2):
                            batCount.configure(text=1)
                        elif (batCount.cget('text')==1):
                            batCount.configure(text=0)
                    elif rotationButton.value =='s' and err.cget('text')!="No intersecting ships!":
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot+1)].configure(text="X")
                        buttonsD[(xSpot,ySpot+2)].configure(text="X")
                        buttonsD[(xSpot,ySpot+3)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot,ySpot+1)].set= True
                        buttonsD[(xSpot,ySpot+2)].set= True
                        buttonsD[(xSpot,ySpot+3)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot,ySpot+1),(xSpot,ySpot+2),(xSpot,ySpot+3)]
                        defArray.value.append(ship)
        
                        if (batCount.cget('text')==2):
                            batCount.configure(text=1)
                        elif (batCount.cget('text')==1):
                            batCount.configure(text=0)
        
                elif carrierButton.value == True and carCount.cget('text')!=0 and buttonsD[(xSpot,ySpot)].set == False:
                    if rotationButton.value =='e' and err.cget('text')!="No intersecting ships!":
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot+1,ySpot)].configure(text="X")
                        buttonsD[(xSpot+2,ySpot)].configure(text="X")
                        buttonsD[(xSpot+3,ySpot)].configure(text="X")
                        buttonsD[(xSpot+4,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot+1,ySpot)].set= True
                        buttonsD[(xSpot+2,ySpot)].set= True
                        buttonsD[(xSpot+3,ySpot)].set= True
                        buttonsD[(xSpot+4,ySpot)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot+1,ySpot),(xSpot+2,ySpot),(xSpot+3,ySpot),(xSpot+4,ySpot)]
                        defArray.value.append(ship)
        
                        if (carCount.cget('text')==1):
                            carCount.configure(text=0)
                    if rotationButton.value =='s' and err.cget('text')!="No intersecting ships!":
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot+1)].configure(text="X")
                        buttonsD[(xSpot,ySpot+2)].configure(text="X")
                        buttonsD[(xSpot,ySpot+3)].configure(text="X")
                        buttonsD[(xSpot,ySpot+4)].configure(text="X")
                        buttonsD[(xSpot,ySpot)].set= True
                        buttonsD[(xSpot,ySpot+1)].set= True
                        buttonsD[(xSpot,ySpot+2)].set= True
                        buttonsD[(xSpot,ySpot+3)].set= True
                        buttonsD[(xSpot,ySpot+4)].set= True
        
                        ship=[(xSpot,ySpot),(xSpot,ySpot+1),(xSpot,ySpot+2),(xSpot,ySpot+3),(xSpot,ySpot+4)]
                        defArray.value.append(ship)
        
                        if (carCount.cget('text')==1):
                            carCount.configure(text=0)
        else:
            err.configure(text="Enter a difficulty")
            err.place(x=245,y=420)

#Hovering over ship placement board
def onDClickE(event):
    
    if (aLabel.done!=True):
        if(subBut.complete != True):
            xSpot=0
            ySpot=0
            for y in range(0,8):
                for x in range (0,8):
                    if buttonsD[(x,y)] == event.widget:
                        xSpot=x
                        ySpot=y
    
            if (destroyerButton.value==True):
                if (rotationButton.value == 'e'):
                    if (xSpot == 7):
                        buttonsD[(xSpot,ySpot)].configure(bg="red")
                        buttonsD[(xSpot,ySpot)].value=False
                    else:
                        inv=False
                        for i in range (0,2):
                            if (buttonsD[(xSpot+i,ySpot)].cget('text')=="X"):
                                inv=True
    
                        if(inv!=True):
                            buttonsD[(xSpot,ySpot)].value=True
                        else:
                            buttonsD[(xSpot,ySpot)].value=False
                            err.configure(text="No intersecting ships!")
                            err.place(x=230,y=420)
    
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot+1,ySpot)].configure(text="X")
    
                else:
                    if (ySpot == 7):
                        buttonsD[(xSpot,ySpot)].configure(bg="red")
                        buttonsD[(xSpot,ySpot)].value=False
                    else:
                        inv=False
                        for i in range (0,2):
                            if (buttonsD[(xSpot,ySpot+i)].cget('text')=="X"):
                                inv=True
    
                        if(inv!=True):
                            buttonsD[(xSpot,ySpot)].value=True
                        else:
                            buttonsD[(xSpot,ySpot)].value=False
                            err.configure(text="No intersecting ships!")
    
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot+1)].configure(text="X")
    
            elif (cruiserButton.value==True):
                if (rotationButton.value == 'e'):
                    if (xSpot >= 6):
                        buttonsD[(xSpot,ySpot)].value=False
                        buttonsD[(xSpot,ySpot)].configure(bg="red")
                        if(xSpot < 7):
                            buttonsD[(xSpot+1,ySpot)].configure(bg="red")
                    else:
                        inv=False
                        for i in range (0,3):
                            if (buttonsD[(xSpot+i,ySpot)].cget('text')=="X"):
                                inv=True
    
                        if(inv!=True):
                            buttonsD[(xSpot,ySpot)].value=True
                        else:
                            buttonsD[(xSpot,ySpot)].value=False
                            err.configure(text="No intersecting ships!")
    
                        buttonsD[(xSpot,ySpot)].value=True
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot+1,ySpot)].configure(text="X")
                        buttonsD[(xSpot+2,ySpot)].configure(text="X")
    
                else:
                    if (ySpot >= 6):
                        buttonsD[(xSpot,ySpot)].value=False
                        buttonsD[(xSpot,ySpot)].configure(bg="red")
                        if(ySpot < 7):
                            buttonsD[(xSpot,ySpot+1)].configure(bg="red")
                    else:
                        inv=False
                        for i in range (0,3):
                            if (buttonsD[(xSpot,ySpot+i)].cget('text')=="X"):
                                inv=True
    
                        if(inv!=True):
                            buttonsD[(xSpot,ySpot)].value=True
                        else:
                            buttonsD[(xSpot,ySpot)].value=False
                            err.configure(text="No intersecting ships!")
    
                        buttonsD[(xSpot,ySpot)].value=True
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot+1)].configure(text="X")
                        buttonsD[(xSpot,ySpot+2)].configure(text="X")
    
            if (battleButton.value==True):
                if (rotationButton.value == 'e'):
                    if (xSpot >= 5):
                        buttonsD[(xSpot,ySpot)].value=False
                        buttonsD[(xSpot,ySpot)].configure(bg="red")
                        if(xSpot <7):
                            buttonsD[(xSpot+1,ySpot)].configure(bg="red")
                            if(xSpot < 6):
                                buttonsD[(xSpot+2,ySpot)].configure(bg="red")
                    else:
                        inv=False
                        for i in range (0,4):
                            if (buttonsD[(xSpot+i,ySpot)].cget('text')=="X"):
                                inv=True
    
                        if(inv!=True):
                            buttonsD[(xSpot,ySpot)].value=True
                        else:
                            buttonsD[(xSpot,ySpot)].value=False
                            err.configure(text="No intersecting ships!")
    
                        buttonsD[(xSpot,ySpot)].value=True
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot+1,ySpot)].configure(text="X")
                        buttonsD[(xSpot+2,ySpot)].configure(text="X")
                        buttonsD[(xSpot+3,ySpot)].configure(text="X")
    
                else:
                    if (ySpot >= 5):
                        buttonsD[(xSpot,ySpot)].value=False
                        buttonsD[(xSpot,ySpot)].configure(bg="red")
                        if(ySpot <7):
                            buttonsD[(xSpot,ySpot+1)].configure(bg="red")
                            if(ySpot<6):
                                buttonsD[(xSpot,ySpot+2)].configure(bg="red")
                    else:
                        inv=False
                        for i in range (0,4):
                            if (buttonsD[(xSpot,ySpot+i)].cget('text')=="X"):
                                inv=True
    
                        if(inv!=True):
                            buttonsD[(xSpot,ySpot)].value=True
                        else:
                            buttonsD[(xSpot,ySpot)].value=False
                            err.configure(text="No intersecting ships!")
    
                        buttonsD[(xSpot,ySpot)].value=True
                        buttonsD[(xSpot,ySpot)].configure(text="X")
                        buttonsD[(xSpot,ySpot+1)].configure(text="X")
                        buttonsD[(xSpot,ySpot+2)].configure(text="X")
                        buttonsD[(xSpot,ySpot+3)].configure(text="X")
    
            if (carrierButton.value==True):
                    if (rotationButton.value == 'e'):
                        if (xSpot >= 4):
                            buttonsD[(xSpot,ySpot)].value=False
                            buttonsD[(xSpot,ySpot)].configure(bg="red")
                            if(xSpot<7):
                                buttonsD[(xSpot+1,ySpot)].configure(bg="red")
                                if(xSpot<6):
                                    buttonsD[(xSpot+2,ySpot)].configure(bg="red")
                                    if(xSpot<5):
                                        buttonsD[(xSpot+3,ySpot)].configure(bg="red")
    
                        else:
                            inv=False
                            for i in range (0,5):
                                if (buttonsD[(xSpot+i,ySpot)].cget('text')=="X"):
                                    inv=True
    
                            if(inv!=True):
                                buttonsD[(xSpot,ySpot)].value=True
                            else:
                                buttonsD[(xSpot,ySpot)].value=False
                                err.configure(text="No intersecting ships!")
    
                            buttonsD[(xSpot,ySpot)].value=True
                            buttonsD[(xSpot,ySpot)].configure(text="X")
                            buttonsD[(xSpot+1,ySpot)].configure(text="X")
                            buttonsD[(xSpot+2,ySpot)].configure(text="X")
                            buttonsD[(xSpot+3,ySpot)].configure(text="X")
                            buttonsD[(xSpot+4,ySpot)].configure(text="X")
    
                    else:
                        if (ySpot >= 4):
                            buttonsD[(xSpot,ySpot)].value=False
                            buttonsD[(xSpot,ySpot)].configure(bg="red")
                            if(ySpot < 7):
                                buttonsD[(xSpot,ySpot+1)].configure(bg="red")
                                if(ySpot < 6):
                                    buttonsD[(xSpot,ySpot+2)].configure(bg="red")
                                    if(ySpot < 5):
                                        buttonsD[(xSpot,ySpot+3)].configure(bg="red")
                        else:
                            inv=False
                            for i in range (0,5):
                                if (buttonsD[(xSpot,ySpot+i)].cget('text')=="X"):
                                    inv=True
    
                            if(inv!=True):
                                buttonsD[(xSpot,ySpot)].value=True
                            else:
                                buttonsD[(xSpot,ySpot)].value=False
                                err.configure(text="No intersecting ships!")
    
                            buttonsD[(xSpot,ySpot)].value=True
                            buttonsD[(xSpot,ySpot)].configure(text="X")
                            buttonsD[(xSpot,ySpot+1)].configure(text="X")
                            buttonsD[(xSpot,ySpot+2)].configure(text="X")
                            buttonsD[(xSpot,ySpot+3)].configure(text="X")
                            buttonsD[(xSpot,ySpot+4)].configure(text="X")


#Mouse leaves a cell in the board ship placement grid
def onDClickL(event):
    if (aLabel.done!=True):
        if(subBut.complete != True):
            xSpot=0
            ySpot=0
            for y in range(0,8):
                for x in range (0,8):
                    if buttonsD[(x,y)] == event.widget:
                        xSpot=x
                        ySpot=y
    
            if (destroyerButton.value==True):
                if (rotationButton.value == 'e'):
                    if (xSpot == 7):
                        buttonsD[(xSpot,ySpot)].configure(bg="white")
                    else:
                        if (buttonsD[(xSpot,ySpot)].set != True):
                            buttonsD[(xSpot,ySpot)].configure(text="")
                        if (buttonsD[(xSpot+1,ySpot)].set != True):
                            buttonsD[(xSpot+1,ySpot)].configure(text="")
                        err.configure(text="")
    
    
                else:
                    if (ySpot == 7):
                        buttonsD[(xSpot,ySpot)].configure(bg="white")
                    else:
                        if (buttonsD[(xSpot,ySpot)].set != True):
                            buttonsD[(xSpot,ySpot)].configure(text="")
                        if (buttonsD[(xSpot,ySpot+1)].set != True):
                            buttonsD[(xSpot,ySpot+1)].configure(text="")
                        err.configure(text="")
    
            elif (cruiserButton.value==True):
                if (rotationButton.value == 'e'):
                    if (xSpot >= 6):
                        buttonsD[(xSpot,ySpot)].configure(bg="white")
                        if(xSpot < 7):
                            buttonsD[(xSpot+1,ySpot)].configure(bg="white")
                    else:
    
                        if (buttonsD[(xSpot,ySpot)].set != True):
                            buttonsD[(xSpot,ySpot)].configure(text="")
                        if (buttonsD[(xSpot+1,ySpot)].set != True):
                            buttonsD[(xSpot+1,ySpot)].configure(text="")
                        if (buttonsD[(xSpot+2,ySpot)].set != True):
                            buttonsD[(xSpot+2,ySpot)].configure(text="")
                        err.configure(text="")
    
                else:
                    if (ySpot >= 6):
                        buttonsD[(xSpot,ySpot)].configure(bg="white")
                        if(ySpot < 7):
                            buttonsD[(xSpot,ySpot+1)].configure(bg="white")
                    else:
                        if (buttonsD[(xSpot,ySpot)].set != True):
                            buttonsD[(xSpot,ySpot)].configure(text="")
                        if (buttonsD[(xSpot,ySpot+1)].set != True):
                            buttonsD[(xSpot,ySpot+1)].configure(text="")
                        if (buttonsD[(xSpot,ySpot+2)].set != True):
                            buttonsD[(xSpot,ySpot+2)].configure(text="")
                        err.configure(text="")
    
            if (battleButton.value==True):
                if (rotationButton.value == 'e'):
                    if (xSpot >= 5):
                        buttonsD[(xSpot,ySpot)].configure(bg="white")
                        if (xSpot < 7):
                            buttonsD[(xSpot+1,ySpot)].configure(bg="white")
                            if(xSpot < 6):
                                buttonsD[(xSpot+2,ySpot)].configure(bg="white")
                    else:
                        if (buttonsD[(xSpot,ySpot)].set != True):
                            buttonsD[(xSpot,ySpot)].configure(text="")
                        if (buttonsD[(xSpot+1,ySpot)].set != True):
                            buttonsD[(xSpot+1,ySpot)].configure(text="")
                        if (buttonsD[(xSpot+2,ySpot)].set != True):
                            buttonsD[(xSpot+2,ySpot)].configure(text="")
                        if (buttonsD[(xSpot+3,ySpot)].set != True):
                            buttonsD[(xSpot+3,ySpot)].configure(text="")
                        err.configure(text="")
    
                else:
                    if (ySpot >= 5):
                        buttonsD[(xSpot,ySpot)].configure(bg="white")
                        if(ySpot < 7):
                            buttonsD[(xSpot,ySpot+1)].configure(bg="white")
                            if(ySpot < 6):
                                buttonsD[(xSpot,ySpot+2)].configure(bg="white")
                    else:
                        if (buttonsD[(xSpot,ySpot)].set != True):
                            buttonsD[(xSpot,ySpot)].configure(text="")
                        if (buttonsD[(xSpot,ySpot+1)].set != True):
                            buttonsD[(xSpot,ySpot+1)].configure(text="")
                        if (buttonsD[(xSpot,ySpot+2)].set != True):
                            buttonsD[(xSpot,ySpot+2)].configure(text="")
                        if (buttonsD[(xSpot,ySpot+3)].set != True):
                            buttonsD[(xSpot,ySpot+3)].configure(text="")
                        err.configure(text="")
    
            if (carrierButton.value==True):
                    if (rotationButton.value == 'e'):
                        if (xSpot >= 4):
                            buttonsD[(xSpot,ySpot)].configure(bg="white")
                            if(xSpot < 7):
                                buttonsD[(xSpot+1,ySpot)].configure(bg="white")
                                if(xSpot<6):
                                    buttonsD[(xSpot+2,ySpot)].configure(bg="white")
                                    if(xSpot<5):
                                        buttonsD[(xSpot+3,ySpot)].configure(bg="white")
    
                        else:
                            
                            if (buttonsD[(xSpot,ySpot)].set != True):
                                buttonsD[(xSpot,ySpot)].configure(text="")
                            if (buttonsD[(xSpot+1,ySpot)].set != True):
                                buttonsD[(xSpot+1,ySpot)].configure(text="")
                            if (buttonsD[(xSpot+2,ySpot)].set != True):
                                buttonsD[(xSpot+2,ySpot)].configure(text="")
                            if (buttonsD[(xSpot+3,ySpot)].set != True):
                                buttonsD[(xSpot+3,ySpot)].configure(text="")
                            if (buttonsD[(xSpot+4,ySpot)].set != True):
                                buttonsD[(xSpot+4,ySpot)].configure(text="")
                            err.configure(text="")
    
                    else:
                        if (ySpot >= 4):
                            buttonsD[(xSpot,ySpot)].configure(bg="white")
                            if(ySpot < 7):
                                buttonsD[(xSpot,ySpot+1)].configure(bg="white")
                                if(ySpot<6):
                                    buttonsD[(xSpot,ySpot+2)].configure(bg="white")
                                    if(ySpot<5):
                                        buttonsD[(xSpot,ySpot+3)].configure(bg="white")
                        else:
                            if (buttonsD[(xSpot,ySpot)].set != True):
                                buttonsD[(xSpot,ySpot)].configure(text="")
                            if (buttonsD[(xSpot,ySpot+1)].set != True):
                                buttonsD[(xSpot,ySpot+1)].configure(text="")
                            if (buttonsD[(xSpot,ySpot+2)].set != True):
                                buttonsD[(xSpot,ySpot+2)].configure(text="")
                            if (buttonsD[(xSpot,ySpot+3)].set != True):
                                buttonsD[(xSpot,ySpot+3)].configure(text="")
                            if (buttonsD[(xSpot,ySpot+4)].set != True):
                                buttonsD[(xSpot,ySpot+4)].configure(text="")
                            err.configure(text="")



#Setting up Game Board---------------------------------------------------------------------------------
easyButton = Button(root, width=8,height=1, bg="white", activebackground='#bababa', text="Easy")
easyButton.place(x=470,y=500)
easyButton.bind("<Button-1>", easyClick)

medButton = Button(root, width=8,height=1, bg="white", activebackground='#bababa', text="Medium")
medButton.place(x=470,y=530)
medButton.bind("<Button-1>", medClick)

hardButton = Button(root, width=8,height=1, bg="white", activebackground='#bababa', text="Hard")
hardButton.place(x=470,y=560)
hardButton.bind("<Button-1>", hardClick)

vhardButton = Button(root, width=8,height=1, bg="white", activebackground='#bababa', text="Expert")
vhardButton.place(x=470,y=590)
vhardButton.bind("<Button-1>", vhardClick)




#attack buttons/cells
begX = 135
begY = 60
buttonsB = {}
for yI in range (0,8):
    for xI in range (0,8):
        coOrd = (xI,yI)
        buttonsB[coOrd] = Button(root, width=3,height=1, bg="white", activebackground='#750000', text="")
        buttonsB[coOrd].place(x=begX+xI*40, y=begY+yI*30)
        buttonsB[coOrd].value=True
        buttonsB[coOrd].set=False
        buttonsB[coOrd].shot=False
        buttonsB[coOrd].bind("<Button-1>", onAClick)
        buttonsB[coOrd].bind("<Enter>", onAClickE)
        buttonsB[coOrd].bind("<Leave>", onAClickL)

#user placement cells
begX2 = 135
begY2 = 450
buttonsD = {}
for yI in range (0,8):
    for xI in range (0,8):
        coOrd = (xI,yI)
        buttonsD[coOrd] = Button(root, width=3,height=1, bg="white", activebackground='#bababa', text="")
        buttonsD[coOrd].place(x=begX2+xI*40, y=begY2+yI*30)
        buttonsD[coOrd].value=True
        buttonsD[coOrd].set=False
        buttonsD[coOrd].bind("<Button-1>", onDClick)
        buttonsD[coOrd].bind("<Enter>", onDClickE)
        buttonsD[coOrd].bind("<Leave>", onDClickL)


#Button to change placement to a destroyer
destroyerButton = Button(root, width=8,height=1, bg="#bababa", activebackground='#bababa', text="Destroyer")
destroyerButton.place(x=40,y=470)
destroyerButton.bind("<Button-1>", desClick)
destroyerButton.value=True

#Button to change placement to a cruiser
cruiserButton = Button(root, width=8,height=1, bg="white", activebackground='#bababa', text="Cruiser")
cruiserButton.place(x=40,y=510)
cruiserButton.bind("<Button-1>", cruClick)
cruiserButton.value=False

#Button to change placement to a battleship
battleButton = Button(root, width=8,height=1, bg="white", activebackground='#bababa', text="Battle Ship")
battleButton.place(x=40,y=550)
battleButton.bind("<Button-1>", batClick)
battleButton.value=False

#Button to change placement to a carrier
carrierButton = Button(root, width=8,height=1, bg="white", activebackground='#bababa', text="Carrier")
carrierButton.place(x=40,y=590)
carrierButton.bind("<Button-1>", carClick)
carrierButton.value=False

#Button to change rotation of placement
rotationButton =  Button(root, width=4,height=1, bg="white", activebackground='#bababa', text=u"\u2192")
rotationButton.place(x=55, y = 630)
rotationButton.bind("<Button-1>", rotate)
rotationButton.value="e"

#Error label for placement
err = Label(root)
err.place(x=230,y=420)

#Counters for ships placed
desCount = Label(root, text=4)
desCount.place(x=110,y=472)

cruCount = Label(root, text=3)
cruCount.place(x=110,y=512)

batCount = Label(root, text=2)
batCount.place(x=110,y=552)

carCount = Label(root, text=1)
carCount.place(x=110,y=592)

#Button for submission
subBut = Button(root,width=19,height=2, bg="white",activebackground='#bababa', text="Submit Ship Placement")
subBut.place(x=200,y=700)
subBut.bind("<Button-1>", subOnClick)
subBut.bind("<Leave>", subOnL)
subBut.complete=False

#Arrary to keep track of user ships
defArray= Label(root)
defArray.value=[]

#button to clear the board
clearBut = Button(root,width=10,height=1, bg="white",activebackground='#bababa', text="Clear Board")
clearBut.place(x=235,y=750)
clearBut.bind("<Button-1>", clearBoard)

#label to display info
aLabel = Label(root)
aLabel.place(x=180,y=305)
aLabel.start=False
aLabel.Uhits=0
aLabel.Ahits=0
aLabel.gameDone=False
aLabel.gameResult=""
aLabel.clickC=0
aLabel.done=False
aLabel.diff=0


#labels for enemy ships
eHeader = Label(root)
eHeader.place(x=460,y=80)
eHeader.configure(text = 'Enemy Ships')

eCarriers = Label(root)
eCarriers.place(x=460,y=100)
eCarriers.configure(text = 'Carriers:')
eCarrierNum = Label(root)
eCarrierNum.place(x=510,y=100)
eCarrierNum.configure(text = 1)

eBattleships = Label(root)
eBattleships.place(x=460,y=120)
eBattleships.configure(text = 'Battleships:')
eBattleshipNum = Label(root)
eBattleshipNum.place(x=525,y=120)
eBattleshipNum.configure(text = 2)

eCruisers = Label(root)
eCruisers.place(x=460,y=140)
eCruisers.configure(text = 'Cruisers:')
eCruiserNum = Label(root)
eCruiserNum.place(x=510,y=140)
eCruiserNum.configure(text = 3)


eDestroyers = Label(root)
eDestroyers.place(x=460,y=160)
eDestroyers.configure(text = 'Destroyers:')
eDestroyerNum = Label(root)
eDestroyerNum.place(x=520,y=160)
eDestroyerNum.configure(text = 4)


#Agent's board
agentBoard = brd.Board()
agentSL = agentBoard.ships
aLabel.botShips = []
for ship in agentSL:
    aLabel.botShips.append(ship[:])


root.mainloop()
