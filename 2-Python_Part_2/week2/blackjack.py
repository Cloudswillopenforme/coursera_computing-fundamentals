!#/usr/bin/python2
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

player_hand = 0
dealer_hand = 0
deck = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand_cards = []

    def __str__(self):
        res = ""
        for i in range(len(self.hand_cards)):
            res += " " + str(self.hand_cards[i])
        return "Hand contains" + res

    def add_card(self, card):
        self.hand_cards.append(card)

    def get_value(self):
        hand_value = 0
        has_aces = False
        
        for card in self.hand_cards:
            rank = card.get_rank()
            hand_value += VALUES[rank]
            
            if rank == 'A':
                has_aces = True
            
        if has_aces and hand_value + 10 <= 21:
            hand_value += 10
                
        return hand_value
                
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                    card = Card(suit, rank)
                    self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        res = ""
        for i in range(len(self.deck)):
            res += " " + str(self.deck[i])
        return "Deck contains" + res


#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck
    
    # initialize game
    player_hand = Hand()
    dealer_hand = Hand()
    
    deck = Deck()
    
    deck.shuffle()
    
    # deal a card to a player and a dealer
    card1 = deck.deal_card()
    player_hand.add_card(card1)
    
    card2 = deck.deal_card()
    dealer_hand.add_card(card2)
    
    print "Player's hand: " + str(player_hand)
    print "Dealer's hand: " + str(dealer_hand)
    in_play = True

def hit():
    global player_hand, in_play, outcome, score

    if player_hand.get_value() <= 21:
        card = deck.deal_card()
        player_hand.add_card(card)
        
        if player_hand.get_value() > 21:
            outcome = "You have busted"
            in_play = False
        else: 
            print "Player's hand: " + str(player_hand.get_value())
    
    print outcome
    score = 0
       
def stand():
    global dealer_hand, in_play, outcome, score
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    while in_play and dealer_hand.get_value() < 17:
        dealer_hand.add_card()
        
    if dealer_hand.get_value() > 21:
        outcome = "Dealer has busted"
    elif dealer_hand.get_value() >= player_hand.get_value():
        outcome = "You have busted"
    else:
        outcome = "You won!"
            
    print outcome
    in_play = False
    score = 0

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()