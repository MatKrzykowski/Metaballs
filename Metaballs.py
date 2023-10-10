"""Pygame_visualization.py

Visualization of my brownian motion script using Pygame library.
"""

import sys
import pygame
import pygame.gfxdraw

import numpy as np  # Import math modules

from config import default_config as config
from memory import init_memory
from particle import gen_particles
from renderer import Renderer


if __name__ == "__main__":
    pygame.init()  # Initialize pygame
    fpsClock = pygame.time.Clock()  # Clock initialization

    # Prepare the display
    pygame.display.set_caption('Metaballs')

    particles = gen_particles(config.n_particles)

    memory = init_memory(config.width, config.height, config.n_particles)
    renderer = Renderer(config.width, config.height, 18)

    # Draw the simulation
    while True:
        renderer.start_frame()

        memory.pos_part[:, :, :, :] = np.array([[p.x, p.y] for p in particles
                            ]).transpose().reshape(
                                (2, 1, 1, config.n_particles))

        np.subtract(memory.pos_grid, memory.pos_part, out=memory.dist_xy)
        np.reciprocal(
            np.hypot(memory.dist_xy[0], memory.dist_xy[1]), out=memory.inv_dist)
        np.sum(memory.inv_dist, axis=2, out=memory.hue_arr)
        np.multiply(config.particle_size, memory.hue_arr, out=memory.hue_arr)
        np.clip(memory.hue_arr, 0, 1, out=memory.hue_arr)

        for particle in particles:
            particle.timestep()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        fps = str(round(fpsClock.get_fps(), 1))
        renderer.draw_frame(memory.hue_arr, fps)
        pygame.display.update()
        fpsClock.tick(config.fps)
