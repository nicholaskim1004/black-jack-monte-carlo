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

def simulate_deck(your_hand, dealer_hand):
    #remove your hand and dealers hand from deck
    temp_deck = deck 
    
    for i in range(len(your_hand_value)):
        #since your and dealer will start with 2 cards each
        temp_deck.remove(your_hand[i])
        temp_deck.remove(dealer_hand[i])
    
    #check for blackjack
    your_hand_value = 0
    dealer_hand_value = 0
    
    for i in range(len(your_hand_value)):
        if your_hand[i][1] == 'A':
            pt_values
    
    #shuffle deck 
    random.shuffle(temp_deck)
    
    new_card = random.choice(temp_deck)
    dealer_new_card = random.choice(temp_deck)
    
    #remove those card from deck
    temp_deck.remove(new_card)
    temp_deck.remove(dealer_new_card)
    
    if dealer_hand_value <= 16:
        
        
        #dealer has to hit 
        dealer_new_card = random.choice(temp_deck)
        temp_deck.remove(dealer_new_card)
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


def monte_carlo(num_sims, your_hand, dealer_hand):
    wins = 0 
    
    for _ in range(num_sims):
        wins += simulate_deck(your_hand, dealer_hand)
    
    return wins / num_sims


#print(simulate_deck(['Spades','5'],['Diamonds','Q']))

