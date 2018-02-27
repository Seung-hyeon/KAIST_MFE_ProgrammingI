def dealer_strategy(state):
    
    if sum_max(state['dealer']) < 17:
        return "H"
    else:
        return "S"

def init(n=1):
    
    return (['A', 'J', 'Q', 'K', 2,3,4,5,6,7,8,9,10])*4*n

def sum_min(cards):
    
    cards_val = [1 if c == 'A' else c for c in cards]
    cards_val = [c if isinstance(c, int) else 10 for c in cards_val]
    sum_cards = sum(cards_val)
    
    return sum_cards

def sum_max(cards):
    
    multiple_aces = False
    cards_val = []
    for c in cards:
        if c == 'A' and not multiple_aces:
            cards_val.append(11)
            multiple_aces = True
        else:
            cards_val.append(c)
    cards_val = [c if isinstance(c, int) else 10 for c in cards_val]
    sum_cards = sum(cards_val)
    
    return sum_cards

def get_press():
    
    while True:
        press = input("\n press 'H'(Hit), or 'S'(Stand, Stop) : ").upper()
        if press in ['H', 'S']:
            return press
        
def show(state, reveal=False):
    
    if not reveal: 
        print("   Dealer : " + str(state['dealer']))
    else:
        if sum_min(state['dealer']) != sum_max(state['dealer']):
            print("   Dealer : " + str(state['dealer']) +\
                  ' sum= ' + str(sum_min(state['dealer'])) +\
                  ' or ' +  str(sum_max(state['dealer'])))
        else:
            print("   Dealer : " + str(state['dealer']) +\
                  ' sum= ' + str(sum_min(state['dealer'])))
    if sum_min(state['player']) != sum_max(state['player']):
        print("   You    : " + str(state['player']) +\
              ' sum= ' + str(sum_min(state['player'])) +\
              ' or ' +  str(sum_max(state['player'])))
    else:
        print("   You    : " + str(state['player']) +\
              ' sum= ' + str(sum_min(state['player'])))
    return True

def get_score(state):

    if sum_max(state['dealer']) < 22:
        dealer_sum = sum_max(state['dealer'])
    elif sum_min(state['dealer']) < 22:
        dealer_sum = sum_min(state['dealer'])
    else:
        dealer_sum = 0
    if sum_max(state['player']) < 22:
        player_sum = sum_max(state['player'])
    elif sum_min(state['player']) < 22:
        player_sum = sum_min(state['player'])
    else:
        player_sum = 0
    return dealer_sum, player_sum

from random import shuffle

def play(player_strategy=None, dealer_strategy=dealer_strategy):

    deck = init()
    shuffle(deck)
    state = {'dealer':[], 'player':[]}
    state['dealer'].append(deck.pop())
    state['player'].append(deck.pop())
    
    if player_strategy is None: 
        print("\n-------------------------------------")
        print("|          Black Jack Game          |")
        print("-------------------------------------\n")
        press = 'H'
        print("\t----- YOUR TURN -----\n")
        while press == 'H':
            state['player'].append(deck.pop())
            show(state)
            if sum_min(state['player']) > 21:
                print("\n\t===== BUST ! YOU LOSE !! =====")
                return -1
            press = get_press()
        print("\n\t----- DEALER's TURN -----\n")
        press = press = dealer_strategy(state)
        while press == 'H':
            state['dealer'].append(deck.pop())
            press = dealer_strategy(state)
        show(state, True)
        
        dealer_sum, player_sum = get_score(state)

        if dealer_sum < player_sum:
            print("\n\t===== YOU WIN !! =====")
            return 1
        elif dealer_sum == player_sum:
            print("\n\t=====  TIED !!  =====")
            return 0
        else:
            print("\n\t===== YOU LOSE !! =====")
            return -1
    else:
        press = 'H'
        while press == 'H':
            state['player'].append(deck.pop())
            if sum_min(state['player']) > 21:
                return -1
            press = player_strategy(state)
        press = press = dealer_strategy(state)
        while press == 'H':
            state['dealer'].append(deck.pop())
            press = dealer_strategy(state)
        dealer_sum, player_sum = get_score(state)
        if dealer_sum < player_sum: return 1
        if dealer_sum == player_sum: return 0
        return -1

def win_rate(strategy, n=1000):
    win_count = 0
    for _ in range(n):
        if play(strategy) == 1:
            win_count += 1
    return win_count/n

if __name__ == '__main__':
	play()