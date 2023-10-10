"""Pygame_visualization.py

Visualization of my brownian motion script using Pygame library.
"""

import pygame

from app import App

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption('Metaballs')
    App().main()
    pygame.quit()
