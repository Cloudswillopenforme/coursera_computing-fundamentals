!#/usr/bin/python2

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

# initialize global variables used in your code here
guess_number = 0
secret_number = 0
range_number = 100
attempt_number = 0

# helper function to start and restart the game
def new_game():
    global secret_number, range_number, attempt_number
    secret_number = random.randrange(0, range_number)
    attempt_number = calc_number_of_attempts()
    
    print
    print 'New game was started!'
    print 'Enter any number in the range [0, ' + str(range_number) + ') and press Enter'
    print 'You have ' + str(attempt_number) + ' attempts'
    
def calc_number_of_attempts():
    global range_number
    return int(math.ceil(math.log(range_number, 2)))

# define event handlers for control panel
def range100():
    global range_number
    range_number = 100
    new_game()
    

def range1000():     
    global range_number
    range_number = 1000
    new_game()
    
    
def input_guess(guess):
    global guess_number, attempt_number
    
    if (attempt_number != 0):
        # check for unempty input and convert
        if (guess):
            guess_number = int(guess)
        else:
            print 'Enter some valid number'
            return
        
        # print message
        print
        print 'Guess was ' + guess
        
        # main logic -- compare to secret_number
        if (guess_number > secret_number):
            print 'Lower!'
        elif (guess_number < secret_number):
            print 'Higher!'
        else:
            print 'Correct!'
            new_game()
            return
        
        # decrease number of attempts
        attempt_number -= 1
            
        # print attempts status message
        if (attempt_number != 0):
            print 'You have ' + str(attempt_number) + ' attempts left'
        else:
            print
            print 'You are out of attempts. Try again!'
            new_game()

    
# create frame
frame = simplegui.create_frame('Guess the number', 200, 200)

# register event handlers for control elements and start frame
frame.add_button('Range is [0, 100)', range100, 200)
frame.add_button('Range is [0, 1000)', range1000, 200)
frame.add_input('Enter a guess number:', input_guess, 200)


# call new_game 
new_game()

# start frame
frame.start()
