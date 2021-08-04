import sys

from PyQt6.QtWidgets import QApplication

from desktop import App

app = QApplication(sys.argv)
win = App()


def bootstrap_app():
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    bootstrap_app()
