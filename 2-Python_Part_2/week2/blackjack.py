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

in_play = False
player_output = ""
dealer_output = ""
score = 0

player_hand = 0
dealer_hand = 0
deck = []

SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


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
        for i in range(len(self.hand_cards)):
            self.hand_cards[i].draw(canvas, [pos[0] + 80 * i, pos[1]])
            
       
    def hide_first_card(self, canvas, pos):
        card_loc = (CARD_BACK_CENTER[0], 
                    CARD_BACK_CENTER[1])
        canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
        
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
    global player_output, dealer_output, in_play, player_hand, dealer_hand, deck, score
    
    # initialize game
    deck = Deck()
    
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    
    # deal 2 cards to a player and a dealer
    d_card1 = deck.deal_card()
    player_hand.add_card(d_card1)
    d_card2 = deck.deal_card()
    player_hand.add_card(d_card2)
    
    p_card1 = deck.deal_card()
    dealer_hand.add_card(p_card1)
    p_card2 = deck.deal_card()
    dealer_hand.add_card(p_card2)
    
    if in_play:
        score -= 1
        dealer_output = "You lose the round!"
    else:
        dealer_output = ""
        
    player_output = "Hit or stand?"    
    in_play = True
    
    print
    print "New game"
    print "Dealer score: "
    print "Player score: " + str(player_hand.get_value())

def hit():
    global player_hand, in_play, player_output, dealer_output, score, deck
    
    dealer_output = ""

    if in_play and player_hand.get_value() <= 21:
        
        card = deck.deal_card()
        player_hand.add_card(card)
        
        if player_hand.get_value() > 21:
            dealer_output = "You have busted and you lose!"
            player_output = "New deal?"
            
            score -= 1
            in_play = False
            
        print        
        print "Dealer score: " 
        print "Player score: " + str(player_hand.get_value())
       
def stand():
    global dealer_hand, in_play, player_output, dealer_output, score, deck
   
    if in_play:
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer_hand.get_value() < 17:
            card = deck.deal_card()
            dealer_hand.add_card(card)
        
        # check results
        if dealer_hand.get_value() > 21:
            dealer_output = "I have busted and you win!"
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            dealer_output = "You lose!"
            score -= 1
        else:
            dealer_output = "You win!"
            score += 1
            
        player_output = "New deal?"
        in_play = False
        
        print
        print "Dealer score: " + str(dealer_hand.get_value())
        print "Player score: " + str(player_hand.get_value())
          
def draw(canvas):
    global dealer_hand, player_hand, score, player_output, dealer_output, in_play
    canvas.draw_text("BLACKJACK", [150, 70], 42, "White", "monospace")
    canvas.draw_text("Score: " + str(score), [400, 140], 28, "White", "monospace")
    
    canvas.draw_text("Dealer:", [90, 200], 22, "White", "monospace")
    canvas.draw_text("Player:", [90, 400], 22, "White", "monospace")
    canvas.draw_text(str(dealer_output), [210, 200], 22, "White", "monospace")
    canvas.draw_text(str(player_output), [210, 400], 22, "White", "monospace")

    dealer_hand.draw(canvas, [120, 230])
    player_hand.draw(canvas, [120, 430])
    
    if in_play:
        dealer_hand.hide_first_card(canvas, [120, 230])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

deal()
frame.start()