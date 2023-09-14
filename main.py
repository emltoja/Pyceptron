from PyQt5.QtWidgets import QApplication
from gui import PerceptronTrainingVisualizer, PerceptronEvaluationVisualizer
import typer
import sys

__version__ = "0.1.0"

typerApp = typer.Typer()

@typerApp.command()
def train(): 
    app = QApplication(sys.argv)
    wndw = PerceptronTrainingVisualizer(50, 50)
    wndw.show()
    sys.exit(app.exec_())

@typerApp.command()
def run():
    # raise NotImplementedError("Evaluation mode not implemented yet.")
    app = QApplication(sys.argv)
    wndw = PerceptronEvaluationVisualizer(50, 50)
    wndw.show()
    sys.exit(app.exec_())
    


if __name__ == "__main__":
    print(f"Pyceptron {__version__}")
    typerApp()
