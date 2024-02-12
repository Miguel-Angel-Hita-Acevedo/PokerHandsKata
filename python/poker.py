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
        
        if number_of_kind:= self._same_of_kind(cards_dict):
            return number_of_kind
        
        if type_straight := self.type_of_straight():
            return type_straight
        
        if self._its_flush():
            return 'Flush' 
        
        return 'High Card'
    
    def type_of_straight(self):
        if not self._has_straight():
            return False
        if not self._its_flush():
            return 'Straight'
        if self.cards[0].value == 9:
            return 'Royal Flush'
        return 'Straight Flush'
        

    def _same_of_kind(self,cards_dict ):  
        posible_results =  {4: "Four of a Kind", 3: self._is_three_of_a_king(cards_dict), 2: "Pair"}

        if self._has_two_pair(cards_dict):
            return 'Two Pair'

        for key, value in posible_results.items():
            if key  in cards_dict.values():
                return value
        return None
    
    def _is_three_of_a_king(self, cards_dict):
        if 3 in cards_dict.values():
            if 2 in cards_dict.values():
                return 'Full House'
            return 'Three of a Kind'
    
    def _has_two_pair(self, cards_dict):
        equal_cards = 0
        for value in cards_dict.values():
            if value == 2:
                equal_cards +=1
        return  equal_cards >=2
    
    def _has_straight(self):
        previous_value = -1
        consecutive_cards = 1
        for card in self.cards:
            card.value = self._parse_to_numbers(card.value)
            if card.value != -1 and card.value == (previous_value + 1):
                consecutive_cards += 1
            previous_value = card.value

        if self.is_straight_with_as():
            consecutive_cards += 1
            
        return consecutive_cards == 5

    def is_straight_with_as(self):
        return self.cards[0].value == 2 and self.cards[self.cards.__len__() - 1].value == 13
        
    def _parse_to_numbers(self, card_value):
        dict_letters = {'J': 10, 'Q': 11, 'K': 12, 'A': 13}
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
    
    def _its_flush(self):
        last_color = ''
        
        for card in self.cards:
            if card.suit != last_color and last_color != '':
                return 
            last_color = card.suit
        return True