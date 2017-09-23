from defs import *
from random import choice, shuffle

class RandomAI(Player):

	def dukesout(self, game_state):
		kingcount = 0
		for player in game_state.player_states:
			if player.card1alive and player.card1 == DUKE:
				kingcount += 1
			if player.card2alive and player.card2 == DUKE:
				kingcount += 1
		if kingcount == 3:
			return True
		return False


	def choose_move(self, game_state, history):
		options = [INCOME, FOREIGN_AID, TAX, SWAP]
		coins = game_state.player_states[self.id].number_of_coins
		opponent_ids = [ i for i in game_state.player_states if i != self.id ]
		stealable_opponent_ids = [ i for i in opponent_ids if game_state.player_states[i].number_of_coins >= 1 ]
		
		if self.dukesout:
			options.remove(TAX)
		
		#coup players with a single card
		if game_state.player_states[self.id].number_of_coins > 6:    
			player_card_count = {
			p_id: int(player.card1alive)+int(player.card2alive)
			for p_id, player in game_state.player_states.items()
			}
			for player, card in game_state.player_states.player_card_count.items():
				if card == 1:
					return Move(self.id, COUP, player)
				else:
					return Move(self.id, COUP, choice(opponent_ids))

		

		if coins >= 3:
			options.append(ASSASSINATE)
		if coins >= 7:
			options.append(COUP)
		if stealable_opponent_ids:
			options.append(STEAL)
			m_t = choice(options)

		if m_t in [INCOME, FOREIGN_AID, TAX, SWAP]:
			return Move(self.id, m_t)

		if m_t != STEAL:
			target_player_id = choice(opponent_ids)
			return Move(self.id, m_t, target_player_id)
		else:
			target_player_id = choice(stealable_opponent_ids)
			c = game_state.player_states[target_player_id].number_of_coins
			
		return Move(self.id, STEAL, target_player_id, (2 if c >= 2 else 1))

	def respond_to_claim_opponent_has_card(self, opponent_id, card, game_state, history):
		return OK
	def respond_to_foreign_aid(self, move, game_state, history):
		return OK
	def respond_to_steal_from_me(self, move, game_state, history):
		return OK
	def respond_to_assassinate_me(self, move, game_state, history):
		return OK
	def choose_which_card_to_lose(self, game_state, history):
		return choice([REVEAL_CARD_1, REVEAL_CARD_2])
	def choose_which_cards_to_keep(self, cards, number_of_cards, game_state, history):
		cards = list(cards)
		shuffle(cards)
		return cards[:number_of_cards]
    
    
    
