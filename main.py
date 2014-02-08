#kudu start program
import sys
import os
from engine.const import pookoo
if pookoo:
	sys.path.append(os.path.abspath("../script"))
else:
	sys.path.append(os.path.abspath("."))
import engine.loop as game



if __name__ == "__main__":
	game.start()
