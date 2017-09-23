from game import *
from textplayer import *
from aiplayer import AIPlayer

if __name__ == '__main__':
	Game(
		TextPlayer(),
       AIPlayer() 
	).play()
