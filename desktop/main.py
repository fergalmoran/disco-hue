import subprocess
import sys
import threading

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog

from main_window import Ui_MainWindow
from services.disco_ball import DiscoBall


class BridgeNotRegisteredException(Exception):
    pass


class BridgeNotFoundException(Exception):
    pass


class App(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('./ui/main.ui', self)
        self._manager = None
        self._bootstrap_ui()

    def _bootstrap_ui(self):
        print('Scanning for Hue Bridges')
        bridges = DiscoBall.get_bridge_list()

        if len(bridges) != 0:
            for bridge in bridges:
                self.bridgeList.addItem(bridge['value'])
            self._select_bridge(0)

        self.bridgeList.currentIndexChanged.connect(self._select_bridge)
        self.refreshBridges.clicked.connect(lambda: self._select_bridge(self.bridgeList.currentIndex()))
        self.chooseFile.clicked.connect(self._choose_input_file)
        self.startButton.clicked.connect(self._play_audio_file)

    def _select_bridge(self, index):
        ip = self.bridgeList.itemText(index)
        self._manager = DiscoBall(ip)
        try:
            lights = self._manager.get_light_list()
            print(lights)

            for light in lights:
                self.lightsList.addItem(light['value'])
        except BridgeNotRegisteredException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("This application is not registered with this Hue Bridge")
            msg.setInformativeText("Please press the register button on top of the bridge and click the retry button")
            msg.setWindowTitle("Error")
            msg.show()

    def _choose_input_file(self):
        fname = QFileDialog.getOpenFileName(
            win,
            'Open file',
            '~',
            'Audio Files (*.mp3 *.wav *.ogg)')
        self.inputFileName.setText(fname[0])

    def _play_audio_file(self):
        audio_thread = threading.Thread(target=self._play_audio_file_internal, name="player")
        audio_thread.start()

    def _play_audio_file_internal(self):
        command = [
            '../disco-hue.py',
            '--action', 'flash',
            '--file', self.inputFileName.text(),
            '--light-id', '1',
            '--bridge-ip', self.bridgeList.currentText()
        ]
        subprocess.run(command, stdout=subprocess.PIPE)

    def closeEvent(self, event):
        if self._manager is not None:
            self._manager.stop()
        event.accept()


app = QApplication(sys.argv)
win = App()


def bootstrap_app():
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    bootstrap_app()
