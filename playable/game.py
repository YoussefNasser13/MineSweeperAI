import pygame
import os
from time import sleep




class Game:
    def __init__(self, board, screen_size):
        self.board = board               # Observation - State
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.images = {}
        self.piece_size = self.screen_size[0] // self.board.get_size()[1], self.screen_size[1] // self.board.get_size()[0]
        self.load_images()

    def run(self):
        pygame.init()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:             # Action
                    position = pygame.mouse.get_pos()
                    right_click = pygame.mouse.get_pressed()[2]
                    self.handle_click(position, right_click)
            self.draw()
            pygame.display.flip()
            if self.board.get_won():
                image = pygame.image.load(r'images/winwin.png')
                image = pygame.transform.scale(image, self.screen_size)
                self.screen.blit(image, (0, 0))
                pygame.display.update()
                sleep(3)
                running = False
            if self.board.get_lost():
                image = pygame.image.load(r'images/lose.png')
                image = pygame.transform.scale(image, self.screen_size)
                self.screen.blit(image, (0, 0))
                pygame.display.update()
                sleep(3)
                running = False
        pygame.quit()

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
        index = position[1] // self.piece_size[1], position[0] // self.piece_size[0]
        piece = self.board.get_piece(index[0], index[1])
        self.board.handle_click(piece, right_click)
