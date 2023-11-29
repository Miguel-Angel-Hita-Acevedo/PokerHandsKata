VALUES = '23456789TJQKA'
SUITS = 'HDSC'

HAND_RANKS = (
    'High Card',
    'Pair',
    'Two Pair',
    'Three of a Kind',
    'Straight',# escalera sin importar color
    'Flush',# color (no necesita ser escalera ni nada)
    'Full House',# 3 y 2
    'Four of a Kind',
    'Straight Flush',# escalera de color
    'Royal Flush'# 10, J, Q, K, A -> del mismo palo
)

class Card:
    """
    Represents a single playing card. Initialise with a two-character string in
    the form <value><suit> e.g. AS for the ace of spades:

    >>> card = Card('AS')
    """
    def __init__(self, value_suit):
        value, suit = value_suit
        if value not in VALUES:
            raise ValueError
        self.value = value
        if suit not in SUITS:
            raise ValueError
        self.suit = suit

    def __repr__(self):
        return '<Card object {}>'.format(self)

    def __str__(self):
        return '{}{}'.format(self.value, self.suit)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value_index < other.value_index

    def __gt__(self, other):
        return self.value_index > other.value_index

    @property
    def value_index(self):
        return VALUES.index(self.value)


class PokerHand:
    """
    Represents a hand of five cards. Initialise with five 2-character strings
    each separated by a space, e.g:

    >>> hand = PokerHand('3D JC 8S 4H 2C')

    Evaluate the hand rank by accessing the rank property:

    >>> hand.rank
    'High Card'
    """
    def __init__(self, cards):
        cards = cards.split(' ')
        self.cards = [Card(sv) for sv in cards]
        card_set = {repr(card) for card in cards}
        duplicate_cards = len(card_set) < len(cards)
        if duplicate_cards:
            raise ValueError
        self.cards = sorted(self.cards)
        

    def __repr__(self):
        card_strings = (str(card) for card in self)
        return '<PokerHand object ({})>'.format(', '.join(card_strings))

    def __iter__(self):
        return iter(self.cards)

    def __gt__(self, other):
        return self.cards[-1] > other.cards[-1]

    def __lt__(self, other):
        return self.cards[-1] < other.cards[-1]

    def __eq__(self, other):
        return self.cards[-1] == other.cards[-1]

    @property
    def rank(self):
        cards_dict = self._get_number_of_each_card()
        if 4 in cards_dict.values():
            return 'Four of a Kind'
        elif 3 in cards_dict.values():
            return 'Three of a Kind'
        elif self._has_two_pair(cards_dict):
            return 'Two Pair'
        elif 2 in cards_dict.values():
            return 'Pair'
        elif self._has_straight():
            return 'Straight'
        return 'High Card'
    
    def _has_two_pair(self, cards_dict):
        equal_cards = 0
        for value in cards_dict.values():
            if value == 2:
                equal_cards +=1
        return  equal_cards >=2
    
    def _has_straight(self):
        current_value = 0
        previous_value = -1
        combo = 0
        for card in self.cards:
            current_value = self._parse_to_numbers(card.value)
            if current_value != -1 and current_value == (previous_value + 1):
                combo += 1
            previous_value = current_value
        return combo == 4

    def _parse_to_numbers(self, card_value):
        dict_letters = {'J': 10, 'Q': 11, 'K': 12, 'A': 1}
        if card_value in dict_letters:
            return dict_letters.get(card_value)
        return int(card_value)

    def _get_number_of_each_card(self):
        last_value = None
        pairs_count = 0
        three_count = 0
        equal_count = 1
        cards_dict = {}
        for  card in self.cards:
            if  card.value in cards_dict.keys():
                #cards_dict[card.value] = cards_dict[card.value] + 1
                cards_dict.update({card.value:cards_dict[card.value]+1})

            else:
                cards_dict[card.value] = 1    
        return cards_dict



# for card in self.cards:
#            if card.value == last_value:
#                equal_count += 1
#            else:
#                equal_count = 1

#            if equal_count == 2:
#                pairs_count += 1
#            elif equal_count == 3:
#                three_count += 1
#            last_value = card.value