from defs import *
from random import shuffle
from collections import deque

class Game:
	def __init__(self, *players):
		self.players = { p.id: p for p in players }
		
		self.deck = [ AMBASSADOR, CAPTAIN, CONTESSA, DUKE, ASSASSIN ]*3
		self.shuffle()
		
		self.player_states = {
			p.id: PlayerState(self.draw_card(), self.draw_card(), True, True, 2)
			for p in players
		}
		self.player_order = deque( p.id for p in players )
		
		self.history = []
	def shuffle(self):
		shuffle(self.deck)
	def draw_card(self):
		return self.deck.pop()
	def replace_cards(self, *cards):
		self.deck.extend(cards)
		self.shuffle()
	
	def get_player_coins(self, player_id):
		return self.player_states[player_id].number_of_coins
	def adjust_player_coins(self, player_id, d_coins):
		s = self.player_states[player_id]
		s = PlayerState(s.card1, s.card2, s.card1alive, s.card2alive, s.number_of_coins+d_coins)
		self.player_states[player_id] = s
	
	def player_number_of_lives(self, player_id):
		p_st = self.player_states[player_id]
		return int(p_st.card1alive) + int(p_st.card2alive)
	
	def move_valid(self, move):
		if move is None:
			raise ValueError()
		
		m_t = move.move_type
		p_id = move.player_id
		t_id = move.target_player_id
		
		if p_id != self.player_order[0]:
			return False
		elif self.get_player_coins(p_id) >= 10 and m_t != COUP:
			return False
		elif m_t in [INCOME, FOREIGN_AID, TAX, SWAP]:
			return True
		elif t_id == p_id or t_id not in self.players:
			return False
		elif m_t == ASSASSINATE:
			return self.get_player_coins(p_id) >= 3
		elif m_t == COUP:
			return self.get_player_coins(p_id) >= 7
		elif m_t == STEAL:
			c = self.get_player_coins(t_id)
			return move.number_of_coins >= 1 and move.number_of_coins <= min(c, 2)
		else:
			return False
	
	def state_visible_to_player(self, player_id):
		return GameState({
			i: PlayerState(
				s.card1 if i == player_id or not s.card1alive else HIDDEN,
				s.card2 if i == player_id or not s.card2alive else HIDDEN,
				s.card1alive,
				s.card2alive,
				s.number_of_coins
			)
			for i,s in self.player_states.items()
		}, tuple(self.player_order))
	
	def get_opponents(self, player_id):
		p_o = list(self.player_order)
		i = p_o.index(player_id)
		return p_o[i+1:] + p_o[:i]
	
	def player_can_reveal_card(self, player_id, card):
		p_st = self.player_states[player_id]
		if p_st.card1 == card and p_st.card1alive:
			self.replace_cards(card)
			self.player_states[player_id] = PlayerState(
				card1 = self.draw_card(),
				card2 = p_st.card2,
				card1alive = True,
				card2alive = p_st.card2alive,
				number_of_coins = p_st.number_of_coins
			)
			return True
		elif p_st.card2 == card and p_st.card2alive:
			self.replace_cards(card)
			self.player_states[player_id] = PlayerState(
				card2 = p_st.card1,
				card1 = self.draw_card(),
				card1alive = p_st.card1alive,
				card2alive = True,
				number_of_coins = p_st.number_of_coins
			)
			return True
		else:
			self.player_loses_life(player_id)
			return False
	
	def player_successfully_claims_to_have_card(self, player_id, card, opponents=None):
		if opponents is None:
			opponents = self.get_opponents(player_id)
		
		for o_id in opponents:
			r = self.players[o_id].respond_to_claim_opponent_has_card(
				player_id,
				card,
				self.state_visible_to_player(o_id),
				self.history
			)
			if r == NO_YOU_DONT_HAVE:
				p_st = self.player_states[player_id]
				if self.player_can_reveal_card(player_id, card):
					self.player_loses_life(o_id)
					return True
				else:
					return False
			elif r != OK:
				raise ValueError(r)
		return True
	
	def player_loses_life(self, player_id):
		p_st = self.player_states[player_id]
		if p_st.card1alive and p_st.card2alive:
			r = self.players[player_id].choose_which_card_to_lose(
				self.state_visible_to_player(player_id),
				self.history
			)
			if r == REVEAL_CARD_1:
				p_st = PlayerState(p_st.card1, p_st.card2, False, True, p_st.number_of_coins)
			elif r == REVEAL_CARD_2:
				p_st = PlayerState(p_st.card1, p_st.card2, True, False, p_st.number_of_coins)
			else:
				raise ValueError(r)
		else:
			p_st = PlayerState(p_st.card1, p_st.card2, False, False, p_st.number_of_coins)
			self.player_order.remove(player_id)
		self.player_states[player_id] = p_st
	
	def take_turn(self):
		p_id = self.player_order[0]
		
		p_st = self.state_visible_to_player(p_id)
		p_move = self.players[p_id].choose_move(p_st, self.history)
		
		if not self.move_valid(p_move):
			raise ValueError(p_move)
		
		self.update_state(p_move)
		
		#TODO: history
	
	def update_state(self, move):
		self.player_order.append(self.player_order.popleft())
		
		m_t = move.move_type
		
		if m_t == INCOME:
			self.do_income(move)
		elif m_t == FOREIGN_AID:
			self.do_foreign_aid(move)
		elif m_t == TAX:
			self.do_tax(move)
		elif m_t == SWAP:
			self.do_swap(move)
		elif m_t == STEAL:
			self.do_steal(move)
		elif m_t == ASSASSINATE:
			self.do_assassinate(move)
		elif m_t == COUP:
			self.do_coup(move)
		else:
			raise ValueError(m_t)
	
	def do_income(self, move):
		self.adjust_player_coins(move.player_id, 1)
	
	def do_foreign_aid(self, move):
		player = self.players[move.player_id]
		blocked = False
		for o_id in self.get_opponents(player.id):
			r = self.players[o_id].respond_to_foreign_aid(
				move,
				self.state_visible_to_player(o_id),
				self.history
			)
			if r != OK and self.player_successfully_claims_to_have_card(o_id, DUKE):
				blocked = True
				break
		if not blocked:
			self.adjust_player_coins(player.id, 2)
	
	def do_tax(self, move):
		if self.player_successfully_claims_to_have_card(move.player_id, DUKE):
			self.adjust_player_coins(move.player_id, 3)
	
	def do_swap(self, move):
		p_id = move.player_id
		if self.player_successfully_claims_to_have_card(p_id, AMBASSADOR):
			p_st = self.player_states[p_id]
			options = [self.draw_card(), self.draw_card()]
			number_of_cards = 0
			if p_st.card1alive:
				options.append(p_st.card1)
				number_of_cards += 1
			if p_st.card2alive:
				options.append(p_st.card2)
				number_of_cards += 1
			cards_kept = self.players[p_id].choose_which_cards_to_keep(
				tuple(options),
				number_of_cards,
				self.state_visible_to_player(p_id),
				self.history
			)
			if len(cards_kept) != number_of_cards:
				raise ValueError(cards_kept)
			for c in cards_kept:
				if c not in options:
					raise ValueError(c)
				options.remove(c)
			self.replace_cards(options)
			if number_of_cards == 2:
				self.player_states[p_id] = PlayerState(
					card1 = cards_kept[0],
					card2 = cards_kept[1],
					card1alive = True,
					card2alive = True,
					number_of_coins = p_st.number_of_coins
				)
			elif p_st.card1alive:
				self.player_states[p_id] = PlayerState(
					card1 = cards_kept[0],
					card2 = p_st.card2,
					card1alive = True,
					card2alive = False,
					number_of_coins = p_st.number_of_coins
				)
			else:
				self.player_states[p_id] = PlayerState(
					card1 = p_st.card1,
					card2 = cards_kept[0],
					card1alive = False,
					card2alive = True,
					number_of_coins = p_st.number_of_coins
				)
	
	def do_steal(self, move):
		p_id = move.player_id
		blocked = False
		for o_id in self.get_opponents(p_id):
			if o_id == move.target_player_id:
				r = self.players[o_id].respond_to_steal_from_me(
					move,
					self.state_visible_to_player(o_id),
					self.history
				)
				if r == NO_YOU_DONT_HAVE:
					if self.player_can_reveal_card(p_id, CAPTAIN):
						self.player_loses_life(o_id)
					else:
						blocked = True
					break
				elif r in [NO_I_HAVE_AMBASSADOR, NO_I_HAVE_CAPTAIN]:
					o_card = (AMBASSADOR if r == NO_I_HAVE_AMBASSADOR else CAPTAIN)
					if self.player_successfully_claims_to_have_card(o_id, o_card):
						blocked = True
					break
				elif r != OK:
					raise ValueError(r)
			elif not self.player_successfully_claims_to_have_card(p_id, CAPTAIN, [o_id]):
				blocked = True
				break
		if not blocked:
			self.adjust_player_coins(p_id, move.number_of_coins)
			self.adjust_player_coins(move.target_player_id, -move.number_of_coins)
	
	def do_assassinate(self, move):
		p_id = move.player_id
		self.adjust_player_coins(p_id, -3)
		blocked = False
		for o_id in self.get_opponents(p_id):
			if o_id == move.target_player_id:
				r = self.players[o_id].respond_to_assassinate_me(
					move,
					self.state_visible_to_player(o_id),
					self.history
				)
				if r == NO_YOU_DONT_HAVE:
					if self.player_can_reveal_card(p_id, ASSASSIN):
						self.player_loses_life(o_id)
					else:
						blocked = True
					break
				elif r == NO_I_HAVE_CONTESSA:
					if self.player_successfully_claims_to_have_card(o_id, CONTESSA):
						blocked = True
					break
				elif r != OK:
					raise ValueError(r)
			elif not self.player_successfully_claims_to_have_card(p_id, ASSASSIN, [o_id]):
				blocked = True
				break
		if not blocked:
			self.player_loses_life(move.target_player_id)
	
	def do_coup(self, move):
		self.adjust_player_coins(move.player_id, -7)
		self.player_loses_life(move.target_player_id)
	
	def is_over(self):
		return len(self.player_order) <= 1
	
	def play(self):
		while not self.is_over():
			self.take_turn()
