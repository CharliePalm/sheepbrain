import engine.model as model
import engine.game as game
from numpy.random import shuffle
from typing import List, Dict
from .player_agent import PlayerAgent
from numpy.random import choice
class GameAgent:
    deck: List[game.Card] = []
    player_agents: Dict[model.player_id, PlayerAgent] = {}
    scoreboard: Dict[model.player_id, int] = {}
    leader: game.player_id
    hand: game.Hand
    verbose: bool
    
    def __init__(self, verbose = False):
        self.init_deck()
        self.verbose = verbose
    
    def init_deck(self):
        self.deck = []
        for card_num in model.CardNum:
            for card_suit in model.CardSuit:
                self.deck.append(game.Card(card_suit, card_num))

    def shuffle_deck(self):
        shuffle(self.deck)
    
    def deal_cards(self):
        curr_player = self.prev_player(self.player_agents[self.leader])
        for card in self.deck[0:30]: # blind of size 2
            curr_player.deal_card(card)
            curr_player = self.next_player(curr_player)        
        self.hand.blind = self.deck[30:32]

    def next_player(self, p: PlayerAgent):
        return self.player_agents[p.left_player()]

    def prev_player(self, p: PlayerAgent):
        return self.player_agents[p.left_player()]
    
    def determine_picker(self):
        curr_player = self.player_agents[self.leader]
        for i in range(5):
            if curr_player.pick_decision():
                self.hand.picker_id = curr_player.id
                self.hand.blind = curr_player.post_pick_decision(self.hand.blind)
                self.find_partner()
                return
            curr_player = self.next_player(curr_player)
    
    def find_partner(self):
        picker = self.player_agents[self.hand.picker_id]
        picker_jacks = map(lambda x: x.suit, filter(lambda x: x.num == game.CardNum.jack, picker.current_player_hand))
        partner_jack_suit = None
        for suit in game.CardSuit:
            if suit not in picker_jacks:
                partner_jack_suit = suit
                break
        if not partner_jack_suit:
            return
        for p_id in self.player_agents:
            if p_id != self.hand.picker_id:
                for c in self.player_agents[p_id].current_player_hand:
                    if c.suit == partner_jack_suit:
                        self.hand.partner_id = p_id
                        return
                    
    
    def trick(self):
        player = self.player_agents[self.leader]
        trick = game.Trick()
        for i in range(5):
            player.play_card(self.hand, trick)
            player = self.next_player(player)
            if self.verbose:
                # print(model.suit_to_emoji[trick.cards[-1].suit], trick.cards[-1].num.value)
                pass
        winning_card = trick.get_winning_card()
        self.leader = self.player_agents[winning_card.parent].id
        self.hand.tricks.append(trick)

    
    def update_score(self):
        points = self.hand.get_outcome_points()
        for id in self.player_agents:
            if id == self.hand.picker_id:
                self.scoreboard[self.hand.picker_id] += points['picker']
            elif id == self.hand.partner_id:
                self.scoreboard[self.hand.partner_id] += points['partner']
            else:
                self.scoreboard[id] += points['defender']
        if self.verbose:
           print(self.scoreboard)
        if sum(list(dict.values(self.scoreboard))) != 0:
            print('sum error')
            exit(1)

    
    def commence(self):
        for id in model.player_id:
            self.player_agents[id] = PlayerAgent(id)
            self.scoreboard[id] = 0
        self.leader = choice(list(self.player_agents.keys()))
        while max(dict.values(self.scoreboard)) < model.MAX_POINTS:
            self.hand = game.Hand()
            self.shuffle_deck()
            self.deal_cards()
            
            self.determine_picker()
            if not self.hand.picker_id:
                continue # TODO handle 'leaster' hand
            for _ in range(6):
                self.trick()
            self.update_score()
