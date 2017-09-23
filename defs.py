from collections import namedtuple

GameState = namedtuple('GameState', ['player_states', 'whose_turn'])
PlayerState = namedtuple('PlayerState', ['card1', 'card2', 'number_of_coins'])

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
REVEAL_AMBASSADOR = 37
REVEAL_CAPTAIN = 38
REVEAL_CONTESSA = 39
REVEAL_DUKE = 40
REVEAL_ASSASSIN = 41

class Player:
	next_id = 1
	def __init__(self):
		self.id = Player.next_id
		Player.next_id += 1
	
	def choose_move(self, game_state, history):
		raise NotImplementedError()
	def respond_to_move(self, game_state, move, options, history):
		raise NotImplementedError()
	def show_game_state(self, game_state):
		pass
	def show_move(self, game_state, move):
		pass
