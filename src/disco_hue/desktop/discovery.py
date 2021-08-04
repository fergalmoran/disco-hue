from PyQt6.QtCore import pyqtSignal, QObject, QThread

from services import DiscoBall


class BridgeNotRegisteredException(Exception):
    pass


class BridgeNotFoundException(Exception):
    pass


class DiscoverBridgesResult(QObject):
    def __init__(self, val):
        QObject.__init__(self)
        self.val = val


class DiscoverBridgesThread(QThread):
    _finished = pyqtSignal(object)

    def __init__(self, callback, parent=None):
        QThread.__init__(self, parent)
        self._finished.connect(callback)

    def run(self):
        print('Scanning for Hue Bridges')
        bridges = DiscoBall.get_bridge_list()
        self._finished.emit(bridges)
