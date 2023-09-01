from PyQt5.QtWidgets import QApplication
from gui import PerceptronVisualizer
import typer
import sys

__version__ = "0.1.0"

typerApp = typer.Typer()

@typerApp.command()
def train(): 
    app = QApplication(sys.argv)
    wndw = PerceptronVisualizer(30, 30)
    wndw.show()
    sys.exit(app.exec_())

@typerApp.command()
def run():
    raise NotImplementedError("Evaluation mode not implemented yet.")


if __name__ == "__main__":
    print(f"Pyceptron {__version__}")
    typerApp()
