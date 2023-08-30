from PyQt5.QtWidgets import QApplication
from gui import Visualizer
import sys

app = QApplication(sys.argv)
wndw = Visualizer()
# wndw.specimenRectangle(30, 30)
wndw.specimenCircle(30, 30)
wndw.show()
sys.exit(app.exec_())
