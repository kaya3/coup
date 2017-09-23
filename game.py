from defs import *
from random import shuffle
from collections import deque

class Game:
	def __init__(self, players):
		self.players = { p.id: p for p in players }
		
		self.deck = [ AMBASSADOR, CAPTAIN, CONTESSA, DUKE, ASSASSIN ]*3
		self.shuffle()
		
		self.player_states = {
			p.id: PlayerState(draw_card(), draw_card(), true, true, 2)
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
		p_o = self.player_order
		i = p_o.index(player_id)
		return p_o[i+1:] + p_o[:i]
	
	def take_turn(self):
		p_id = self.player_order[0]
		
		p_st = self.state_visible_to_player(p_id)
		p_move = self.players[p_id].choose_move(p_st, self.history)
		
		if not self.move_valid_in_state(p_move, p_st):
			raise ValueError()
		
		self.update_state(p_move)
		
		#TODO: history
	
	def get_response(self, o_id, move, options):
		r = self.players[o_id].respond_to_move(
			self.state_visible_to_player(o_id),
			move,
			options,
			self.history
		)
		if r not in options:
			raise ValueError()
		return r
	
	def get_response_to_response
	
	def everyone_accepts_player_has(self, player_id, card):
		for o_id in self.get_opponents(player_id):
			r = 
	
	def update_state(self, move):
		player_states = dict(self.player_states)
		opponents = list(self.player_order[1:])
		p = self.players[move.player_id]
		
		if move.move_type == INCOME:
			s = player_states[p.id]
			s = PlayerState(s.card1, s.card2, s.card1alive, s.card2alive, s.number_of_coins+1)
			player_states[p.id] = s
		elif move.move_type == FOREIGN_AID:
			options = (OK, NO_I_HAVE_DUKE)
			blocked = False
			for o_id in opponents:
				r = get_response(o_id, game_state, move, options)
				if r != OK:
					if self.everyone_accepts_player_has(o_id, DUKE):
						blocked = True
						break
						
					
				
			
		player_order = opponents + [move.player_id]
		for p_id, p_st in player_states.items():
			if not p_st.card1alive and not p_st.card2alive:
				player_order.remove(p_id)
		player_order = tuple(opponents)
		
		self.current_state = GameState(player_states, player_order)
	
	def is_over(self):
		return len(self.player_queue) <= 1
	
	def play(self):
		while not self.is_over():
			self.take_turn()
