from engine.model import player_id
from engine.game import Hand, Card, Player, Trick
import numpy as np
from typing import List, Dict, Tuple
from copy import deepcopy
from .train_agent import TrainAgent
'''
class used for human interaction with game
'''
class HumanAgent(Player):
    current_player_hand: List[Card]
    train_agent: TrainAgent
    def __init__(self, id: player_id, use_api = False):
        self.play_model = self.init_play_model()
        self.pick_model = self.init_pick_model()
        self.train_agent = TrainAgent()
        super().__init__(id)
    
    def pick_decision(self) -> bool:
        return np.random.choice([False, False, True]) # todo
    
    def play_decision(self, hand: Hand, trick: Trick) -> Card:
        # todo
        pass
        
    def random_choice(self, actions: List[Card]) -> Dict[str, Tuple[float, Card]]:
        card_choice = np.random.choice(actions)
        res = {}
        for card in actions:
            res[str(card.suit.value+card.num.value)] = ((1 if card == card_choice else 0), card)
        return res
        
    def play_card(self, hand: Hand, trick: Trick) -> Card:
        decision = self.play_decision(hand, trick)
        self.played_card(decision)
        trick.play(decision)
        return decision
