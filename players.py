import numpy as np

from board import Board
from board import ROTATION_MAP

class NoMovesPossibleException(Exception):
    pass

class Player():
    def __init__(self, game):
        self.game = game
        self.score = 0

    def turn(self) :
        self.possible_moves = self.game.possible_moves
        while True:
            if self.possible_moves == []:
                print("No possible move")
                raise NoMovesPossibleException("Pas de coup possible")
            input_player = self.make_choice_smarter()
            if input_player not in self.possible_moves:
                print("Sorry, your response must be {}".format(self.possible_moves))
                continue
            break

        score = self.game.do_move(input_player)
        self.score += score

    def make_choice(self):
        pass

class HumanPlayer(Player):

    def make_choice(self):
        input_player = input("your move : {} --> ".format(
            self.possible_moves
        ))
        return input_player


class IAPlayer(Player):
    
    def make_choice(self):
        return self.make_choice_random()

    def make_choice_random(self):
        print(self.possible_moves)
        input_player = np.random.choice(self.possible_moves)
        return input_player

    def make_choice_smarter(self):
        #test
        print(self.possible_moves)

        scores = []
        for move in self.possible_moves:
            new_board = Board()
            new_board.board = np.copy(self.game.board)
            scores.append(new_board.do_move(move))
        input_player = self.possible_moves[np.array(scores).argmax()]
        print("Choice: {}".format(input_player))
        return input_player