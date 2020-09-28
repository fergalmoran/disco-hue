#!/usr/bin/env python
import argparse
from hue.hue_manager import HueManager, RegistrationException
from audio.beat_detector import BeatDetector
from audio.errors import noalsaerr

parser = argparse.ArgumentParser(description='Make your lights dance.')
parser.add_argument('-b', '--bridge-ip', type=str, dest='bridge_ip', required=True,
                    help='IP or DNS name of your Hue bridge')
parser.add_argument('-f', '--file', type=str, dest='file', required=False,
                    help='Audio file to play, omit to use currently playing audio (a bit wonky at the moment)')
parser.add_argument('-l', '--light-id', type=int, dest='light_id',
                    help='ID of the light you wish to flash (blank to choose interactively)')


args = parser.parse_args()
try:
    bridge_manager = HueManager(args.bridge_ip)
except RegistrationException:
    print('Failed to register with Hue Bridge. Press registration button and try again.')

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


def get_light_id():

    lights = bridge_manager.get_light_list()

    print('\n')
    print('Id - Name')
    print('===========================================')
    for id, light in lights.items():
        print(f'{id}  - {light.name}')

    while True:
        id = input('Please select id of light you wish to flash: ')

        if id.isdigit() and int(id) in lights:
            return id

        print('Invalid light selected')


def flash_light(beat):
    on = (beat % 2) == 0
    colour = COLOURS[beat % len(COLOURS) - 1]
    bridge_manager.set_light(
        args.light_id,
        {
            'transitiontime': 0,
            'on': on,
            'xy': colour,
            'bri': 254
        }
    )
    beat += 1


if not args.light_id:
    args.light_id = get_light_id()

beat_detector = BeatDetector(flash_light)

print('Starting playback')
with noalsaerr():
    if args.file:
        beat_detector.play_audio_file(args.file)
    else:
        beat_detector.play_captured()
