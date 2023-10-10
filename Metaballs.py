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

FONTSIZE = 18


def draw_FPS(screen, fontObj, textRectObj):
    textSurfaceObj = fontObj.render("FPS: " + str(round(fpsClock.get_fps(), 1)),
                                    True, (0, 0, 0))
    textRectObj.topright = (config.width - 101, 0)
    screen.blit(textSurfaceObj, textRectObj)


if __name__ == "__main__":
    pygame.init()  # Initialize pygame
    fpsClock = pygame.time.Clock()  # Clock initialization

    # Prepare the display
    DISPLAYSURF = pygame.display.set_mode((config.width, config.height), 0, 32)
    pygame.display.set_caption('Brownian motion')

    # Prepare print of the text
    fontObj = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    textSurfaceObj = fontObj.render('', True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()

    particles = gen_particles(config.n_particles)

    memory = init_memory(config.width, config.height, config.n_particles)

    # Draw the simulation
    while True:
        DISPLAYSURF.fill((255, 255, 255))  # Clear the surface

        memory.pos_part[:, :, :, :] = np.array([[p.x, p.y] for p in particles
                            ]).transpose().reshape(
                                (2, 1, 1, config.n_particles))

        np.subtract(memory.pos_grid, memory.pos_part, out=memory.dist_xy)
        np.reciprocal(
            np.hypot(memory.dist_xy[0], memory.dist_xy[1]), out=memory.inv_dist)
        np.sum(memory.inv_dist, axis=2, out=memory.hue_arr)
        np.multiply(config.particle_size, memory.hue_arr, out=memory.hue_arr)
        np.clip(memory.hue_arr, 0, 1, out=memory.hue_arr)

        lol = pygame.surfarray.pixels3d(DISPLAYSURF)
        lol[:, :, 0] = 255 - 128 * memory.hue_arr
        lol[:, :, 1] = 255 * (1 - memory.hue_arr)
        lol[:, :, 2] = 255 - 128 * memory.hue_arr
        del lol

        draw_FPS(DISPLAYSURF, fontObj, textRectObj)  # Write the FPS text

        for particle in particles:
            particle.timestep()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(config.fps)
