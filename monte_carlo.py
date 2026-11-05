import random 

deck_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

pt_values = {'2': 2, 
             '3': 3, 
             '4': 4, 
             '5': 5, 
             '6': 6, 
             '7': 7, 
             '8': 8, 
             '9': 9, 
             '10': 10,
             'J': 10, 
             'Q': 10, 
             'K': 10, 
             'A': [1, 11]}

options = ['hit', 'stand', 'split', 'double', 'surrender']

deck = [[suit, rank] for suit in deck_suits for rank in deck_ranks]


#how each round works:
#draw 2 cards, dealer draws 2 cards (only know what 1st card is)
#decide between the options in the list
#calculate to see if the total points equals 21 or if you bust
#if hit -> draw a new card and recalc.-> dealer flips card -> if total > 17 stand -> if < 16 hits-> compares points  
#if stand -> delear flips card -> if total > 17 stands -> if < 16 stands -> compare points
#if surrender -> you lose/give up on hand
#if split -> play one hand 1st -> same decision tree as b/f -> after 1st hand finishes move to the 2nd hand 

#points calc
#only wrinkle is if Ace
#lets store both hands/how it plays out if you choose 1 or 11

#look into if I can use a tree/backtracking for this

def calculate_pt(hand):
    pt = 0
    for card in hand:
        pt += pt_values[card[1]]

    return pt

def make_deck(your_hand, dealer_hand):
    temp_deck = deck 
    
    for i in range(len(your_hand)):
        #since your and dealer will start with 2 cards each
        temp_deck.remove(your_hand[i])
        temp_deck.remove(dealer_hand[i])
    
    return temp_deck

def simulate_deck(your_hand, dealer_hand):

    fil_deck = make_deck(your_hand, dealer_hand)
    
    #check for blackjack
    your_hand_value = 0
    dealer_hand_value = 0
    
    for i in range(len(your_hand_value)):
        if your_hand[i][1] == 'A':
            pt_values
    
    #shuffle deck 
    random.shuffle(fil_deck)
    
    new_card = random.choice(fil_deck)
    dealer_new_card = random.choice(fil_deck)
    
    #remove those card from deck
    fil_deck.remove(new_card)
    fil_deck.remove(dealer_new_card)
    
    if dealer_hand_value <= 16:
        
        
        #dealer has to hit 
        dealer_new_card = random.choice(fil_deck)
        fil_deck.remove(dealer_new_card)
    else:
        if dealer_hand_value == 21:
            return 0
        elif dealer_hand_value > 21:
            return 1
        else:
            if dealer_hand_value < your_hand_value:
                return 1
            else:
                return 0
            
    
    return your_hand_value, dealer_hand_value

#run a monte carlo on each type of hand you could have


def monte_carlo(num_sims, your_hand, dealer_hand):
    wins = 0 
    
    for _ in range(num_sims):
        wins += simulate_deck(your_hand, dealer_hand)
    
    return wins / num_sims


#print(simulate_deck(['Spades','5'],['Diamonds','Q']))

