"""
    Class to co-ordinate messaging between audio & lights
"""
import threading

from services.audio.beat_detector import BeatDetector
from services.audio.errors import noalsaerr
from services.hue import HueManager

ORANGE = (0.6, 0.4)
RED = (0.67, 0.32)
GREEN = (0.15, 0.8)
PURPLE = (0.25, 0.1)
PINK = (0.5, 0.25)
COLOURS = [
    ORANGE,
    RED,
    GREEN,
    PURPLE,
    PINK
]


class DiscoBall:

    def __init__(self, bridge_ip):
        self._bridge_ip = bridge_ip
        self._light_id = -1
        self._bridge = HueManager(bridge_ip)
        self._beat_detector = None

    @staticmethod
    def get_bridge_list():
        return HueManager.get_bridge_list()

    def get_light_list(self):
        return self._bridge.get_light_list()

    def flash_light(self, beat):
        flash_thread = threading.Thread(
            target=self._flash_light_internal,
            name="flasher", args=[beat])
        flash_thread.start()

    def _flash_light_internal(self, beat):
        on = (beat % 2) == 0
        colour = COLOURS[beat % len(COLOURS) - 1]
        self._bridge.set_light(
            self._light_id,
            {
                'transitiontime': 0,
                'on': on,
                'xy': colour,
                'bri': 254
            }
        )
        beat += 1

    def play_audio_file(self, light_id, file):
        self._light_id = light_id
        print('Starting playback')
        play_thread = threading.Thread(
            target=self._play_internal,
            name="flasher", args=[file])
        play_thread.start()

    def _play_internal(self, file):
        with noalsaerr():
            if file:
                self._beat_detector = BeatDetector(self.flash_light)
                self._beat_detector.play_audio_file(
                    file
                )
            else:
                self._beat_detector.play_captured()

    def stop(self):
        if self._beat_detector is not None:
            self._beat_detector.stop()
