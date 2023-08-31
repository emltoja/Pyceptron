from PyQt5.QtWidgets import QApplication
from gui import PerceptronVisualizer
import sys

app = QApplication(sys.argv)
wndw = PerceptronVisualizer(30, 30)
wndw.show()
sys.exit(app.exec_())
