"""renderer.py"""

import pygame

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

class Renderer():

    def __init__(self, width, height, fontsize):
        self.display_surf = pygame.display.set_mode((width, height), 0, 32)

        # Prepare print of the text
        self.fontObj = pygame.font.Font('freesansbold.ttf', fontsize)
        self.textSurfaceObj = self.fontObj.render('', True, (0, 0, 0))
        self.textRectObj = self.textSurfaceObj.get_rect()
        self.textRectObj.topright = (width - 101, 0)

        self.fps_topright = (width - 101, 0)

    def start_frame(self, color=WHITE):
        self.display_surf.fill(color)

    def draw_frame(self, hue_arr, fps):
        lol = pygame.surfarray.pixels3d(self.display_surf)
        lol[:, :, 0] = 255 - 128 * hue_arr
        lol[:, :, 1] = 255 * (1 - hue_arr)
        lol[:, :, 2] = 255 - 128 * hue_arr
        del lol

        self.draw_FPS(fps)

    def draw_FPS(self, fps):
        self.textSurfaceObj = self.fontObj.render("FPS: " + fps, True, BLACK)
        self.display_surf.blit(self.textSurfaceObj, self.textRectObj)