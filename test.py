from unittest import TestCase, main
from engine import game, model
from agent.player_agent import PlayerAgent
from agent.game_agent import GameAgent
from copy import deepcopy

class TestAgent(TestCase):
    agent = GameAgent()
    def test_deck_init(self):
        self.assertEqual(len(self.agent.deck), model.TOTAL_CARDS)
        for suit in model.CardSuit:
            self.assertEqual(len(list(filter(lambda x: x.suit == suit, self.agent.deck))), 8)
        for num in model.CardNum:
            self.assertEqual(len(list(filter(lambda x: x.num == num, self.agent.deck))), 4)
    
    def test_point_total(self):
        s = 0
        for card in self.agent.deck:
            s += model.card_point_map[card.num]
        self.assertEqual(s, 120)

class TestCards(TestCase):
    def test_player(self):
        pass
    
class TestPlayerAgent(TestCase):
    agent = PlayerAgent(model.player_id.a)
    def test_one_hot(self):
        card = game.Card(model.CardSuit.spades, model.CardNum.ace)
        card.parent = 0
        hand = game.Hand()
        hand.picker = game.Player(model.player_id.a)
        result = self.agent.get_card_one_hot(card, hand)
        self.assertEqual(result, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])

class TestGame(TestCase):
    def test_card_compare(self):
        seven_diamonds = game.Card(model.CardSuit.diamonds, model.CardNum.seven)
        for suit in model.CardSuit:
            if suit != model.CardSuit.diamonds:
                for num in model.CardNum:
                    if num not in [model.CardNum.queen, model.CardNum.jack]:
                        self.assertTrue(seven_diamonds.is_higher(game.Card(suit, num), suit)) # seven of trump beats any non trump
    
    def test_face_cards(self):
        jack_diamonds = game.Card(model.CardSuit.diamonds, model.CardNum.jack)
        for suit in model.CardSuit:
            if suit != model.CardSuit.diamonds:
                self.assertFalse(jack_diamonds.is_higher(game.Card(suit, model.CardNum.jack), suit))
        for suit in model.CardSuit:
            self.assertFalse(jack_diamonds.is_higher(game.Card(suit, model.CardNum.queen), suit))
        for num in model.CardNum:
            if num not in [model.CardNum.queen, model.CardNum.jack]:
                self.assertTrue(jack_diamonds.is_higher(game.Card(model.CardSuit.diamonds, num), model.CardSuit.clubs))
        
    def test_led_suit(self):
        ace_spades = game.Card(model.CardSuit.spades, model.CardNum.ace)
        seven_clubs = game.Card(model.CardSuit.clubs, model.CardNum.seven)
        self.assertTrue(seven_clubs.is_higher(ace_spades, model.CardSuit.clubs))
        self.assertFalse(seven_clubs.is_higher(ace_spades, model.CardSuit.spades))

    def test_next_player(self):
        p = game.Player(game.player_id.a)
        self.assertEqual(p.left_player(), game.player_id.b)
        p.id = game.player_id.b
        self.assertEqual(p.left_player(), game.player_id.c)
        p.id = game.player_id.c
        self.assertEqual(p.left_player(), game.player_id.d)
        p.id = game.player_id.d
        self.assertEqual(p.left_player(), game.player_id.e)
        p.id = game.player_id.e
        self.assertEqual(p.left_player(), game.player_id.a)

    def test_next_player(self):
        p = PlayerAgent(game.player_id.a)
        self.assertEqual(p.right_player(), game.player_id.e)
        p.id = game.player_id.b
        self.assertEqual(p.right_player(), game.player_id.a)
        p.id = game.player_id.c
        self.assertEqual(p.right_player(), game.player_id.b)
        p.id = game.player_id.d
        self.assertEqual(p.right_player(), game.player_id.c)
        p.id = game.player_id.e
        self.assertEqual(p.right_player(), game.player_id.d)

if __name__ == '__main__': main()