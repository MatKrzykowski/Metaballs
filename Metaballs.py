# Pygame_visualization.py
#
# Visualization of my brownian motion script using Pygame library.
#
# Changelog:
# 03.11.2016 - original script from "Brownian motion" project
# 03.11.2018 - script for metaballs created


# Libraries import
import pygame
import sys
import pygame.gfxdraw
from pygame.locals import QUIT

# Libraries imports
import numpy as np  # Import math modules

# Size of the window
WIDTH, HEIGHT = 800, 600

# Colors
PURPLE = (0, 128, 255)
RED = (255, 0, 0)


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


def draw_FPS(screen):
    textSurfaceObj = fontObj.render("FPS: "
                                    + str(round(fpsClock.get_fps(), 1)),
                                    True, (0, 0, 0))
    textRectObj.topright = (699, 0)
    screen.blit(textSurfaceObj, textRectObj)


if __name__ == "__main__":
    pygame.init()  # Initialize pygame

    FPS = 60  # Frames per second
    fpsClock = pygame.time.Clock()  # Clock initialization

    fontsize = 18

    # Prepare the display
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Brownian motion')

    # Prepare print of the text
    fontObj = pygame.font.Font('freesansbold.ttf', fontsize)
    textSurfaceObj = fontObj.render('', True, (0, 0, 0))
    textRectObj = textSurfaceObj.get_rect()

    n = 10
    particles = [Particle() for i in range(n)]

    # Draw the simulation
    while True:
        DISPLAYSURF.fill((255, 255, 255))  # Clear the surface

        d = 10

        for i in range(0, WIDTH, d):
            for j in range(0, HEIGHT, d):
                x = i + d / 2
                y = j + d / 2
                r = sum([1 / ((particles[i].x - x)**2 +
                              (particles[i].y - y)**2)**0.5 * 5
                         for i in range(n)])
                color = (255 - min(255, 255 * r), 255, 255 - min(255, 255 * r))
                pygame.draw.rect(DISPLAYSURF, color,
                                 (i, j, i + d, j + d))

        draw_FPS(DISPLAYSURF)  # Write the FPS text

        for i in range(n):
            particles[i].timestep()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        fpsClock.tick(FPS)
