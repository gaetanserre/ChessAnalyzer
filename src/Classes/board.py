import pygame as pg
import chess.engine as ce
import chess.pgn
import os
import sys
from ai import AI

main_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

dir_data = main_dir+'/Data/'
dir_images = dir_data+'images/'
dir_sounds = dir_data+'sounds/'

OFFSET = 20
SIZE = 60

class Board ():
    def __init__  (self, screen, depth, pos):
        self.screen = screen

        self.B_KING = pg.image.load(dir_images+'BlackKing.png')
        self.W_KING = pg.image.load(dir_images+'WhiteKing.png')

        self.B_QUEEN = pg.image.load(dir_images+'BlackQueen.png')
        self.W_QUEEN = pg.image.load(dir_images+'WhiteQueen.png')

        self.B_ROOK = pg.image.load(dir_images+'BlackRook.png')
        self.W_ROOK = pg.image.load(dir_images+'WhiteRook.png')

        self.B_BISHOP = pg.image.load(dir_images+'BlackBishop.png')
        self.W_BISHOP = pg.image.load(dir_images+'WhiteBishop.png')

        self.B_KNIGHT = pg.image.load(dir_images+'BlackKnight.png')
        self.W_KNIGHT = pg.image.load(dir_images+'WhiteKnight.png')

        self.B_PAWN = pg.image.load(dir_images+'BlackPawn.png')
        self.W_PAWN = pg.image.load(dir_images+'WhitePawn.png')

        self.boardW = pg.image.load(dir_images+'BoardW.png')
        self.boardB = pg.image.load(dir_images+'BoardB.png')

        self.move_sound = pg.mixer.Sound(dir_sounds+"move.wav")
        self.finished_analyze = pg.mixer.Sound(dir_sounds+"success.wav")

        self.actualBoard = pos
        self.algo_board = ce.chess.Board()
        self.board = []
        self.FenToBoard()

        self.moves = []
        self.removed_moves = []
        self.analyze = False
        self.IA = AI(depth)





    def FenToBoard (self):
        fen = self.algo_board.fen()
        self.board = []
        fen = fen.split()[0].split('/')
        for rangee in fen:
            for piece in rangee:
                if piece == 'r':
                    self.board.append(self.B_ROOK)
                elif piece == 'R':
                    self.board.append(self.W_ROOK)
                
                elif piece == 'n':
                    self.board.append(self.B_KNIGHT)
                elif piece == 'N':
                    self.board.append(self.W_KNIGHT)

                elif piece == 'b':
                    self.board.append(self.B_BISHOP)
                elif piece == 'B':
                    self.board.append(self.W_BISHOP)

                elif piece == 'q':
                    self.board.append(self.B_QUEEN)
                elif piece == 'Q':
                    self.board.append(self.W_QUEEN)

                elif piece == 'k':
                    self.board.append(self.B_KING)
                elif piece == 'K':
                    self.board.append(self.W_KING)
                
                elif piece == 'p':
                    self.board.append(self.B_PAWN)
                elif piece == 'P':
                    self.board.append(self.W_PAWN)

                elif int(piece) >= 1 and int(piece) <= 8:
                    piece = int(piece)
                    for i in range(0, piece):
                        self.board.append(None)

        if self.actualBoard == "black":
            self.board.reverse()

    
    def drawMove (self, move, color="B"):

        BLUE = (0, 255, 255, 100)
        GREEN = (0, 255, 0, 100)
        RED = (255, 0, 0, 100)
        ORANGE = (255, 165, 0)
            

        def convertAlgToCase(case, reverse=False):
            letters = 'abcdefgh'
            numbers = '87654321'
            convert = [-1,-1]
            for i in range(0, len(letters)):
                if case[0] == letters[i]:
                    convert[0] = i
                if case[1] == numbers[i]:
                    convert[1] = i
            if reverse:
                return (7 - convert[0], 7 - convert[1])
            return (convert[0], convert[1])

        if move != "None":

            case1 = convertAlgToCase(move[0:2], reverse=self.actualBoard == "black")
            case2 = convertAlgToCase(move[2:4], reverse=self.actualBoard == "black")

            case = pg.Surface((SIZE, SIZE), pg.SRCALPHA)
                
            if color == "G":
                case.fill(GREEN)
            elif color == "E":
                case.fill(RED)
            elif color == "P":
                case.fill(ORANGE)
            else:
                case.fill(BLUE)

            self.screen.blit(case, (case1[0] * SIZE + OFFSET, case1[1] * SIZE + OFFSET))
            self.screen.blit(case, (case2[0] * SIZE + OFFSET, case2[1] * SIZE + OFFSET))




    def drawBoard (self):
        self.screen.fill((255, 255, 255))

        if self.actualBoard == "white":              # Draw Broad then highligthed cases then pieces
            self.screen.blit(self.boardW, (0, 0))
        else:
            self.screen.blit(self.boardB, (0, 0))

        for i in range(OFFSET, SIZE*8 + OFFSET, SIZE):
            if ((i-OFFSET) / SIZE)%2 == 0:
                value = SIZE + OFFSET
            else:
                value = OFFSET
            for j in range(value, SIZE*8 + OFFSET, 2 * SIZE):
                pg.draw.rect(self.screen, (181, 136, 99), (j, i, SIZE, SIZE))

        if len(self.moves) > 0 and not self.analyze:
            actual_move, best_move, state = self.moves[-1]
            self.drawMove(actual_move, state)
            self.drawMove(best_move)


        (x, y) = (OFFSET, OFFSET)
        for i in range(0, len(self.board)):
            if self.board[i] != None:
                self.screen.blit(self.board[i], (x,y))

            x += SIZE
            if (i+1)%8 == 0:
                x = OFFSET
                y += SIZE

        
        pg.display.update()


    def rotateBoard (self):
        if self.actualBoard == "white" :
            self.actualBoard = "black"
            self.board.reverse()
        else:
            self.actualBoard = "white"
            self.board.reverse()

    
    def makeMove (self, move, sound=True):
        move = ce.chess.Move.from_uci(move)
        if move in self.algo_board.legal_moves:
            self.algo_board.push(move)
            self.FenToBoard()
            if sound:
                self.move_sound.play()
            return True
        return False

    def removeMove (self):
        try:
            self.algo_board.pop()
            move = self.moves.pop()
            self.removed_moves.append(move)
            self.FenToBoard()
            self.move_sound.play()
        except:
            pass
    
    def pushBackRemovedMove (self):
        try:
            move, x, y  = self.removed_moves.pop()
            self.makeMove(move)
            self.moves.append((move, x, y))
        except:
            pass

    def analyzePGN (self, path):
        self.analyze = True
        self.drawBoard()
        pgn = open(path, 'r')

        game = chess.pgn.read_game(pgn)
        pgn.close()

        w_bm, w_e, b_bm, b_e, count = (0, 0, 0, 0, 0)


        for move in game.mainline_moves():
            move, best, state = self.IA.compareMove(str(move), self.algo_board)
            if count % 2 == 0:
                if state == 'E':
                    w_e += 1
                elif state == 'P':
                    w_bm += 1
            else:
                if state == 'E':
                    b_e += 1
                elif state == 'P':
                    b_bm += 1
            count += 1

            self.moves.append((move, best, state))

            self.makeMove(str(move), sound=False)
            self.drawBoard()
            
        self.analyze = False
        self.finished_analyze.play()

        return (w_e, w_bm, b_e, b_bm)



    def analyzeFEN (self, fen):
        self.analyze = True
        try:
            self.algo_board = ce.chess.Board(fen)
            self.FenToBoard()
            self.drawBoard()

            best_move = self.IA.getBestMove(self.algo_board)

            self.moves.append((best_move, best_move, "B"))
            self.analyze = False
            self.finished_analyze.play()

        except:
            print("[ERROR] invalid FEN")
            self.quitAI()
            pg.quit()
            sys.exit()


    def printFen(self):
        print(self.algo_board.fen()+'\n')


    def printMoves(self):
        try:
            actual_move, best_move, d = self.moves[-1]
            self.algo_board.pop()

            actual_score = self.IA.getScore(ce.chess.Move.from_uci(actual_move), self.algo_board)
            best_score = self.IA.getScore(ce.chess.Move.from_uci(best_move), self.algo_board)

            actual_move = self.algo_board.san(ce.chess.Move.from_uci(actual_move))
            best_move = self.algo_board.san(ce.chess.Move.from_uci(best_move))


            print("Score for move {} : {}".format(actual_move, actual_score))
            print("Score for best move {} : {}\n".format(best_move, best_score))

            self.makeMove(actual_move, sound=False)
            
        except:
            pass


    def quitAI(self):
        self.IA.quit()