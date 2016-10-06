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
        self.card_list = []

    def __str__(self):
        p = ''
        for i in self.card_list:
            p += (str(i.suit)+str(i.rank))
            p += ' '
        return 'Hand contains '+ p[0:-1]
            

    def add_card(self, card):
        return self.card_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        count = 0
        has_A = False
        for i in self.card_list:
            count += VALUES[i.get_rank()]
            if i.get_rank() == 'A':
                has_A = True
        if has_A:
            if count + 10 <= 21:
                count += 10
        return count
                
   
    def draw(self, canvas, pos):
        count = 0
        for i in self.card_list:
            i.draw(canvas, [pos[0]+count*72, pos[1]])
            count += 1
 
        
# define deck class 
class Deck:
    def __init__(self):
        p = []
        for i in SUITS:
            for j in RANKS:
                p.append(Card(i,j))
        self.card_set = p

    def shuffle(self):
        # shuffle the deck 
        return random.shuffle(self.card_set)

    def deal_card(self):
        return self.card_set.pop()
    
    def __str__(self):
        o = ''
        for i in self.card_set:
            o += str(i.suit) + str(i.rank)
            o += ' '
        return "Deck contains " + o[0:-1]




#define event handlers for buttons
def deal():
    global outcome, in_play, player_hand, dealer_hand, deck, score
    outcome = ''
    if in_play:
        score -= 1
        outcome = 'Player give up this turn, dealer win!'
    player_hand = Hand()
    dealer_hand = Hand()
    deck = Deck()
    deck.shuffle()
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    print "player's hand ", player_hand
    print "dealer's hand ", dealer_hand
    print dealer_hand.get_value(),player_hand.get_value()
    in_play = True

def hit():
    global player_hand, deck, score, in_play, outcome
    # if the hand is in play, hit the player
    if in_play:
        player_hand.add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            print "You have busted"
            outcome = 'Player busted! Dealer win!'
            score -= 1
            in_play = False
        print dealer_hand, player_hand
        
def stand():
    global player_hand, deck, score, in_play, dealer_hand, outcome
    if in_play:
        if player_hand.get_value() > 21:
            print "Friend, you have already busted, so do yourself some favor and save some energy, stop press the button!"
            in_play = False
        else:
            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal_card())
            if dealer_hand.get_value() > 21:
                score += 1
                outcome = "Dealer busted! Player win!"
                print dealer_hand, player_hand
                print dealer_hand.get_value(),player_hand.get_value()
            elif dealer_hand.get_value() < player_hand.get_value():
                score += 1
                outcome = "Player win!"
                print dealer_hand, player_hand
                print dealer_hand.get_value(),player_hand.get_value()
            elif dealer_hand.get_value() > player_hand.get_value():
                score -= 1
                outcome = "Dealer win!"
                print dealer_hand, player_hand
                print dealer_hand.get_value(),player_hand.get_value()
            elif dealer_hand.get_value() == player_hand.get_value():
                score -= 1
                outcome = "Dealer win ties!"
                print dealer_hand, player_hand
                print dealer_hand.get_value(),player_hand.get_value()
            in_play = False
            
                
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global player_hand, dealer_hand, outcome, in_play
    player_hand.draw(canvas, [50,400])
    canvas.draw_text(outcome, [50,325],30,"Yellow")
    canvas.draw_text("score = %d"%score, [240,560], 30, "Yellow")
    canvas.draw_text("Blackjack", [170,60],60, "Red")
    if in_play:
        dealer_hand.draw(canvas, [50,150])
        canvas.draw_polygon([[50, 150], [122, 150], [120, 246], [50, 246]], 4, 'Green', 'Green')
    else:
        dealer_hand.draw(canvas, [50,150])
        



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


# remember to review the gradic rubric
