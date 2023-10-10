"""config.py"""

from dataclasses import dataclass


@dataclass()
class Config():
    width: int
    height: int
    n_particles: int

default_config = Config(
    400,  # window width
    400,  # window height
    20,  # number of particles
)