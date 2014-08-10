#/usr/bin/env python
import sys
import os
from engine.init import engine

sys.path.append(os.path.abspath("."))



if __name__ == "__main__" or __name__ == "main":
    engine.init_all()
    engine.loop()
