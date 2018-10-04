import sys
import os

sys.path.append(os.path.realpath("Classes"))
sys.path.append(os.path.realpath("Modules"))

import Game

def main():
	game = Game.Game()
	quit()

main()
