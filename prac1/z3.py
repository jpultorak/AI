# Rozwiązanie zadania z ćwiczeń w 

from random import sample
from itertools import combinations

class Card:
    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return f'{self.rank}{self.suit}'

# assumption: hand is sorted
class Hand:
    def __init__(self, hand) -> None:
        self.hand = hand
        self.ranks_dist = list(set([x.rank for x in self.hand]))
        self.ranks = [x.rank for x in self.hand]
        self.counts = [self.ranks.count(x) for x in self.ranks_dist]

        
        self.is_flush = self.check_flush()
        self.is_straight = self.check_straight()
        self.strength = self.calculate_strenght()

    def __str__(self) -> str:
        return ' '.join([str(x) for x in self.hand])
    
    def calculate_strenght(self) -> int:
        if self.is_straight and self.is_flush:
            return 8
        
        if self.check_4_of_a_kind():
            return 7
        
        if self.check_full():
            return 6
        
        if self.is_flush:
            return 5
        
        if self.is_straight:
            return 4
        
        if self.check_three_of_a_kind():
            return 3
        
        if self.check_two_pair():
            return 2
        
        if self.check_pair():
            return 1
        return 0
        
    def check_flush(self) -> bool:
        return all(x.suit == self.hand[0].suit for x in self.hand)

    # for hand of type A, we dont bother checking straight    
    def check_straight(self) -> bool:
        if self.ranks[0] in 'AKQJ':
            return False

        return(list(map(lambda x : int(x), self.ranks)) == list(range(int(self.ranks[0]), int(self.ranks[0])+5)))
    
    def check_4_of_a_kind(self) -> bool:
        if self.counts.count(4) != 0:
            return True
        return False
    
    def check_full(self) -> bool:
        if self.counts.count(3) != 0 and self.counts.count(2) != 0:
            return True
        return False
    
    def check_three_of_a_kind(self) -> bool:
        if self.counts.count(3) != 0:
            return True
        return False
    
    def check_two_pair(self) -> bool:
        if self.counts.count(2) == 2:
            return True
        return False

    def check_pair(self) -> bool:
        if self.counts.count(2) >= 1:
            return True
        return False

Deck_A = [Card(rank, suit) for rank in ('A', 'K', 'Q', 'J') for suit in ('c', 'h', 'd', 's')]
Deck_B = [Card(str(rank), suit) for rank in range(2, 11) for suit in ('c', 'h', 'd', 's')]


# hand_X composed of cards from deck_X
# True if A wins, False otherwise
def compare_hands(hand_A, hand_B):
    return hand_A.strength >= hand_B.strength

def create_hand(deck):
    id = sorted(sample(range(0, len(deck)), 5))
    res = [deck[i] for i in id]
    return Hand(res)

# approximation of player B getting a better hand
def approx_odds(n, deck_a = Deck_A, deck_b = Deck_B):
    res = 0
    for _ in range(n):
        h1 = create_hand(deck_a)
        h2 = create_hand(deck_b)
    
        if not compare_hands(h1, h2):
            # print(h1)
            # print(h2)
            # print()
            res += 1
    
    return res/n

def find_deck():
    for deck in combinations(Deck_B, 12):
       # print([str(x) for x in deck])
        odds = approx_odds(1000, Deck_A, deck)
        if odds > 0.5:
            return (deck, odds)
    
def pair_or_less_B():
    cnt = 0
    total = 0
    for hand_B in combinations(Deck_B, 5):
        h_b = Hand(hand_B)
        total += 1
        if h_b.strength == 0 or h_b.strength == 1:
            #print(h_b, h_b.strength)
            cnt += 1
    return (cnt, total)

if __name__ == '__main__':
    #print(approx_odds(1000, Deck_A, Deck_B))

   
    # observation: deck B has always at least one pair
    print(pair_or_less_B())
    # based on above, deck B has 316956 out of 376992 hands which are two pair or high card
    # we dont have to consider them
    # takes a while, much faster than brute forcing all options
    b_win, total = 0, 0
    for hand_B in combinations(Deck_B, 5):
        h_b = Hand(hand_B)
        # h_b loses
        if h_b.strength <= 1:
            continue

        for hand_A in combinations(Deck_A, 5):
            h_a = Hand(hand_A)
            if not compare_hands(h_a, h_b):
                b_win += 1
            total += 1

    # print(b_win, total)
    # result: 139193664/1646701056 ≈ 0.08452879986
  