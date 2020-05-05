!#/usr/bin/python2
import random

# helper functions

def name_to_number(name):
    if name == 'rock':
        result = 0
    elif name == 'Spock':
        result = 1
    elif name == 'paper':
        result = 2
    elif name == 'lizard':
        result = 3
    elif name == 'scissors':
        result = 4
    else:
        print 'Incorrect value was given. Please, insert one of 5 options for this game!'
        return
    
    return result


def number_to_name(number):
    if number == 0:
        result = 'rock'
    elif number == 1:
        result = 'Spock'
    elif number == 2:
        result = 'paper'
    elif number == 3:
        result = 'lizard'
    elif number == 4:
        result = 'scissors'
    else:
        print 'Incorrect value was passed in the function. It is probably some programme mistake'
        return
    
    return result
    

def rpsls(player_choice): 
    
    # a blank line to separate consecutive games
    print ''
    
    print 'Player chooses ' + player_choice

    player_number = name_to_number(player_choice)

    comp_number = random.randrange(0, 5)    
    comp_choice = number_to_name(comp_number)
    
    print 'Computer chooses ' + comp_choice

    # difference of comp_number and player_number modulo five
    diff = (player_number - comp_number) % 5

    # use if/elif/else to determine winner, print winner message
    if (diff == 1) or (diff == 2):
        winner_message = 'Player wins!'
    elif diff == 0:
        winner_message = 'Player and computer tie!'
    else:
        winner_message = 'Computer wins!'
    
    print winner_message
    
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

