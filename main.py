from os import system, get_terminal_size
from time import sleep
from random import randint


class Board:
    def __init__(self, width=None, height=None):
        self._board = []
        self.terminal_size = list(get_terminal_size())
        self.terminal_size[0] = self.terminal_size[0] // 2  # account for double-spacing
        if width is None:
            width = self.terminal_size[0]
        if height is None:
            height = self.terminal_size[1]
        self.width = width
        self.height = height
        self.alive = '\033[91m#\033[00m'
        self.dead = ' '
        self.living = set()
        for _ in range(height):
            self._board.append([self.dead] * width)

    def __repr__(self):
        string = ''
        for row in self._board:
            for column in row:
                if column == self.alive:
                    string += f'{column} '
                else:
                    string += f'{column} '
            string += '\n'
        return string

    def _is_valid(self, r, c):
        return self.height > r > -1 and self.width > c > -1

    def _is_valid_hard(self, r, c):
        if not self._is_valid(r, c):
            raise IndexError(f'[{r}, {c}] out of bounds within {self.height}, [{self.width}]')

    def set(self, r, c, value):
        # This really needs to get fixed
        self._is_valid_hard(r, c)
        self._board[r][c] = value

    def get(self, r, c):
        self._is_valid_hard(r, c)
        return self._board[r][c]

    def toggle(self, r, c):
        self._is_valid_hard(r, c)
        if self.get(r, c) == self.alive:
            self.set(r, c, self.dead)
            self.living.remove((r, c))
        else:
            self.set(r, c, self.alive)
            self.living.add((r, c))

    def get_neighbors(self, r, c):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not self._is_valid(r + i, c + j):
                    continue
                if i == 0 and j == 0:
                    continue
                neighbors.append([r + i, c + j])
        return neighbors

    def count_neighbors(self, r, c):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not self._is_valid(r + i, c + j):
                    continue
                if i == 0 and j == 0:
                    continue
                if self.get(r + i, c + j) == self.alive:
                    count += 1
        return count if count > 0 else 0

    def show_neighbors(self):
        for r, row in enumerate(self._board):
            for c, column in enumerate(row):
                if self.get(r, c) == self.alive:
                    print(f'\033[91m{self.count_neighbors(r, c)}\033[00m', end=" ")
                else:
                    print(self.count_neighbors(r, c), end=" ")
            print()

    def get_next_board(self):
        next_board = []

        for _ in range(self.height):
            next_board.append([self.dead] * self.width)

        new_living = set()
        for coord in self.living:
            neighbors = self.count_neighbors(coord[0], coord[1])
            if 1 < neighbors < 4:
                next_board[coord[0]][coord[1]] = self.alive
                new_living.add(tuple(coord))

            for neighbor in self.get_neighbors(coord[0], coord[1]):
                if self.get(neighbor[0], neighbor[1]) == self.dead:
                    if self.count_neighbors(neighbor[0], neighbor[1]) == 3:
                        next_board[neighbor[0]][neighbor[1]] = self.alive
                        new_living.add((neighbor[0], neighbor[1]))
        self.living = new_living
        return next_board

    def add_random(self):
        size = randint(8, 10)
        location = [randint(0, self.width - (size * 2)), randint(0, self.height - (size * 2))]

        for _ in range(randint(10, 20)):
            b.toggle(
                randint(location[1], location[1] + size),
                randint(location[0], location[0] + size)
            )

    def loop(self, debug=False, random=False):
        while True:
            system('clear')
            if debug:
                self.show_neighbors()
            else:
                print(self)
            # input()
            sleep(0.05)
            self._board = self.get_next_board()

    def add_acorn(self, row=None, column=None, relRow=None, relColumn=None):
        if relRow and relColumn:
            row = int(self.terminal_size[1] * relRow)
            column = int(self.terminal_size[0] * relColumn)
        self.toggle(1 + row, 2 + column)
        self.toggle(1 + row, 3 + column)
        self.toggle(3 + row, 3 + column)
        self.toggle(2 + row, 5 + column)
        self.toggle(1 + row, 6 + column)
        self.toggle(1 + row, 7 + column)
        self.toggle(1 + row, 8 + column)

    def add_glider(self, row=None, column=None, relRow=None, relColumn=None):
        if relRow and relColumn:
            row = int(self.terminal_size[1] * relRow)
            column = int(self.terminal_size[0] * relColumn)
        self.toggle(1 + row, 2 + column)
        self.toggle(3 + row, 1 + column)
        self.toggle(3 + row, 2 + column)
        self.toggle(3 + row, 3 + column)
        self.toggle(2 + row, 3 + column)

    def add_toggle(self, row=None, column=None, relRow=None, relColumn=None):
        if relRow and relColumn:
            row = int(self.terminal_size[1] * relRow)
            column = int(self.terminal_size[0] * relColumn)
        self.toggle(1 + row, 1 + column)
        self.toggle(1 + row, 2 + column)
        self.toggle(1 + row, 3 + column)


if __name__ == '__main__':
    # default font size
    b = Board()
    # b.add_acorn(39, 44)
    b.add_acorn(relColumn=0.7, relRow=0.5)

    # # font size: 10
    # b = Board(178, 98)
    # b.add_acorn(40, 100)
    b.loop()
