from collections import namedtuple

GameState = namedtuple('GameState', ['player_states', 'player_order'])
PlayerState = namedtuple('PlayerState', ['card1', 'card2', 'card1alive', 'card2alive', 'number_of_coins'])

class Move(namedtuple('Move', ['player_id', 'move_type', 'target_player_id', 'number_of_coins'])):
    def __new__(cls, player_id, move_type, target_player_id=None, number_of_coins=None):
        return super(Move, cls).__new__(cls, player_id, move_type, target_player_id, number_of_coins)

# card types
AMBASSADOR = 10
CAPTAIN = 11
CONTESSA = 12
DUKE = 13
ASSASSIN = 14

# move types
INCOME = 21
FOREIGN_AID = 22
TAX = 23
SWAP = 24
STEAL = 25
ASSASSINATE = 26
COUP = 27

# move responses
OK = 31
NO_YOU_DONT_HAVE = 32
NO_I_HAVE_DUKE = 33
NO_I_HAVE_AMBASSADOR = 34
NO_I_HAVE_CAPTAIN = 35
NO_I_HAVE_CONTESSA = 36
REVEAL_CARD_1 = 37
REVEAL_CARD_2 = 38

class Player:
	next_id = 1
	def __init__(self):
		self.id = Player.next_id
		Player.next_id += 1
	
	def choose_move(self, game_state, history):
		#options: INCOME, FOREIGN_AID, TAX, SWAP, STEAL, ASSASSINATE, COUP
		raise NotImplementedError()
	def respond_to_claim_opponent_has_card(self, opponent_id, card, game_state, history):
		#options: OK, NO_YOU_DONT_HAVE
		raise NotImplementedError()
	def respond_to_foreign_aid(self, move, game_state, history):
		#options: OK, NO_I_HAVE_DUKE
		raise NotImplementedError()
	def respond_to_steal_from_me(self, move, game_state, history):
		#options: OK, NO_YOU_DONT_HAVE, NO_I_HAVE_AMBASSADOR, NO_I_HAVE_CAPTAIN
		raise NotImplementedError()
	def respond_to_assassinate_me(self, move, game_state, history):
		#options: OK, NO_YOU_DONT_HAVE, NO_I_HAVE_CONTESSA
		raise NotImplementedError()
	def choose_which_card_to_lose(self, move, game_state, history):
		#options: REVEAL_CARD_1, REVEAL_CARD_2
		raise NotImplementedError()
	
	def show_game_state(self, game_state):
		pass
	def show_move(self, game_state, move):
		pass
