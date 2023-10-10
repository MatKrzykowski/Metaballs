"""memory.py"""

import numpy as np

class Memory():
    """Class storying reusable numpy arrays"""
    def __init__(self, width, height, n_particles):
        self.pos_grid = np.zeros((2, width, height))

        for i in range(width):
            for j in range(height):
                self.pos_grid[0, i, j] = i
                self.pos_grid[1, i, j] = j

        self.pos_grid = self.pos_grid.reshape((2, width, height, 1))
        self.dist_xy = np.zeros((2, width, height, n_particles))
        self.pos_part = np.zeros((2, width, height, n_particles))
        self.pos_grid = self.pos_grid + self.dist_xy
        self.inv_dist = np.zeros((width, height, n_particles))
        self.hue_arr = np.zeros((width, height))

def init_memory(width, height, n_particles):
    return Memory(width, height, n_particles)