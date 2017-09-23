# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 18:15:24 2017

@author: james
"""

from defs import *
from random import choice

class AIPlayer(Player):
    
   def choose_move(self, game_state, history):		

       NONTARGETMOVES = [INCOME, FOREIGN_AID, SWAP]
       TARGETMOVES = [TAX, STEAL, ASSASSINATE, COUP]  
    #Coup players with a single card
       if game_state.player_states[self.id].number_of_coins > 6:    
    
        player_card_count = {
            p_id: int(player.card1alive)+int(player.card2alive)
            for p_id, player in game_state.player_states.items()
        }
            
        for player, card in player_card_count.items():
            if card == 1:
                return Move(self.id, COUP, player, 7)
                break 

    #Never choose tax if 3 dukes on the table
       counter = 0  
       for player in game_state.player_states:
           if not player.card1alive and player.card1 == 'DUKE':
               counter += 1
           if not player.card2alive and player.card2 == 'DUKE':
               counter += 1
    
       if counter == 3:
           TARGETMOVES.remove(TAX)

    
    
       moveset = choice([NONTARGETMOVES, TARGETMOVES])
    
       if moveset == NONTARGETMOVES:
           return Move(self.id, choice(moveset))
       else:
           move = choice(moveset)
        
           if move == STEAL:
               return Move(self.id, move, target_player_id, choice([1,2]))
        
       return Move(self.id, move, target_player_id)

	
    
    
   def respond_to_move(self, game_state, move, options, history):
        self.show_game_state(game_state)
        self.show_move(game_state, move)
		
        initial_responses =[OK, NO]
        initial = choice(initial_responses)
        
        if initial == OK:
            return OK
        
        if choice([0,1]):
            return NO_YOU_DONT_HAVE
        
        blockers = {FOREIGN_AID:[NO_I_HAVE_DUKE], 
                    STEAL:[NO_I_HAVE_CAPTAIN, NO_I_HAVE_AMBASSADOR],
                    ASSASSINATE: [CONTESSA]}
        
        if move.target_player_id == self.id:
            return choice(blockers[move.move_type])
        
        reveals = {FOREIGN_AID:[REVEAL_DUKE],
                   STEAL:[REVEAL_CAPTAIN, REVEAL_AMBASSADOR],
                   ASSASINATE: REVEAL_ASSASSIN}
		
        return choice(reveals[move.move_type])
