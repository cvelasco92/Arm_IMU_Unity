import sys
from PySide6.QtWidgets import QApplication
from model import SensorModel
from view import SensorView
from controller import SensorController

def main():
    app = QApplication(sys.argv)

    model = SensorModel()
    view = SensorView()
    controller = SensorController(model, view)

    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()