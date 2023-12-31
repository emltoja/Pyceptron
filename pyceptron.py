import numpy as np


class Perceptron:

    # Initialize the Perceptron
    def __init__(
        self,
        width,
        height,
        trainingSet,
        bias=0,
        learningRate=0.1,
        trainingThreshold=0.1,
    ) -> None:
        self.dims = (width, height)                                    # Dimension of percepted specimens (as well as dimension of weights matrix)
        self.bias = bias                                               # Bias of the Perceptron
        self.learningRate = learningRate                               # Learning rate of the Perceptron
        self.weights = np.zeros((width, height))                       # Weights of the Perceptron
        self.trainingSet = trainingSet                                 # Set of tuples (specimen, stype) used for training
        self.trainingTime = len(trainingSet) if trainingSet else 0     # Length of training set
        self.trainingThreshold = trainingThreshold                     # Boundary for accepting the training results
        self.currentSpecimen = 0                                       # Specimen currently used for training the Perceptron
        self.accumError = 0                                            # Error accumulated during training


    # Restart the perceptron
    def reset(self) -> None:
        self.__init__(*self.dims, self.trainingSet, self.bias, self.learningRate, self.trainingThreshold)

    # Linear output of the neuron
    def threshold(self, input: np.matrix) -> float:
        return np.sum(np.multiply(self.weights, input)) + self.bias


    # Train the Perceptron on next specimen in training set
    def nextSpecimen(self) -> bool:

        
        sample = self.trainingSet[self.currentSpecimen]
        specimen = sample[0]
        desired = sample[1]
        output = 1 if self.threshold(specimen) > 0 else 0
        diff = desired - output
        self.accumError += np.abs(diff)

        # Update the weights
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                self.weights[i][j] += self.learningRate * diff * sample[0][i][j]

        self.currentSpecimen += 1
        
        # Last specimen in the set. Finish training
        if self.currentSpecimen == self.trainingTime - 1:
            self.currentSpecimen = 0
            return False
        
        # If the training threshold has been passeed, then finish the training
        if self.accumError > self.trainingTime * self.trainingThreshold:
            return False
        return True


    # Evaluate the given input by weights
    # True - Rectangle
    # False - Circle
    def evaluate(self, input) -> bool:
        result = self.threshold(input)
        print(result)
        return result > 0
