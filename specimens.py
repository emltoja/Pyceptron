import numpy as np


class Generator:
    def __init__(self, width, height) -> None:
        self.dims = (width, height)

    def generate_rect(self) -> np.matrix:
        rectWidth = np.random.randint(0, self.dims[0])
        rectHeight = np.random.randint(0, self.dims[1])

        x = np.random.randint(0, self.dims[0] - rectWidth)
        y = np.random.randint(0, self.dims[1] - rectHeight)

        specimen = np.zeros(self.dims)

        # Upper and lower bound
        for i in range(x, x + rectWidth + 1):
            specimen[i][y] = 1
            specimen[i][y + rectHeight] = 1

        # Sides
        for j in range(y, y + rectHeight + 1):
            specimen[x][j] = 1
            specimen[x + rectWidth][j] = 1

        return specimen

    def generate_circle(self) -> np.matrix:
        radius = np.random.randint(0, min(self.dims) // 2)

        x = np.random.randint(radius, self.dims[0] - radius)
        y = np.random.randint(radius, self.dims[1] - radius)

        specimen = np.zeros(self.dims)

        for i in range(0, 100):
            angle = 0.02 * np.pi * i
            xpos = np.round(x + radius * np.cos(angle)).astype(int)
            ypos = np.round(y + radius * np.sin(angle)).astype(int)

            specimen[xpos][ypos] = 1

        return specimen
