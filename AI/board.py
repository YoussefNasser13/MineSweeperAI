from piece import Piece
from random import random


class Board:

    def __init__(self, size, num_of_bombs):
        self.size = size
        self.num_of_bombs = num_of_bombs
        self.board = []
        self.lost = False
        self.won = False
        self.num_clicked = 0
        self.num_non_bomb = size[0] * size[1] - num_of_bombs
        self.set_board()

    def set_board(self):
        bomb_prob = []
        vals = []
        for row in range(self.size[0]):
            row_list = []
            for col in range(self.size[1]):
                prob = random()
                row_list.append(prob)
                vals.append(prob)
            bomb_prob.append(row_list)
        vals.sort()
        num_has_bomb = 0
        for row in range(self.size[0]):
            row_list = []
            for col in range(self.size[1]):
                if num_has_bomb < self.num_of_bombs:
                    has_bomb = bomb_prob[row][col] >= vals[self.num_non_bomb]
                else:
                    has_bomb = False
                if has_bomb:
                    num_has_bomb += 1
                piece = Piece(has_bomb)
                row_list.append(piece)
            self.board.append(row_list)
        self.set_neighbors()

    def set_neighbors(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                piece = self.get_piece(row, col)
                neighbors = self.get_list_of_neighbors((row, col))
                piece.set_neighbors(neighbors)

    def get_list_of_neighbors(self, index):
        neighbors = []
        for row in range(index[0]-1, index[0]+2):
            for col in range(index[1]-1, index[1]+2):
                out_of_bounds = row < 0 or row >= self.size[0] or col < 0 or col >= self.size[1]
                same = row == index[0] and col == index[1]
                if same or out_of_bounds:
                    continue
                neighbors.append(self.get_piece(row, col))
        return neighbors

    def get_size(self):
        return self.size

    def get_piece(self, row, col):
        return self.board[row][col]

    def handle_click(self, piece, flag):
        if piece.get_clicked() or (not flag and piece.get_flagged()):
            return
        if flag:
            piece.toggle_flag()
            return
        piece.handle_click()
        if piece.get_has_bomb():
            self.lost = True
            return
        self.num_clicked += 1
        if piece.get_num_around() == 0:
            for neighbor in piece.get_neighbors():
                if not neighbor.get_has_bomb() and not neighbor.get_clicked():
                    self.handle_click(neighbor, False)

    def get_won(self):
        return self.num_clicked == self.num_non_bomb

    def get_lost(self):
        return self.lost
