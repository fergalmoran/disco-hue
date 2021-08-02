import unittest

from services.hue import HueManager

"""
    Highly dependent on my personal network
    To run tests on your network, change below as appropriate
"""
BRIDGE_IP = '10.1.1.20'
TD_BRIDGES = [{
    'id': '001788a73030',
    'ip': BRIDGE_IP
}]
TD_LIGHTS = [
    {'id': 1, 'value': 'Living Room Main Light'},
    {'id': 2, 'value': 'Hallway Two'},
    {'id': 4, 'value': "Penny's Bedroom Main Light"},
    {'id': 5, 'value': "Dad's Office Main Light"},
    {'id': 6, 'value': "Dad's Bedroom Main Light"},
    {'id': 7, 'value': 'Hallway 1'}
]


class BridgeTests(unittest.TestCase):

    def test_bridge_list(self):
        bridges = HueManager.get_bridge_list()
        self.assertListEqual(bridges, TD_BRIDGES)

    def test_light_list(self):
        manager = HueManager(BRIDGE_IP)
        lights = manager.get_light_list()
        self.assertListEqual(lights, TD_LIGHTS)


if __name__ == '__main__':
    unittest.main()
