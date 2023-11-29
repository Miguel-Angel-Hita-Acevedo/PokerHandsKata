from poker import PokerHand

# test high card rank
hand = PokerHand('3D JC 8S 4H 2C')
assert hand.rank == 'High Card', hand.rank
hand = PokerHand('AH AD 8C 4S 7H')
assert hand.rank == 'Pair', hand.rank
hand = PokerHand('AH 3D TC 4S 3S')
assert hand.rank == 'Pair', hand.rank

hand = PokerHand('AH 3D 4C 4S 3S')
assert hand.rank == 'Two Pair', hand.rank

hand = PokerHand('AH 4D 4C 4S 3S')
assert hand.rank == 'Three of a Kind', hand.rank

hand = PokerHand('2D 5H 4D 6S 3H')
assert hand.rank == 'Straight', hand.rank

hand = PokerHand('9D JC 8S 6H 7C')
assert hand.rank == 'Straight', hand.rank

#hand = PokerHand('AH 1H 2H 4H 4H')
#assert hasnd.rank == 'Flush', hand.rank

hand = PokerHand('AH 4D 4C 4H 4S')
assert hand.rank == 'Four of a Kind', hand.rank
# keep this at the end - it will only show if all your tests pass
print('Tests passing!')
