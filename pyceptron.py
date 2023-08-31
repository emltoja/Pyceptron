import numpy as np
from typing import List, Tuple


class Perceptron:
    def __init__(
        self,
        width,
        height,
        trainingSet,
        bias=0,
        learningRate=0.1,
        trainingThreshold=0.1,
    ) -> None:
        self.dims = (width, height)                         # Dimension of percepted specimens (as well as dimension of weights matrix)
        self.bias = bias                                    # Bias of the Perceptron
        self.learningRate = learningRate                    # Learning rate of the Perceptron
        self.weights = np.zeros((width, height))            # Weights of the Perceptron
        self.trainingSet = trainingSet                      # Set of tuples (specimen, stype) used for training
        self.trainingTime = len(trainingSet)                # Length of training set
        self.trainingThreshold = trainingThreshold          # Boundary for accepting the training results
        self.currentSpecimen = 0                            # Specimen currently used for training the Perceptron
        self.accumError = 0                                 # Error accumulated during training

    def reset(self) -> None:
        self.__init__()

    def threshold(self, input: np.matrix) -> float:
        return np.sum(np.kron(self.weights, input)) + self.bias

    def nextSpecimen(self) -> bool:
        if self.currentSpecimen == self.trainingTime:
            return 0
        sample = self.trainingSet[self.currentSpecimen]
        output = self.threshold(sample[0]) > 0
        diff = sample[1] - output
        self.accumError += np.abs(diff)
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                self.weights[i][j] += self.learningRate * diff * sample[0][i][j]
                # print(self.weights[i][j])
        self.currentSpecimen += 1
        if self.accumError > self.trainingTime * self.trainingThreshold:
            return False
        return True

