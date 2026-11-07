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

#stores for the starting hand, and delear show card what is 
outcome_mat = []

def calculate_pt(hand):
    pt = sum(1 if rank == 'A' else pt_values[rank] for _, rank in hand)
    has_ace = any(rank == 'A' for _, rank in hand)
    if has_ace and pt + 10 <= 21:   # promote one ace to 11 if it doesn't bust
        pt += 10
    return pt

def make_deck(*hands):
    used = [card for hand in hands for card in hand]
    return [card for card in deck if card not in used]

def draw_hand(deck):
    return [deck.pop(random.randrange(len(deck))) for _ in range(2)]

def simulate_deck(your_hand, dealer_hand, choice='hit'):
    # work on copies so the caller's hands are never modified
    your_hand = your_hand.copy()
    dealer_hand = dealer_hand.copy()

    fil_deck = make_deck(your_hand, dealer_hand)
    random.shuffle(fil_deck)

    your_val = calculate_pt(your_hand)
    dealer_val = calculate_pt(dealer_hand)

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

def monte_carlo(num_sims, your_hand, dealer_hand):
    results = {}
    for choice in ['hit', 'stand']:
        total = sum(simulate_deck(your_hand, dealer_hand, choice) for _ in range(num_sims))
        results[choice] = total / num_sims

    return {
        'hand_value': calculate_pt(your_hand),
        'dealer_show_value': calculate_pt([dealer_hand[0]]),
        'hit_ev': results['hit'],
        'stand_ev': results['stand'],
    }

temp = deck.copy()

your_hand = draw_hand(temp)
dealer_hand = draw_hand(temp)

print(monte_carlo(100000, your_hand, dealer_hand))

#print(calculate_pt([['Spades','A'],['Diamonds','Q']]))