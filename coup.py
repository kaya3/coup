from game import *
from textplayer import *

if __name__ == '__main__':
	Game(
		TextPlayer(),
		TextPlayer()
	).play()
