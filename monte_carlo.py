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

deck = [[suit, rank] for suit in deck_suits for rank in deck_ranks]

def simulate_deck(your_hand, dealer_hand):
    return 


def monte_carlo(num_sims, your_hand, dealer_hand):
    wins = 0 
    
    for _ in range(num_sims):
        wins += simulate_deck(your_hand, dealer_hand)
    
    return wins / num_sims

print(deck)