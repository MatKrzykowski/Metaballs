"""app.py"""

import numpy as np  # Import math modules
import pygame

from config import default_config as config
from memory import init_memory
from particle import gen_particles
from renderer import Renderer

class App():
    def __init__(self):
        self.fpsClock = pygame.time.Clock()
        self.particles = gen_particles(config.n_particles)
        self.memory = init_memory(config.width, config.height, config.n_particles)
        self.renderer = Renderer(config.width, config.height, 18)
        self.hue_arr = self.memory.hue_arr

    def main(self):
        while True:
            self.renderer.start_frame()

            hue_arr = self.calculate_hue_arr()

            for particle in self.particles:
                particle.timestep()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            fps = str(round(self.fpsClock.get_fps(), 1))
            self.renderer.draw_frame(hue_arr, fps)
            pygame.display.update()
            self.fpsClock.tick(config.fps)

    def calculate_hue_arr(self):
        pos_part_list = [[part.x, part.y] for part in self.particles]
        self.memory.pos_part[:, :, :, :] = np.array(
                pos_part_list
                ).transpose(
                ).reshape((2, 1, 1, config.n_particles))
        np.subtract(
            self.memory.pos_grid,
            self.memory.pos_part,
            out=self.memory.dist_xy)
        np.hypot(
            self.memory.dist_xy[0],
            self.memory.dist_xy[1],
            out=self.memory.inv_dist)
        np.reciprocal(
            self.memory.inv_dist,
            out=self.memory.inv_dist)
        np.sum(
            self.memory.inv_dist,
            axis=2,
            out=self.hue_arr)
        np.multiply(
            config.particle_size,
            self.hue_arr,
            out=self.hue_arr)
        np.clip(
            self.hue_arr,
            0, 1,
            out=self.hue_arr)
        return self.hue_arr
