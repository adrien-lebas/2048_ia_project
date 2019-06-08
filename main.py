from board import Board
from players import HumanPlayer
from players import IAPlayer
from players import NoMovesPossibleException

def game():
    game = Board()
    human_player = HumanPlayer(game)
    ia_player = IAPlayer(game)

    player = ia_player

    turn_number = 0
    while True :
        try :
            print("Board:")
            print(game.board)
            print("Score: {}".format(player.score))
            print("Turn: {}".format(turn_number))

            player.turn()
            game.add_number_in_board()
            turn_number += 1

        except NoMovesPossibleException as e:
            print("Sorry, you lose")
            print("Nb of turn : {}".format(turn_number))
            print("Final Score : {}".format(player.score))
            break
            
if __name__ == "__main__":
    game()