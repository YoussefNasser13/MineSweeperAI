from game import Game
from board import Board

size = (12, 12)
num_of_bomb = 20
board = Board(size, num_of_bomb)
screen_size = (600, 600)

game = Game(board, screen_size)
game.run()

