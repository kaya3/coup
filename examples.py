# examples
from defs import *

# PlayerState
player1_state = PlayerState(
	DUKE, CAPTAIN, True, False, 4
)

player2_state = PlayerState(
	ASSASSIN, ASSASSIN, False, False, 0
)

# or
player3_state = PlayerState(
	card1 = AMBASSADOR,
	card2 = CONTESSA,
	card1alive = True,
	card2alive = True,
	number_of_coins = 6
)


# GameState
game_state = GameState(
	player_states = {
		1: player1_state,
		2: player2_state,
		3: player3_state,
	},
	player_order = (1, 3) # player 2 is out of the game
)


# Move

player1_claims_tax = Move(1, TAX)

player3_assassinates_player1 = Move(3, ASSASSINATE, 1)

player1_steals_two_coins_from_player3 = Move(1, STEAL, 3, 2)
