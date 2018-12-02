import numpy
import random
import matplotlib.pyplot as plt
from source.matplotlib_player import Player

import sys
from PyQt5.QtWidgets import QMessageBox, QApplication


class Cell:
    def __init__(self):
        self.state = 0


class GameOfLife:
    def __init__(self, turns=10, dimensions=(16, 16),
                 first_seed=None, second_seed=None,
                 show_plot=True, forward=True, speed=5):

        plt.rcParams['toolbar'] = 'None'

        self.dim_x = dimensions[0]
        self.dim_y = dimensions[1]
        self.old_board = numpy.zeros((self.dim_x, self.dim_y), dtype='int')

        state = self.state_from_file(second_seed)
        reversed_state = []
        for line in reversed(state):
            reversed_state.append(list(reversed(line)))
        state = self.state_from_file(first_seed)

        for i in range(0, 4):
            for j in range(0, 4):
                self.old_board[i+2][j+2] = state[i][j]
                self.old_board[i+2+8][j+2+8] = -reversed_state[i][j]

        for i in range(0, 4):
            for j in range(0, 4):
                self.old_board[i+2+8][j+2+8] = -reversed_state[i][j]

        self.new_board = self.old_board.copy()
        self.mat = None
        self.fig = None
        self.ax = None

        self.turns = turns
        self.speed = speed
        self.winner = 0
        self.game_resolved = False

        self.gen = 0

        self.prev_states = []
        self.prev_states.append(self.new_board.copy())
        self.forward = forward

        self.show_plot = show_plot

    def init_random_state(self):
        for i in range(0, self.dim_y):
            for j in range(0, self.dim_x):
                rand_state = random.randint(0, 100)
                if rand_state < 15:
                    self.old_board[i][j] = 1
                elif rand_state < 30:
                    self.old_board[i][j] = -1
                else:
                    self.old_board[i][j] = 0

    def state_from_file(self, filename):
        board_state = []
        with open(filename, 'r') as f:
            state = f.read()
            state = state.split('\n')
            prev_line_len = len(state[0])
            i = 0
            for line in state:
                if len(line) != prev_line_len:
                    raise RuntimeError('Lines not of same length')
                prev_line_len = len(line)
                board_state.append([])
                for char in line:
                    if char == '.':
                        board_state[i].append(0)
                    else:
                        board_state[i].append(1)
                i += 1
        return board_state

    def neighbours_state(self, i, j):
        count = 0
        red_count = 0
        blue_count = 0
        for y in [i-1, i, i+1]:
            for x in [j-1, j, j+1]:
                if x == j and y == i:
                    continue
                if x != self.dim_x and y != self.dim_y:
                    cell = self.old_board[y][x]
                elif x == self.dim_x and y != self.dim_y:
                    cell = self.old_board[y][0]
                elif x != self.dim_x and y == self.dim_y:
                    cell = self.old_board[0][x]
                else:
                    cell = self.old_board[0][0]

                if cell == -1:
                    count += 1
                    blue_count += 1
                elif cell == 1:
                    count += 1
                    red_count += 1
                pass

        return count, red_count, blue_count

    def new_board_state(self):
        for i in range(0, self.dim_y):
            for j in range(0, self.dim_x):
                count, red_count, blue_count = self.neighbours_state(i, j)
                if self.old_board[i][j]:
                    if count < 2:
                        is_alive = False
                    elif count > 3:
                        is_alive = False
                    else:
                        is_alive = True
                else:
                    if count == 3:
                        is_alive = True
                    else:
                        is_alive = False

                if is_alive and red_count > blue_count:
                    self.new_board[i][j] = 1
                elif is_alive and blue_count > red_count:
                    self.new_board[i][j] = -1
                elif is_alive:
                    self.new_board[i][j] = self.old_board[i][j]
                else:
                    self.new_board[i][j] = 0

    def update(self, gen):
        if gen == 0:
            gen = 1
        try:
            self.new_board = self.prev_states[gen]
            self.gen = gen
        except IndexError:
            if gen > self.gen:
                if self.gen > 0:
                    self.new_board_state()
                self.prev_states.append(self.new_board.copy())
                self.gen = gen
            elif gen == self.gen or gen == self.gen - 1:
                if self.gen > 0:
                    self.new_board_state()
                self.prev_states.append(self.new_board.copy())
                # self.gen = gen
            elif self.gen == 0:
                self.prev_states.append(self.new_board.copy())
            else:
                raise RuntimeError('Problem with generations! '
                                   'self={}, gen={}'.format(self.gen, gen))
        self.mat.set_data(self.new_board)
        unique, counts = numpy.unique(self.new_board, return_counts=True)
        cells = dict(zip(unique, counts))
        try:
            self.red = cells[1]
        except KeyError:
            self.red = 0
        try:
            self.blue = cells[-1]
        except KeyError:
            self.blue = 0

        self.ax.set_title('Gen: {}      '
                          'Red: {}      '
                          'Blue: {}'.format(self.gen, self.red, self.blue))
        self.old_board = self.new_board.copy()

        return [self.mat]

    def play(self):
        plt.style.use('classic')
        self.fig, self.ax = plt.subplots()
        self.mat = self.ax.matshow(self.old_board)
        cbaxes = self.fig.add_axes([0.4, 0.6, 0.4, 0.6])
        cbar = plt.colorbar(self.mat, cax=cbaxes)
        cbar.set_clim(vmin=-1, vmax=1)
        self.fig.delaxes(self.fig.axes[1])
        ani = Player(self.fig, self.update, max=self.turns+1,
                     interval=int(250/self.speed), save_count=self.turns+1)
        if self.show_plot:
            plt.show()
        else:
            ani.save('animation.gif', writer='imagemagick', fps=12)


if __name__ == '__main__':
    import time

    start_time = time.time()
    game = GameOfLife(32,
                      first_seed='../seeds/second.txt',
                      second_seed='../seeds/first.txt',
                      forward=True, speed=9)
    game.play()
    # print('----', round(time.time() - start_time, 6), '----')
