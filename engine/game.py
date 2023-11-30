from engine.model import CardNum, CardSuit, Team, player_id, card_point_map
from typing import List, Dict
from numpy.random import choice

class Card:
    num: CardNum
    suit: CardSuit
    parent: player_id
    
    def __init__(self, suit: CardSuit, num: CardNum):
        self.num = num
        self.suit = suit

    def is_trump(self):
        return self.suit == CardSuit.diamonds or self.num == CardNum.jack or self.num == CardNum.queen

    def deal(self, dealt_to: str):
        self.parent = dealt_to
    
    def is_higher(self, other_card, led_suit: CardSuit) -> bool:
        if (not self.is_trump()) and other_card.is_trump():
            return False
        if self.is_trump() and (not other_card.is_trump()):
            return True
        elif self.is_trump() and other_card.is_trump():
            return (self.num.value > other_card.num.value) or (self.num.value == other_card.num.value and self.suit.value > other_card.suit.value)
        # both not trump
        return (self.suit == led_suit and other_card.suit != led_suit) or (self.suit == led_suit and self.num.value > other_card.num.value)

class Player:
    current_player_hand: List[Card]
    id: player_id
    def __init__(self, id: player_id):
        self.init(id)
    
    def init(self, id):
        self.current_player_hand = []
        self.tricks = []
        self.id = id if id else self.id
    
    def deal_card(self, card: Card):
        self.current_player_hand.append(card)
        card.parent = self.id
    
    def played_card(self, card: Card):
        to_rem = self.find_card(card)
        self.current_player_hand.remove(to_rem)
        
    def find_card(self, card: Card):
        for search_card in self.current_player_hand:
            if search_card.suit == card.suit and search_card.num == card.num:
                return card
        return None
    
    def left_player(self) -> player_id:
        return list(player_id)[((self.id.value + 1) % 5)]
    def right_player(self) -> player_id:
        return list(player_id)[((self.id.value - 1) % 5)]
    
class Trick:
    cards: List[Card]
    winning_card: Card
    points: int
    led_suit: CardSuit
    
    def __init__(self):
        self.cards = []
        self.led_suit = None
        self.winning_card = None
        self.points = 0
        
    def play(self, card: Card):
        self.cards.append(card)
        if len(self.cards) == 1:
            self.led_suit = card.suit
            self.winning_card = card
        elif card.is_higher(self.winning_card, self.led_suit):
            self.winning_card = card
        self.points += card_point_map[card.num]
    
    def get_winning_card(self):
        return self.winning_card

    def get_points(self):
        return self.points

class Hand:
    tricks: List[Trick]
    blind: List[Card]
    picker_id: player_id
    partner_id: player_id

    def __init__(self):
        self.init()
        
    def init(self):
        self.tricks = []
        self.blind = []
        self.picker_id = None
        self.partner_id = None
    
    def start(self, picker: Player, partner_jack = CardSuit.diamonds):
        self.picker_id = picker.id

    def get_final_defender_points(self) -> int:
        total = 0
        for trick in self.tricks:
            if trick.winning_card.parent not in [self.picker_id, self.partner_id if self.partner_id else None]: total += trick.get_points()
        return total
    
    def get_outcome_points(self):
        outcome = self.get_final_defender_points()
        picker_points, defender_points = 0, 0
        if outcome == 120:
            picker_points = 6
            defender_points = -3
        elif outcome > 90:
            picker_points = 4
            defender_points = -2
        elif outcome > 60:
            picker_points = 2
            defender_points = -1
        elif outcome > 30:
            picker_points = -2
            defender_points = 1
        elif outcome > 0:
            picker_points = -4
            defender_points = 2
        else:
            picker_points = -6
            defender_points = 3
        partner_points = defender_points * -1
        if not partner_points:
            picker_points *= 2
            partner_points = 0
        return {
            'picker': picker_points,
            'partner': partner_points, 
            'defender': defender_points
        }