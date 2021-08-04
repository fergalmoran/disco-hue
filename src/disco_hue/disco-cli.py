#!/usr/bin/env python
import argparse
from enum import Enum

from services.disco_ball import DiscoBall
from services.hue import RegistrationException


class Action(Enum):
    flash = 'flash'
    listBridges = 'bridges'
    listLights = 'lights'
    listInputs = 'inputs'

    def __str__(self):
        return self.value


parser = argparse.ArgumentParser(description='Make your lights dance.')
parser.add_argument('-b', '--bridge-ip', type=str, dest='bridge_ip', required=False,
                    help='IP or DNS name of your Hue bridge')
parser.add_argument('-f', '--file', type=str, dest='file', required=False,
                    help='Audio file to play, omit to use currently playing audio (a bit wonky at the moment)')
parser.add_argument('-l', '--light-id', type=int, dest='light_id',
                    help='ID of the light you wish to flash (blank to choose interactively)')
parser.add_argument('-a', '--action', type=Action, dest='action', required=False, default=Action.flash,
                    help='Action to perform')
parser.add_argument('-s', '--silent', action='store_true', dest='silent', required=False,
                    help='Suppress non data output')

args = parser.parse_args()


def print_bridge_list(bridges, separator='\t'):
    for bridge in bridges:
        print(f"{bridge['id']}{separator}{bridge['value']}", sep='\n')


def print_light_list(lights, separator='\t'):
    for light in lights:
        print(f"{light['id']}{separator}{light['value']}", sep='\n')


def get_light_id(lights):
    print('\n')
    print('Id - Name')
    print('===========================================')
    print_light_list(lights, '  - ')

    while True:
        id = input('Please select id of light you wish to flash: ')

        if id.isdigit() and int(id) in lights:
            return id

        print('Invalid light selected')


if __name__ == '__main__':
    # First check if we're performing an action that doesn't require a light-id
    if args.action == Action.listBridges:
        if not args.silent:
            print('Looking for bridges, please wait')
        b = DiscoBall.get_bridge_list()
        print_bridge_list(b)
        exit(0)

    try:
        if not args.bridge_ip:
            print('Bridge IP not specified')
            exit(1)

        manager = DiscoBall(args.bridge_ip)
        if args.action == Action.listLights:
            print_light_list(manager.get_light_list())

        elif not args.light_id:
            args.light_id = get_light_id(manager.get_light_list())

        if args.light_id:
            manager.play_audio_file(args.light_id, args.file)

    except RegistrationException:
        print('Failed to register with Hue Bridge. Press registration button and try again.')
        exit(1)

    except Exception as e:
        print(f'Error performing action, {e}')
        exit(1)
