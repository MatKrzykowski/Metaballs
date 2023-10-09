"""Pygame_visualization.py

Visualization of my brownian motion script using Pygame library.
"""

# Libraries import
import sys
import pygame
import pygame.gfxdraw
from pygame.locals import QUIT

# Libraries imports
import numpy as np  # Import math modules

# Size of the window
WIDTH, HEIGHT = 800, 600

# Colors
PURPLE = (0, 128, 255)
RED = (255, 0, 0)

D = 10
N = 10

FONTSIZE = 18


class Particle():

    def __init__(self):
        self.x = np.random.random() * WIDTH
        self.y = np.random.random() * HEIGHT
        self.vx = (np.random.random() - 0.5) * 10
        self.vy = (np.random.random() - 0.5) * 10

    def timestep(self):
        self.x += self.vx
        self.y += self.vy
        if not 0 <= self.x <= WIDTH:
            self.vx *= -1
        if not 0 <= self.y <= HEIGHT:
            self.vy *= -1


def draw_FPS(screen, fontObj, textRectObj):
    textSurfaceObj = fontObj.render("FPS: " + str(round(fpsClock.get_fps(), 1)),
                                    True, (0, 0, 0))
    textRectObj.topright = (699, 0)
    screen.blit(textSurfaceObj, textRectObj)


if __name__ == "__main__":
    pygame.init()  # Initialize pygame

    FPS = 60  # Frames per second
    fpsClock = pygame.time.Clock()  # Clock initialization

    # Prepare the display
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Brownian motion')

    # Prepare print of the text
    fontObj = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    textSurfaceObj = fontObj.render('', True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()

    particles = [Particle() for _ in range(N)]

    n_x = WIDTH // D
    n_y = HEIGHT // D
    pos = np.zeros((n_x, n_y, 2))
    for i in range(n_x):
        for j in range(n_y):
            pos[i, j, 0] = i * D + D / 2
            pos[i, j, 1] = j * D + D / 2
    pos = pos.reshape(n_x, n_y, 1, 2)

    rect = np.zeros((n_x, n_y, 4))
    for i in range(n_x):
        for j in range(n_y):
            rect[i, j, 0] = i * D
            rect[i, j, 1] = j * D - 1
            rect[i, j, 2] = i * D + D
            rect[i, j, 3] = j * D + D + 1
    print(n_x, n_y, n_x * n_y)

    inv_hypot = np.zeros((n_x, n_y, N))

    # Draw the simulation
    while True:
        DISPLAYSURF.fill((255, 255, 255))  # Clear the surface

        test = pos - np.array([[p.x, p.y] for p in particles]).reshape(
            (1, 1, N, 2))
        inv_hypot = np.reciprocal(np.hypot(test[:, :, :, 0], test[:, :, :, 1]), out=inv_hypot)
        sum_inv_hypot = np.sum(inv_hypot, axis=2)

        for i in range(n_x):
            for j in range(n_y):
                r = int(min(255, sum_inv_hypot[i, j] * 5 * 255))
                color = pygame.Color((255 - r) * 256**2 + 255 * 256 + 255 - r)
                pygame.draw.rect(DISPLAYSURF, color, rect[i, j])

        draw_FPS(DISPLAYSURF, fontObj, textRectObj)  # Write the FPS text

        for particle in particles:
            particle.timestep()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)
