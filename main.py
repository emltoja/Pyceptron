from PyQt5.QtWidgets import QApplication
from gui import Visualizer
import sys

app = QApplication(sys.argv)
wndw = Visualizer()
sys.exit(app.exec_())
