from engine.game import Card
from engine.model import player_id
from typing import Dict, Set
import numpy as np
class Node:
    r: float
    r_term: float
    parent_id: player_id
    depth: int
    explored: bool
    v: int
    data_in: np.ndarray
    def __init__(self, parent_id):
        self.parent_id = parent_id

class HandSet:
    '''
    A tree represents one hand
    '''
    nodes: Set[Node]
    player_rewards: Dict[player_id, int]
    
    def __init__(self):
        self.nodes = set()
    
    def add(self, card: Card, data: np.ndarray) -> None:
        self.nodes.add(Node(card.parent_id), data)
    
    def propagate(self) -> None:
        for node in self.nodes:
            player_value = self.player_rewards[node.parent_id]
            node.r_term = player_value
            
    def end_hand(self, rewards):
        self.player_rewards = rewards
        self.propagate()