from game import *
from textplayer import *
from randomplayer import RandomAI

if __name__ == '__main__':
	Game(
		TextPlayer(),
		RandomAI() 
	).play()
