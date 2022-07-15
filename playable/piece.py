class Piece:
    # States: Not clicked, clicked, flagged
    def __init__(self, has_bomb):
        self.has_bomb = has_bomb
        self.around = 0
        self.clicked = False
        self.flagged = False
        self.neighbors = []

    def __str__(self):
        return str(self.has_bomb)

    def get_num_around(self):
        return self.around

    def get_has_bomb(self):
        return self.has_bomb

    def get_clicked(self):
        return self.clicked

    def get_flagged(self):
        return self.flagged

    def toggle_flag(self):
        self.flagged = not self.flagged

    def handle_click(self):
        self.clicked = True

    def set_num_around(self):
        num = 0
        for neighbor in self.neighbors:
            if neighbor.get_has_bomb():
                num += 1
        self.around = num

    def set_neighbors(self, neighbors):
        self.neighbors = neighbors
        self.set_num_around()

    def get_neighbors(self):
        return self.neighbors
