from defs import *

class TextPlayer(Player):
	def choose_move(self, game_state, history):
		self.show_game_state(game_state)
		
		move_str = input('Choose your move: ').upper()
		
		if move_str == 'INCOME':
			return Move(self.id, INCOME)
		elif move_str == 'FOREIGN AID':
			return Move(self.id, FOREIGN_AID)
		elif move_str == 'TAX':
			return Move(self.id, TAX)
		elif move_str == 'SWAP':
			return Move(self.id, SWAP)
		elif move_str not in ['STEAL', 'ASSASSINATE', 'COUP']:
			return None
		
		opponent_str = input('Which opponent: ')
		opponent_id = int(opponent_str)
		
		if move_str == 'STEAL':
			coins_str = input('How many coins: ')
			coins = int(coins_str)
			return Move(self.id, STEAL, opponent_id, coins)
		elif move_str == 'ASSASSINATE':
			return Move(self.id, ASSASSINATE, opponent_id)
		elif move_str == 'COUP':
			return Move(self.id, COUP, opponent_id)
		else:
			return None
	
	def respond_to_move(self, game_state, move, options, history):
		self.show_game_state(game_state)
		self.show_move(game_state, move)
		
		response_str = input('Enter your response: ').upper()
		
		if response_str == 'OK':
			return OK
		elif response_str == 'NO':
			return NO_YOU_DONT_HAVE
		elif move.move_type == FOREIGN_AID and response_str == 'BLOCK DUKE':
			return NO_I_HAVE_DUKE
		elif move.move_type == STEAL and move.target_player_id == self.id and response_str == 'BLOCK AMBASSADOR':
			return NO_I_HAVE_AMBASSADOR
		elif move.move_type == STEAL and move.target_player_id == self.id and response_str == 'BLOCK CAPTAIN':
			return NO_I_HAVE_CAPTAIN
		elif move.move_type == ASSASSINATE and move.target_player_id == self.id and response_str == 'BLOCK CONTESSA':
			return NO_I_HAVE_CONTESSA
		elif move.move_type in ['ASSASSINATE', 'COUP'] and move.target_player_id == self.id:
			if response_str == 'REVEAL AMBASSADOR':
				return REVEAL_AMBASSADOR
			elif response_str == 'REVEAL CAPTAIN':
				return REVEAL_CAPTAIN
			elif response_str == 'REVEAL CONTESSA':
				return REVEAL_CONTESSA
			elif response_str == 'REVEAL DUKE':
				return REVEAL_DUKE
			elif response_str == 'REVEAL ASSASSIN':
				return REVEAL_ASSASSIN
			else:
				return None
		else:
			return None

	def show_game_state(self, game_state):
		print(game_state) #TODO
	
	def show_move(self, game_state, move):
		print(move) #TODO
