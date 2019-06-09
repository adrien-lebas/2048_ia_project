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
            input_player = self.make_choice()
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
        input_player = raw_input("your move : {} --> ".format(
            self.possible_moves
        ))
        return input_player


class IAPlayer(Player):
    
    def make_choice(self):
        return self.make_choice_smarter()

    def make_choice_random(self):
        print(self.possible_moves)
        input_player = np.random.choice(self.possible_moves)
        print("Choice: {}".format(input_player))
        return input_player

    def make_choice_smarter(self):
        print(self.possible_moves)
        input_player, _ = self.get_next_next_best_move()
        print("Choice: {}".format(input_player))
        return input_player

    def get_next_best_move(self):
        scores = []
        for move in self.possible_moves:
            score = self.get_next_score(move)
            scores.append(score)
        best_move = self.possible_moves[np.array(scores).argmax()]
        best_score = np.max(score)
        return best_move, best_score

    def get_next_score(self, move):
            new_board = Board()
            new_board.board = np.copy(self.game.board)
            score = new_board.do_move(move)
            return score

    def get_next_next_best_move(self):
        scores = []
        for move in self.possible_moves:
            score = self.get_next_next_score(move)
            scores.append(score)
        best_move = self.possible_moves[np.array(scores).argmax()]
        best_score = np.max(scores)
        return best_move, best_score


    def get_next_next_score(self, move):
            new_board = Board()
            new_board.board = np.copy(self.game.board)
            first_score = new_board.do_move(move)

            scores = []
            for cell in np.argwhere(new_board.board == 0):
                new_board.board[cell] = 2
                _, best_score_2 = self.get_next_best_move()
                scores.append(best_score_2)
                new_board.board[cell] = 4
                _, best_score_4 = self.get_next_best_move()
                scores.append(best_score_4)
                new_board.board[cell] = 0

            return np.max(scores)
