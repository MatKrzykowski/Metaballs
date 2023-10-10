"""Pygame_visualization.py

Visualization of my brownian motion script using Pygame library.
"""

import sys
import pygame
import pygame.gfxdraw
from pygame.locals import QUIT

import numpy as np  # Import math modules

from config import default_config as config
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

    pos_grid = np.zeros((2, config.width, config.height))
    for i in range(config.width):
        for j in range(config.height):
            pos_grid[0, i, j] = i
            pos_grid[1, i, j] = j
    pos_grid = pos_grid.reshape((2, config.width, config.height, 1))
    dist_xy = np.zeros((2, config.width, config.height, config.n_particles))
    pos_part = np.zeros((2, config.width, config.height, config.n_particles))
    pos_grid = pos_grid + dist_xy
    inv_dist = np.zeros((config.width, config.height, config.n_particles))
    hue_arr = np.zeros((config.width, config.height))

    # Draw the simulation
    while True:
        DISPLAYSURF.fill((255, 255, 255))  # Clear the surface

        pos_part[:, :, :, :] = np.array([[p.x, p.y] for p in particles
                            ]).transpose().reshape(
                                (2, 1, 1, config.n_particles))

        np.subtract(pos_grid, pos_part, out=dist_xy)
        np.reciprocal(np.hypot(dist_xy[0], dist_xy[1]), out=inv_dist)
        np.sum(inv_dist, axis=2, out=hue_arr)
        np.multiply(config.particle_size, hue_arr, out=hue_arr)
        np.clip(hue_arr, 0, 1, out=hue_arr)

        lol = pygame.surfarray.pixels3d(DISPLAYSURF)
        lol[:, :, 0] = 255 - 128 * hue_arr
        lol[:, :, 1] = 255 * (1 - hue_arr)
        lol[:, :, 2] = 255 - 128 * hue_arr
        del lol

        draw_FPS(DISPLAYSURF, fontObj, textRectObj)  # Write the FPS text

        for particle in particles:
            particle.timestep()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(config.fps)
