from engine.model import picker_one_hot, num_one_hot, suit_one_hot, player_id
from engine.game import Hand, Card, Player, Trick
import numpy as np
from typing import List, Dict, Tuple
from copy import deepcopy
from .train_agent import TrainAgent
'''
class to be used for making decisions about a game state
'''
class PlayerAgent(Player):
    current_player_hand: List[Card]
    train_agent: TrainAgent
    def __init__(self, id: player_id):
        self.play_model = self.init_play_model()
        self.pick_model = self.init_pick_model()
        self.train_agent = TrainAgent()
        super().__init__(id)

    def init_play_model(self):
        return None #todo
    def init_pick_model(self):
        return None #todo
    
    def pick_decision(self) -> bool:
        return np.random.choice([False, False, True]) # todo

    def post_pick_decision(self, blind: List[Card]) -> None:
        '''
        given a blind, sets own hand according to own policy
        '''
        self.current_player_hand = list(np.random.choice(self.current_player_hand + blind, 6, False))
        for card in self.current_player_hand:
            card.parent = self.id
    
    def play_decision(self, hand: Hand, trick: Trick) -> Card:
        # get valid action states
        valid_actions = []
        model_input = []
        for action in self.get_valid_actions(trick):
            trick.cards.append(action)
            model_input.append(self.train_agent.compile_game_state(hand, trick))
            valid_actions.append(action)
            trick.cards.pop()
        results = self.play_model.predict(model_input) if self.play_model else self.random_choice(valid_actions)
        # find valid state with highest expected reward
        m = np.NINF
        max_key = None
        for r in results:
            if results[r][0] > m:
                m = results[r][0]
                max_key = r
        return results[max_key][1]
        
    def get_valid_actions(self, trick: Trick):
        needs_to_follow_suit = False
        if trick.led_suit:
            for card in self.current_player_hand:
                needs_to_follow_suit = (card.suit == trick.led_suit)
                if needs_to_follow_suit:
                    break
        for card in self.current_player_hand:
            if not needs_to_follow_suit or card.suit == trick.led_suit:
                yield card

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
