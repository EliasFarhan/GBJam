#kudu start program
import engine.loop as game
import sys
if sys.platform != 'darwin':
	import pygame._view
import os
sys.path.append(os.path.abspath("."))

if __name__ == "__main__":
	game.start()
