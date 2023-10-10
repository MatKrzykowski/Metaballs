"""config.py"""

from dataclasses import dataclass


@dataclass()
class Config():
    """Config class to store apllication data"""
    width: int
    height: int
    n_particles: int
    av_speed: float
    particle_size: int
    fps: int


default_config = Config(
    400,  # window width
    400,  # window height
    20,  # number of particles
    20,  # average particle speed
    5,  # Particle size
    60,  # goal FPS count
)