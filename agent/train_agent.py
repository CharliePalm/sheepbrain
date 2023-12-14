import numpy as np
from engine.game import Hand, Trick, Card
from engine.model import suit_one_hot, num_one_hot, picker_one_hot
from typing import List
class TrainAgent:
    def __init__(self):
        pass
    
    def handle_endgame(self):
        pass
    
    def compile_game_state(self, hand: Hand, trick: Trick) -> np.ndarray:
        network_input = np.zeros((6, 5, 13))
        hand.tricks.append(trick)
        for idx, trick in enumerate(hand.tricks):
            for jdx, card in enumerate(trick.cards):
                network_input[idx][jdx] = self.get_card_one_hot(card, hand)
        hand.tricks.pop()
        return network_input
    
    def get_card_one_hot(self, card: Card, hand: Hand) -> List[int]:
        return suit_one_hot[card.suit] + num_one_hot[card.num] + picker_one_hot[card.parent == hand.picker_id]
    
    def compile_pick_state(self, player_hand: List[Card]) -> np.ndarray:
        network_input = np.empty((6, 12))
        for idx, card in enumerate(player_hand):
            network_input[idx] = suit_one_hot[card.suit] + num_one_hot[card.num]

