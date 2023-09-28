from poker import PokerHand

# test high card rank
hand = PokerHand('3D JC 8S 4H 2C')
assert hand.rank == 'High Card', hand.rank
hand = PokerHand('AH AD 8C 4S 7H')
assert hand.rank == 'Pair', hand.rank
hand = PokerHand('AH 3D TC 4S 3S')
assert hand.rank == 'Pair', hand.rank
# keep this at the end - it will only show if all your tests pass
print('Tests passing!')
