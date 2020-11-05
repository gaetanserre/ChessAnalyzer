import os
main_dir = os.path.dirname(os.path.realpath(__file__))
from sys import path; path.append(main_dir+'/Classes')
import sys

DEPTH = 18

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("[ERROR]\nWrong arguments : Usage python3 ChessAnalyzer.py gamefile [depth]")
        sys.exit()

    if len(sys.argv) == 3:
        DEPTH = int(sys.argv[2])

    from analyzer import Analyzer
    analyzer = Analyzer(sys.argv[1], DEPTH)
