import pygame
import os
from time import sleep
from board import Board

pygame.init()

SPEED = 100


class Game:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.frame_iteration = 0
        self.reset()
        self.images = {}
        self.piece_size = self.screen_size[0] // self.board.get_size()[1], self.screen_size[1] // self.board.get_size()[
            0]
        self.load_images()
        self.step_num = 0

    def reset(self):
        size = (5, 5)
        num_of_bombs = 5
        self.board = Board(size, num_of_bombs)
        self.frame_iteration = 0

    def play_step(self, action):
        step_reward = 0
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        clicked = False
        position = (action // 5, action % 5)
        right_click = False
        p = self.board.get_piece(position[0], position[1])
        clicked = p.get_clicked()
        self.handle_click(position, right_click)

        self.draw()
        pygame.display.flip()
        # 3. check if game over
        game_over = False
        if self.board.get_won():
            game_over = True
            step_reward = 1
            self.step_num += 1
            return game_over, step_reward
        if self.board.get_lost():
            game_over = True
            if self.step_num > 0:
                step_reward = -1
            self.step_num += 1
            return game_over, step_reward

        if self.step_num > 0:
            if clicked:
                step_reward = -0.1
            else:
                step_reward = 0.1

        self.step_num += 1
        self.draw()
        pygame.display.flip()
        self.clock.tick(SPEED)

        return game_over, step_reward

    def draw(self):
        top_left = (0, 0)
        for row in range(self.board.get_size()[0]):
            for col in range(self.board.get_size()[1]):
                piece = self.board.get_piece(row, col)
                image = self.get_image(piece)
                self.screen.blit(image, top_left)
                top_left = top_left[0] + self.piece_size[0], top_left[1]
            top_left = 0, top_left[1] + self.piece_size[1]

    def load_images(self):
        for file in os.listdir("images"):
            if not file.endswith('.png'):
                continue
            image = pygame.image.load(r"images/" + file)
            image = pygame.transform.scale(image, self.piece_size)
            self.images[file.split(".")[0]] = image

    def get_image(self, piece):
        string = None
        if piece.get_clicked():
            if piece.get_has_bomb():
                string = "bomb-at-clicked-block"
            else:
                string = str(piece.get_num_around())
        else:
            string = "flag" if piece.get_flagged() else "empty-block"

        return self.images[string]

    def handle_click(self, position, right_click):
        if self.board.get_lost():
            return
        piece = self.board.get_piece(position[1], position[0])
        self.board.handle_click(piece, right_click)
