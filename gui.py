import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QColor
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
