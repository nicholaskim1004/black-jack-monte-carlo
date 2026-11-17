import random 
import pandas as pd
import numpy as np

from itertools import combinations

deck_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
deck_ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

pt_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,'J': 10, 'Q': 10, 'K': 10, 'A': [1, 11]}

deck = [[suit, rank] for suit in deck_suits for rank in deck_ranks]

all_pairs = list(combinations(deck, 2))

STOP_THRESHOLDS = [12, 13, 14, 15, 16, 17]

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


def card_val(card):
    return 11 if card[1] == 'A' else pt_values[card[1]]

#randomly draws two cards that add up to some value (the total value of your hand)
def draw_hand(value, hard_total=True):
    # hard: no ace in hand; soft: contains an ace
    choices = [list(p) for p in all_pairs
               if calculate_pt(list(p)) == value
               and any(r == 'A' for _, r in p) == (not hard_total)]
    return random.choice(choices)
        
#realized the logic for delear is easier
def draw_dealer(deck, up):
    up_val = 11 if up == 'A' else up
    rand_up = random.choice([c for c in deck if card_val(c) == up_val])
    hole = random.choice([c for c in deck if c != rand_up])
    return [rand_up, hole]

def compare_hands(you, dealer):
    if you > 21:
        return -1
    if dealer > 21 or you > dealer:
        return 1
    return 0 if you == dealer else -1

def play_dealer(dealer, deck):
    hand = list(dealer)
    
    #if hand value is < 17 then dealer forced to hit
    while calculate_pt(hand) < 17:
        hand.append(deck.pop())
    
    return calculate_pt(hand)

def simulate_deck(your_hand_value, dealer_up, hard_total=True, thresholds = STOP_THRESHOLDS):
    #return outcome under hit and stand under same situation
    
    your_hand = draw_hand(your_hand_value)

    dealer_hand = draw_dealer(make_deck(your_hand), dealer_up)    
    fil_deck = make_deck(your_hand, dealer_hand)
    random.shuffle(fil_deck)

    your_val = calculate_pt(your_hand, hard_total)
    dealer_val = calculate_pt(dealer_hand, hard_total)

    # blackjack check
    if your_val == 21 and dealer_val == 21:
        return 0, [0]*len(thresholds)
    if your_val == 21:
        return 1, [1]*len(thresholds)
    if dealer_val == 21:
        return -1, [-1]*len(thresholds)

    stand_outcome = compare_hands(your_val, play_dealer(dealer_hand, fil_deck.copy()))

    hit_outcomes = []
    for T in thresholds:
        deck_copy = fil_deck.copy()
        hand = your_hand + [deck_copy.pop()]          # first hit is forced
        while calculate_pt(hand) < T:                 # stopping condition
            hand.append(deck_copy.pop())
        val = calculate_pt(hand)
        if val > 21:
            hit_outcomes.append(-1)
        else:
            hit_outcomes.append(compare_hands(val, play_dealer(dealer_hand, deck_copy)))

    return stand_outcome, hit_outcomes


def monte_carlo(num_sims, your_hand_value, dealer_up, hard_total = True, thresholds = STOP_THRESHOLDS):

    results = [simulate_deck(your_hand_value, dealer_up, thresholds) for _ in range(num_sims)]
    stands = np.array([r[0] for r in results])
    hits = np.array([r[1] for r in results])          # shape (num_sims, len(thresholds))

    hit_evs = hits.mean(axis=0)
    best_i = int(np.argmax(hit_evs))                  # data picks the stopping rule
    best_hits = hits[:, best_i]

    diff = best_hits - stands
    diff_mean = diff.mean()
    diff_se = diff.std(ddof=1) / np.sqrt(num_sims)

    row = {
        'hand_value': your_hand_value,
        'dealer_show_value': dealer_up,
        'stand_ev': stands.mean(),
        'best_hit_ev': hit_evs[best_i],
        'best_stop_T': thresholds[best_i],
        'hit_minus_stand': diff_mean,
        'diff_se': diff_se,
        'best_action': 'hit' if hit_evs[best_i] > stands.mean() else 'stand',
        'significant': np.abs(diff_mean) > 2 * diff_se,
        'stand_win': (stands == 1).mean(), 'stand_tie': (stands == 0).mean(), 'stand_loss': (stands == -1).mean(),
        'hit_win': (best_hits == 1).mean(), 'hit_tie': (best_hits == 0).mean(), 'hit_loss': (best_hits == -1).mean(),
    }
    for T, ev in zip(thresholds, hit_evs):
        row[f'hit_T{T}_ev'] = ev
    return row

starting_hand_values = [4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]   
dealer_up_card = [2,3,4,5,6,7,8,9,10,'A']

#loop to go through every starting hand value and dealer up card and storing the exp value

rows = []

for start in starting_hand_values:
    for up in dealer_up_card:
    
        print('starting monte carlo for following hands')
        print(f'your hand value: {start}  delear up: {up}')
        
        sim = monte_carlo(10000, start, up)
        
        if sim['best_hit_ev']>sim['stand_ev']:
            print('winning strat hit')
        else:
            print('winning strate stand')
            
        print('storing result')
        rows.append(sim)

outcome_df = pd.DataFrame(rows)
outcome_df.to_csv('/Users/nicholaskim/Documents/Repositories/black jack monte carlo/result_hardtotals.csv', index=False)
