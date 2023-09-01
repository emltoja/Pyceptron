'''Pyceptron gui'''

import numpy as np
from PyQt5.QtWidgets import QWidget, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
from pyceptron import Perceptron
from specimens import Generator


class WeightsDisplayer(QWidget):
    '''Display the weights or specimen as rectangular cell matrix'''

    # Initialize the weights matrix in the main window
    def __init__(self, weights) -> None:
        super().__init__()
        self.colors = weights
        self.num_rows, self.num_cols = np.shape(weights)

        self.cell_width = 20
        self.cell_height = 20

        self.setMinimumSize(
            self.num_cols * self.cell_width, self.num_rows * self.cell_height
        )

    # Paint the matrix onto the screen
    def paintEvent(self, event) -> None:
        painter = QPainter(self)

        for row in range(self.num_rows):
            for col in range(self.num_cols):
                value = self.colors[row][col]
                color = QColor.fromRgbF(value, value, value)

                painter.setBrush(color)
                painter.drawRect(
                    col * self.cell_width,
                    row * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                )


    # Adjust the cell size if resized
    def resizeEvent(self, event) -> None:
        available_width = self.width()
        available_height = self.height()
        self.cell_width = available_width // self.num_cols
        self.cell_height = available_height // self.num_rows

        self.update()


# Main window
class Visualizer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pyceptron")

    # Display given perceptron weights
    def perceptronWeights(self, p: Perceptron) -> None:
        display = WeightsDisplayer(p.weights)
        self.setCentralWidget(display)

    # Display rectangular specimen
    def specimenRectangle(self, width, height) -> None:
        g = Generator(width, height)
        display = WeightsDisplayer(g.generate_rect())
        self.setCentralWidget(display)

    # Display circular specimen
    def specimenCircle(self, width, height) -> None:
        g = Generator(width, height)
        display = WeightsDisplayer(g.generate_circle())
        self.setCentralWidget(display)


# Main window with attached perceptron
class PerceptronVisualizer(Visualizer):

    # Initialize the window
    def __init__(self, width, height) -> None:

        super().__init__()
        gen = Generator(width, height)

        # Generate the training set
        trainingSet = []
        for _ in range(1000):
            trainingSet.append((gen.generate_rect(), 0))
            trainingSet.append((gen.generate_circle(), 1))

        # Attach perceptron and weights matrix display
        self.perceptron = Perceptron(width, height, trainingSet, trainingThreshold=1)
        self.weightsDisplay = WeightsDisplayer(self.perceptron.weights)
        currentSpecimen = self.perceptron.trainingSet[self.perceptron.currentSpecimen][0]
        self.specimenDisplay = WeightsDisplayer(currentSpecimen)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.trainPerceptron)

        # Utilities buttons
        self.startButton = QPushButton("Start training")
        self.startButton.clicked.connect(self.startTraining)

        self.stopButton = QPushButton("Stop training")
        self.stopButton.clicked.connect(self.timer.stop)

        self.saveButton = QPushButton("Save training results")
        self.saveButton.clicked.connect(self.saveResults)

        self.loadButton = QPushButton("Load last training result")
        self.loadButton.clicked.connect(self.loadResults)

        self.resetButton = QPushButton("Reset Perceptron")
        self.resetButton.clicked.connect(self.resetPerceptron)


        # Layout for start/stop buttons
        controlLayout = QVBoxLayout()
        controlLayout.addWidget(self.startButton, alignment=Qt.AlignTop)
        controlLayout.addWidget(self.stopButton)

        # Layout for saving/loading buttons
        saveloadLayout = QVBoxLayout()
        saveloadLayout.addWidget(self.saveButton, alignment=Qt.AlignTop)
        saveloadLayout.addWidget(self.loadButton)

        # Button layout
        buttonLayout = QHBoxLayout()
        buttonLayout.addLayout(controlLayout)
        buttonLayout.addLayout(saveloadLayout)
        buttonLayout.addWidget(self.resetButton)

        # Display layout
        displayLayout = QHBoxLayout()
        displayLayout.addWidget(self.weightsDisplay)
        displayLayout.addWidget(self.specimenDisplay)

        # Main layout
        layout = QVBoxLayout()
        layout.addLayout(buttonLayout)
        layout.addLayout(displayLayout)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    # Begin training of the Perceptron
    def startTraining(self) -> None:

        self.timer.start(10)

    # Training routine
    def trainPerceptron(self) -> None:

        if not self.perceptron.nextSpecimen():
            self.timer.stop()
            print('Training stopped')
        self.weightsDisplay.colors = self.perceptron.weights
        self.weightsDisplay.update()
        currentSpecimen = self.perceptron.trainingSet[self.perceptron.currentSpecimen][0]
        self.specimenDisplay.colors = currentSpecimen
        self.specimenDisplay.update()

    # Save training results into the file 
    def saveResults(self) -> None:
        
        stoped = False
        if self.timer.isActive():
            self.timer.stop()
            stoped = True

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Data", "", "Numpy array (*.npy);;All Files(*)", options=options
        )

        if file_name:
            with open(file_name, "wb") as f:
                np.save(f, self.perceptron.weights)

        if stoped:
            self.timer.start(10)

    # Load perceptron weights from the file
    def loadResults(self) -> None:
        if self.timer.isActive():
            self.timer.stop()
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Load Data", "", "Numpy array (*.npy);;All Files(*)", options=options
        )

        if file_name:
            with open(file_name, "rb") as f:
                self.perceptron.weights = np.load(f)
        self.weightsDisplay.colors = self.perceptron.weights
        self.weightsDisplay.update()

    # Reset the Perceptron
    def resetPerceptron(self):

        self.perceptron.reset()
        self.weightsDisplay.colors = self.perceptron.weights
        self.weightsDisplay.update()
