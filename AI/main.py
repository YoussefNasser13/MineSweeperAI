from game import Game
from board import Board

size = (12, 12)
prob = 0.1
board = Board(size, prob)
screen_size = (600, 600)

game = Game(board, screen_size)
game.run()
