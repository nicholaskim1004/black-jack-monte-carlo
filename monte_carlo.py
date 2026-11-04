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
    #remove your hand and dealers hand from deck
    temp_deck = deck 
    
    temp_deck.remove(your_hand)
    temp_deck.remove(dealer_hand)
    
    #shuffle deck 
    random.shuffle(temp_deck)
    
    new_card = random.choice(temp_deck)
    dealer_new_card = random.choice(temp_deck)
    
    #remove those card from deck
    temp_deck.remove(new_card)
    temp_deck.remove(dealer_new_card)
    
    your_hand_value = pt_values[your_hand[1]] + pt_values[new_card[1]]
    dealer_hand_value = pt_values[dealer_hand[1]] + pt_values[dealer_new_card[1]]
    
    return your_hand_value, dealer_hand_value


def monte_carlo(num_sims, your_hand, dealer_hand):
    wins = 0 
    
    for _ in range(num_sims):
        wins += simulate_deck(your_hand, dealer_hand)
    
    return wins / num_sims


print(simulate_deck(['Spades','5'],['Diamonds','Q']))

