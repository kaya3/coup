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
	
	def respond_to_claim_opponent_has_card(self, opponent_id, card, game_state, history):
		self.show_game_state(game_state)
		
		response_str = input('Opponent ' + str(opponent_id) + ' claims to have ' + card_to_str(card) + ': ').upper()
		if response_str == 'OK':
			return OK
		elif response_str == 'NO':
			return NO_YOU_DONT_HAVE
		else:
			raise ValueError()
	def respond_to_foreign_aid(self, move, game_state, history):
		return self.respond_to_move(move, game_state, history)
	def respond_to_steal_from_me(self, move, game_state, history):
		return self.respond_to_move(move, game_state, history)
	def respond_to_assassinate_me(self, move, game_state, history):
		return self.respond_to_move(move, game_state, history)
	def choose_which_card_to_lose(self, game_state, history):
		p_st = game_state.player_states[self.id]
		
		response_str = input('Choose which card to lose (' + card_to_str(p_st.card1) + ' or ' + card_to_str(p_st.card2) + '): ').upper()
		response_card = card_from_str(response_str)
		
		if response_card == p_st.card1:
			return REVEAL_CARD_1
		elif response_card == p_st.card2:
			return REVEAL_CARD_2
		else:
			return None
	def choose_which_cards_to_keep(self, cards, number_of_cards, game_state, history):
		p_st = game_state.player_states[self.id]
		
		response_str = input('Choose ' + str(number_of_cards) + ' cards to keep (of '
			+ ', '.join(card_to_str(c) for c in cards)
		 	+ '): ').upper()
		return [ card_from_str(c.strip()) for c in response_str.split(' ') ]
	
	def respond_to_move(self, move, game_state, history):
		self.show_game_state(game_state)
		self.show_move(game_state, move)
		
		response_str = input('Enter your response: ').upper()
		
		if response_str == 'OK':
			return OK
		elif response_str == 'NO':
			return NO_YOU_DONT_HAVE
		elif move.move_type == FOREIGN_AID:
			if response_str == 'BLOCK DUKE':
				return NO_I_HAVE_DUKE
			else:
				raise ValueError(response_str)
		elif move.move_type == STEAL:
			if move.target_player_id != self.id:
				raise ValueError(move.target_player_id)
			if response_str == 'BLOCK AMBASSADOR':
				return NO_I_HAVE_AMBASSADOR
			elif response_str == 'BLOCK CAPTAIN':
				return NO_I_HAVE_CAPTAIN
			else:
				raise ValueError(response_str)
		elif move.move_type == ASSASSINATE:
			if move.target_player_id != self.id:
				raise ValueError(move)
			if response_str == 'BLOCK CONTESSA':
				return NO_I_HAVE_CONTESSA
			else:
				raise ValueError(response_str)
		else:
			raise ValueError(move)

	def show_game_state(self, game_state):
		for p_id, p_st in game_state.player_states.items():
			print('Player {p_id} has {card1}, {card2} and {number_of_coins} coins.'.format(
				p_id = p_id,
				card1 = card_to_str(p_st.card1) + ('' if p_st.card1alive else ' (dead)'),
				card2 = card_to_str(p_st.card2) + ('' if p_st.card2alive else ' (dead)'),
				number_of_coins = p_st.number_of_coins
			))
	
	def show_move(self, game_state, move):
		m_t = move.move_type
		move = {
			'player_id': move.player_id,
			'target_player_id': move.target_player_id,
			'number_of_coins': move.number_of_coins,
		}
		if m_t == INCOME:
			print('Player {player_id} took income.'.format(**move))
		elif m_t == FOREIGN_AID:
			print('Player {player_id} attempted to take foreign aid.'.format(**move))
		elif m_t == TAX:
			print('Player {player_id} attempted to take tax.'.format(**move))
		elif m_t == SWAP:
			print('Player {player_id} attempted to swap cards.'.format(**move))
		elif m_t == STEAL:
			print('Player {player_id} attempted to steal {number_of_coins} from Player {target_player_id}.'.format(**move))
		elif m_t == ASSASSINATE:
			print('Player {player_id} attempted to assassinate {target_player_id}.'.format(**move))
		elif m_t == COUP:
			print('Player {player_id} made a coup against {target_player_id}.'.format(**move))
		else:
			raise ValueError(m_t)
