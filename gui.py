import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt, QTimer
from pyceptron import Perceptron
from specimens import Generator


class WeightsDisplayer(QWidget):
    def __init__(self, weights) -> None:
        super().__init__()
        self.colors = weights
        self.num_rows, self.num_cols = np.shape(weights)

        self.cell_width = 30
        self.cell_height = 30

        self.setMinimumSize(
            self.num_cols * self.cell_width, self.num_rows * self.cell_height
        )

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

    def resizeEvent(self, event) -> None:
        available_width = self.width()
        available_height = self.height()
        self.cell_width = available_width // self.num_cols
        self.cell_height = available_height // self.num_rows

        self.update()


class Visualizer(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Pyceptron")

    def perceptronWeights(self, p: Perceptron) -> None:
        display = WeightsDisplayer(p.weights)
        self.setCentralWidget(display)

    def specimenRectangle(self, width, height) -> None:
        g = Generator(width, height)
        display = WeightsDisplayer(g.generate_rect())
        self.setCentralWidget(display)

    def specimenCircle(self, width, height) -> None:
        g = Generator(width, height)
        display = WeightsDisplayer(g.generate_circle())
        self.setCentralWidget(display)


class PerceptronVisualizer(Visualizer):
    def __init__(self, width, height) -> None:
        
        super().__init__()
        gen = Generator(width, height)
        trainingSet = []
        for _ in range(500):
            trainingSet.append((gen.generate_rect(), 0))
            trainingSet.append((gen.generate_circle(), 1))
        self.perceptron = Perceptron(width, height, trainingSet)
        self.display = WeightsDisplayer(self.perceptron.weights)

        self.button = QPushButton("Start Training")
        self.button.clicked.connect(self.startTraining)

        layout = QVBoxLayout()
        layout.addWidget(self.button, alignment=Qt.AlignTop)
        layout.addWidget(self.display)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def startTraining(self) -> None:

        # print('ButtonClicked')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.trainPerceptron)
        self.timer.start(10)

    def trainPerceptron(self) -> None:
        # print('Training Going on')
        self.perceptron.nextSpecimen()
        self.display.colors = self.perceptron.weights
        self.display.update()
