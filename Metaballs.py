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

    pos = np.zeros((2, config.width, config.height))
    for i in range(config.width):
        for j in range(config.height):
            pos[0, i, j] = i
            pos[1, i, j] = j
    pos = pos.reshape((2, config.width, config.height, 1))
    test = np.zeros((2, config.width, config.height, config.n_particles))
    inv_hypot = np.zeros((config.width, config.height, config.n_particles))
    q = np.zeros((config.width, config.height))

    # Draw the simulation
    while True:
        DISPLAYSURF.fill((255, 255, 255))  # Clear the surface

        np.subtract(
            pos,
            np.array([[p.x, p.y] for p in particles]).transpose().reshape(
                (2, 1, 1, config.n_particles)),
            out=test)
        np.reciprocal(np.hypot(*test), out=inv_hypot)
        np.sum(inv_hypot, axis=2, out=q)
        np.multiply(config.particle_size * 255, q, out=q)
        np.clip(q, 0, 255, out=q)

        lol = pygame.surfarray.pixels3d(DISPLAYSURF)
        lol[:, :, 0] = 255
        lol[:, :, 1] = q
        lol[:, :, 2] = 255
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
