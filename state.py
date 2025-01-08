import numpy as np
from dataclasses import dataclass
from typing import List, Union

@dataclass
class State:
    self.x: np.ndarray
    self.x_dot: np.ndarray

    def update(self, dt):
        self.x += self.x_dot*dt

        