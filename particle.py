"""particle.py"""

import numpy as np
from config import default_config as config


class Particle():

    def __init__(self):
        self.x = np.random.random() * config.width
        self.y = np.random.random() * config.height
        self.vx = (np.random.random() - 0.5) * config.av_speed
        self.vy = (np.random.random() - 0.5) * config.av_speed

    def timestep(self):
        self.x += self.vx
        self.y += self.vy
        if not 0 <= self.x <= config.width:
            self.vx *= -1
        if not 0 <= self.y <= config.height:
            self.vy *= -1

def gen_particles(n):
    return [Particle() for _ in range(config.n_particles)]
