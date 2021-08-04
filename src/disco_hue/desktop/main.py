from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QFileDialog

from desktop import BridgeNotRegisteredException, DiscoverBridgesThread
from services import DiscoBall


class App(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('./desktop/ui/main.ui', self)
        self._settings = QSettings('disco_hue')
        self._manager = None
        self._selected_light = None
        self._bootstrap_ui()

    def _bridge_list_finished(self, bridges):
        self._bridges = bridges
        self._settings.setValue('discovered_bridges', self._bridges)
        self.bridgeList.clear()
        if len(bridges) != 0:
            for bridge in self._bridges:
                self.bridgeList.addItem(bridge['value'])
            self._select_bridge(0)

    def _populate_bridges(self):
        previous_bridges = self._settings.value('discovered_bridges')
        if previous_bridges is not None:
            self._bridge_list_finished(previous_bridges)
        else:
            self.discover_bridges_thread = DiscoverBridgesThread(self._bridge_list_finished)
            self.discover_bridges_thread.start()

    def _bootstrap_ui(self):

        self._populate_bridges()
        self.bridgeList.currentIndexChanged.connect(self._select_bridge)
        self.lightsList.currentIndexChanged.connect(self._select_light)
        self.refreshBridges.clicked.connect(lambda: self._select_bridge(self.bridgeList.currentIndex()))
        self.chooseFile.clicked.connect(self._choose_input_file)
        self.startButton.clicked.connect(self._play_audio_file)
        self.inputFileName.setText(self._settings.value('last_audio_file'))

    def _select_light(self, index):
        self._selected_light = self._lights[index]
        self._settings.setValue('selected_light', index)

    def _select_bridge(self, index):
        bridge = self._bridges[index]
        self._settings.setValue('selected_bridge', index)
        self._manager = DiscoBall(bridge['value'])

        try:
            self._lights = self._manager.get_light_list()
            self.lightsList.clear()
            for light in self._lights:
                self.lightsList.addItem(light['value'])
            self._select_light(0)

        except BridgeNotRegisteredException as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("This application is not registered with this Hue Bridge")
            msg.setInformativeText("Please press the register button on top of the bridge and click the retry button")
            msg.setWindowTitle("Error")
            msg.show()

    def _choose_input_file(self):
        fname = QFileDialog.getOpenFileName(
            self,
            'Open file',
            '~',
            'Audio Files (*.mp3 *.wav *.ogg)')
        self.inputFileName.setText(fname[0])
        self._settings.setValue('last_audio_file', fname[0])

    def _play_audio_file(self):
        self._manager.play_audio_file(
            self._selected_light['id'],
            self.inputFileName.text())

    def closeEvent(self, event):
        if self._manager is not None:
            self._manager.stop()
        event.accept()
