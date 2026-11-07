import random 
import pandas as pd

deck_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

pt_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,'J': 10, 'Q': 10, 'K': 10, 'A': [1, 11]}

deck = [[suit, rank] for suit in deck_suits for rank in deck_ranks]

def calculate_pt(hand, hard_total=True):
    
    if hard_total:
        pt = sum(1 if rank == 'A' else pt_values[rank] for _, rank in hand)
        has_ace = any(rank == 'A' for _, rank in hand)
        if has_ace and pt + 10 <= 21:   # promote one ace to 11 if it doesn't bust
            pt += 10
    else:
        pt = sum(1 if rank == 'A' else pt_values[rank] for _, rank in hand)
    return pt

def make_deck(*hands):
    used = [card for hand in hands for card in hand]
    return [card for card in deck if card not in used]

def draw_hand(deck, value):
    
    return 

def simulate_deck(your_hand, dealer_hand, choice='hit', hard_total=True):
    # work on copies so the caller's hands are never modified
    your_hand = your_hand.copy()
    dealer_hand = dealer_hand.copy()

    fil_deck = make_deck(your_hand, dealer_hand)
    random.shuffle(fil_deck)

    your_val = calculate_pt(your_hand, hard_total)
    dealer_val = calculate_pt(dealer_hand, hard_total)

    # blackjack check
    if your_val == 21 and dealer_val == 21:
        return 0
    if your_val == 21:
        return 1
    if dealer_val == 21:
        return -1

    if choice == 'hit':
        your_hand.append(fil_deck.pop())
        your_val = calculate_pt(your_hand)
        if your_val > 21:
            return -1

    # dealer draws until 17+
    while calculate_pt(dealer_hand) < 17:
        dealer_hand.append(fil_deck.pop())
    dealer_val = calculate_pt(dealer_hand)

    if dealer_val > 21 or your_val > dealer_val:
        return 1
    elif your_val == dealer_val:
        return 0
    else:
        return -1

def monte_carlo(num_sims, your_hand, dealer_hand, hard_total = True):
    results = {}
    for choice in ['hit', 'stand']:
        total = sum(simulate_deck(your_hand, dealer_hand, choice, hard_total) for _ in range(num_sims))
        results[choice] = total / num_sims

    return {
        'hand_value': calculate_pt(your_hand),
        'dealer_show_value': calculate_pt([dealer_hand[0]]),
        'hit_ev': results['hit'],
        'stand_ev': results['stand'],
    }
    
starting_hand_values = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]   
dealer_up_card = [2,3,4,5,6,7,8,9,10,'A']

#loop to go through every starting hand value and dealer up card and storing the exp value

outcome_df = pd.DataFrame(columns = ['hand_value', 'dealer_show_value', 'hit_ev', 'stand_ev'])

'''
for start in starting_hand_values:
    for up in dealer_up_card:
        your_hand = 1
        dealer_hand = 4
        
        outcome_df = pd.concat(monte_carlo(1000000, your_hand, dealer_hand))
'''
temp = deck.copy()

#way to pull a card based on inputted value of hand
target = 2

print(['A' if card[1] == 'A' else pt_values[card[1]] for card in deck ])

'''
for card in deck:
    suit, value = card
    
    value_int = pt_values[value]

    if value_int == target:
        print(card)
    elif value > 10:
        other_value = target - value_int
        if other_value == 1:
            print()
'''