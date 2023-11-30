from enum import Enum
from typing import List
TOTAL_CARDS = 32
UNPLAYED = 'UNPLAYED'
MAX_POINTS = 50
class CardNum(Enum):
    seven = 0
    eight = 1
    nine = 2
    king = 3
    ten = 4
    ace = 5
    jack = 6
    queen = 7

class CardSuit(Enum):
    diamonds = 0
    hearts = 1
    spades = 2
    clubs = 3
    
class Team(Enum):
    picker_and_partner = 0
    defenders = 1

class player_id(Enum):
    a = 0
    b = 1
    c = 2
    d = 3
    e = 4        

suit_to_emoji = {
    CardSuit.diamonds: '♦️',
    CardSuit.spades: '♠️',
    CardSuit.clubs: '♣️',
    CardSuit.hearts: '❤️',
}
suit_one_hot = {
    UNPLAYED: [0, 0, 0, 0],
    CardSuit.spades: [1, 0, 0, 0],
    CardSuit.clubs: [0, 1, 0, 0],
    CardSuit.diamonds: [0, 0, 1, 0],
    CardSuit.hearts: [0, 0, 0, 1],   
}

num_one_hot = {
    UNPLAYED: [0, 0, 0, 0, 0, 0, 0, 0],
    CardNum.seven: [1, 0, 0, 0, 0, 0, 0, 0],
    CardNum.eight: [0, 1, 0, 0, 0, 0, 0, 0],
    CardNum.nine: [0, 0, 1, 0, 0, 0, 0, 0],
    CardNum.jack: [0, 0, 0, 1, 0, 0, 0, 0],
    CardNum.queen: [0, 0, 0, 0, 1, 0, 0, 0],
    CardNum.king: [0, 0, 0, 0, 0, 1, 0, 0],
    CardNum.ten: [0, 0, 0, 0, 0, 0, 1, 0],
    CardNum.ace: [0, 0, 0, 0, 0, 0, 0, 1],
}
# last bit is ued to signify if a card was played by the picker
picker_one_hot = {
    0: [0],
    1: [1],
}

card_point_map = {
    CardNum.seven: 0,
    CardNum.eight: 0,
    CardNum.nine: 0,
    CardNum.jack: 2,
    CardNum.queen: 3,
    CardNum.king: 4,
    CardNum.ten: 10,
    CardNum.ace: 11,
}

'''
game state: 
    There are 5 cards played per trick, and 6 tricks played per hand
    One card has a suit and a number
    four suits, 8 cards. 1x12 array
    alternatively, there are 32 unique cards. We could one hot to be 1x32 if the model is confused by the 1x12 format in future testing
    we also need a last bit to say whether or not the card was played by the picker - 1x13
    [[Card, Card, Card, Card, Card], [unplayed... and so on], [], [], []]
    in total, the input should be a matrix of shape 6x5x13
'''