import os
main_dir = os.path.dirname(os.path.realpath(__file__))
from board import Board
import pygame as pg
import time

FAIL = '\033[91m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
ORANGE = '\033[33m'
ENDC = '\033[0m'

class Analyzer():
    def __init__ (self, gamefile, depth, pos):
        pg.init()
        self.screen = pg.display.set_mode((520, 520))
        pg.display.set_caption("Python Chess Analyzer")
        pg.display.set_icon(pg.image.load(main_dir+"/../Data/images/icon.png"))


        self.type = "fen"
        self.gamefile = gamefile
        self.depth = depth

        if self.gamefile[-4:] == ".pgn" or self.gamefile[-4:] == ".txt":
            self.type = "pgn"

        print("\n\nWelcome to Python Chess Analyzer")
        print("At each move, you will see two highlighted moves.")
        print("One of the moves is the one that has just been played, the second is the best one that could have been played.")

        print(FAIL+"Red"+ENDC+" means blunder.")
        print(ORANGE+"Orange"+ENDC+" means bad move.")
        print(OKGREEN+"Green"+ENDC+" means good move.")
        print(OKCYAN+"Blue"+ENDC+" means best move.")
        print("\n\n")
        
        self.run(pos)


    def run(self, pos):
        board = Board(self.screen, self.depth, pos)

        print("Starting the in-depth analysis.. (depth = {})".format(self.depth))
        start = time.time()

        if self.type == "pgn":
            w_e, w_bm, b_e, b_bm = board.analyzePGN(self.gamefile)
            print("White : "+FAIL+"{}".format(w_e) + " blunder(s) " + ENDC + ORANGE + "{}".format(w_bm) + " bad move(s)." + ENDC)
            print("Black : "+FAIL+"{}".format(b_e) + " blunder(s) " + ENDC + ORANGE + "{}".format(b_bm) + " bad move(s)." + ENDC)
            print("Done in {:.3f} seconds\n\n".format(time.time() - start))

        else:
            board.analyzeFEN(self.gamefile)

        running = True

        while running :
            board.drawBoard()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_q or event.key == pg.K_ESCAPE:
                        running = False
                        board.quitAI()

                    if event.key == pg.K_r:
                        board.rotateBoard()
                    
                    if event.key == pg.K_f:
                        board.printFen()
                    
                    if event.key == pg.K_LEFT:
                        board.removeMove()
                    if event.key == pg.K_RIGHT:
                        board.pushBackRemovedMove()

                    if event.key == pg.K_p:
                        board.printMoves()                    
        pg.quit()
