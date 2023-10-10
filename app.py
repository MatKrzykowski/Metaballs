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

    def main(self):
        while True:
            self.renderer.start_frame()

            self.memory.pos_part[:, :, :, :] = np.array([[p.x, p.y] for p in self.particles
                                ]).transpose().reshape(
                                    (2, 1, 1, config.n_particles))

            np.subtract(self.memory.pos_grid, self.memory.pos_part, out=self.memory.dist_xy)
            np.reciprocal(
                np.hypot(self.memory.dist_xy[0], self.memory.dist_xy[1]), out=self.memory.inv_dist)
            np.sum(self.memory.inv_dist, axis=2, out=self.memory.hue_arr)
            np.multiply(config.particle_size, self.memory.hue_arr, out=self.memory.hue_arr)
            np.clip(self.memory.hue_arr, 0, 1, out=self.memory.hue_arr)

            for particle in self.particles:
                particle.timestep()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            fps = str(round(self.fpsClock.get_fps(), 1))
            self.renderer.draw_frame(self.memory.hue_arr, fps)
            pygame.display.update()
            self.fpsClock.tick(config.fps)
