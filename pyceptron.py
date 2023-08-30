import numpy as np
from typing import List, Tuple


class Perceptron:
    def __init__(self, width, height) -> None:
        self.dims = (width, height)
        self.weights = np.random.rand(width, height)
        # self.weights = np.ones((width, height))

    def threshold(input: List[float]) -> List[float]:
        pass

    def train(training_set: List[Tuple]) -> None:
        pass
