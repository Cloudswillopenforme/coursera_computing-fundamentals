!#/usr/bin/python2
# implementation of card game - Memory

import simplegui
import random

memoryDeck = 0
exposedDeck = list()
state = 0
firstCardIndex = 0
secondCardIndex = 0
pointsCounter = 0

def new_game():
    global memoryDeck, exposedDeck, state, poinsCounter
    
    state = 0
    updateScore(0)
    
    memoryDeck = list()
    memoryDeck.extend(range(8))
    memoryDeck.extend(range(8))
    random.shuffle(memoryDeck)
    
    exposedDeck = [False] * len(memoryDeck)

# helpers
def checkForWinning():
    global memoryDeck, exposedDeck, firstCardIndex, secondCardIndex
    
    if memoryDeck[firstCardIndex] != memoryDeck[secondCardIndex]:
        exposedDeck[firstCardIndex], exposedDeck[secondCardIndex] = False, False
                
def updateScore(value):
    global pointsCounter
    
    if not value:
        pointsCounter = 0
    else:
        pointsCounter += 1
    label.set_text("Turns = " + str(pointsCounter))
     
# define event handlers
def mouseclick(pos):
    global memoryDeck, exposedDeck, state, firstCardIndex, secondCardIndex
    clickedCardIndex = pos[0] / 50
    
    if not exposedDeck[clickedCardIndex]:
        updateScore(1)
    # state handling
        if state == 0:
            state = 1
            exposedDeck[clickedCardIndex] = True
            firstCardIndex = clickedCardIndex
        elif state == 1:
            state = 2
            exposedDeck[clickedCardIndex] = True
            secondCardIndex = clickedCardIndex
            
        else:
            state = 1
            
            checkForWinning()
            
            exposedDeck[clickedCardIndex] = True
            firstCardIndex = clickedCardIndex
            
                           
def draw(canvas):
    global memoryDeck, exposedDeck
    x, y = 10, 75
    x_start, x_end = 0, 50
    
    for i in range(len(memoryDeck)):
        if exposedDeck[i] == True:
            canvas.draw_text(str(memoryDeck[i]), (x, y), 72, 'White')
        else:
            canvas.draw_polygon([[x_start, 0], [x_end, 0], [x_end, 100], [x_start, 100]], 6, 'White', 'Green')
        
        x +=50
        x_start += 50
        x_end += 50


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = " + str(pointsCounter))

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()