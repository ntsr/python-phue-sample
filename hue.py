#!/usr/env python

"""
https://github.com/studioimaginaire/phue
"""

import time
import argparse
from phue import Bridge, PhueRegistrationException, Light
from rgbxy import Converter

DEFAULT_CONFIG_FILE_PATH = './python_hue.json'
GET_INTERVAL = 0.5
SET_INTERVAL = 1

conv = Converter()


def get_args():
    ap = argparse.ArgumentParser(description='Philips Hue Developer Tool.')
    ap.add_argument('action', choices=['demo', 'show', 'set'], help='Action')
    ap.add_argument('--ip', help='HomeBridge IP address', required=True)
    ap.add_argument('-i', '--light-id', type=int, help='Light device No. (1 origin)', required=True)
    ap.add_argument('--off', action='store_true', help='Light off (with set action)')
    ap.add_argument('-b', '--bri', type=int, help='Brightness (0-255)')
    ap.add_argument('-c', '--color-rgb-hex', help='Color RGB Hex (ex: 3e982c)')
    ap.add_argument('--color-rgb', nargs=3, type=int, help='Color RGB (0-255)')
    ap.add_argument('--config-file-path', default=DEFAULT_CONFIG_FILE_PATH, help='Config file path')

    args = ap.parse_args()

    # TODO validation

    return args


def get_bridge(ip, config_file_path) -> Bridge:
    if ip is None:
        print('no IP set!')
        exit()

    while True:
        try:
            b = Bridge(ip=ip, config_file_path=config_file_path)
            b.connect()
            return b
        except PhueRegistrationException:
            print('Searching... Press HomeBridge Button.')
            time.sleep(1)
            continue
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            exit()
        except Exception as e:
            print(e)
            exit()


def get_light(bridge, light_id) -> Light:

    lights = bridge.get_light_objects()
    index = light_id - 1   # light_id is 1 origin
    try:
        return lights[index]
    except:
        print("invalid light_id! :{}".format(light_id))
        return


def main():

    args = get_args()
    bridge = get_bridge(ip=args.ip, config_file_path=args.config_file_path)
    num = args.light_id
    light = get_light(bridge, num) or exit()

    if args.action == "show":
        show_hue(light)
    elif args.action == "set":
        on = not args.off
        bri = args.bri
        rgb_hex = args.color_rgb_hex
        rgb = args.color_rgb
        set_hue(light, on, bri, rgb_hex, rgb)
    else:
        demo(light)


def show_hue(light):
    """
    name, on, bri, rgb, hex, xy
    """
    while True:
        try:
            reachable = light.reachable
            light_id = light.light_id
            on = '--' if not reachable else 'on' if light.on else 'off'
            bri = light.brightness if reachable else "--"
            xy = light.xy if reachable else "--"
            if xy != '--':
                color_rgb = conv.xy_to_rgb(*xy, bri=bri)
                color_hex = conv.xy_to_hex(*xy, bri=bri)

            print("id:{}\t{}\tbri:{}\thex:{}\trgb:{}\txy:{}".format(
                light_id, on, bri, color_hex, color_rgb, xy))
            time.sleep(GET_INTERVAL) 

        except KeyboardInterrupt:
            break

    print('end')


def set_hue(light, on=None, bri=None, rgb_hex=None, rgb=[]):
    if isinstance(on, bool):
        light.on = on

    if isinstance(bri, int) and 0 <= bri <= 255:
        light.brightness = bri

    if isinstance(rgb_hex, str):
        try:
            x, y = conv.hex_to_xy(rgb_hex)
            light.xy = (x, y)
        except:
            print('Invalid rgb_hex!: {}'.format(rgb_hex))
    elif rgb and len(rgb) == 3:
        try:
            x, y = conv.rgb_to_xy(rgb[0], rgb[1], rgb[2])
            light.xy = (x, y)
        except:
            print('Invalid rgb!: {}'.format(rgb))

def demo(light):
    color_hex = '0000ff'
    xy = conv.hex_to_xy(color_hex)

    light.on = True
    light.xy = xy
    light.brightness = 50
    time.sleep(SET_INTERVAL)

    import random
    for _ in range(10):
        x = random.random()
        y = random.random()
        xy = (x, y)
        print(xy)
        light.xy = xy
        time.sleep(SET_INTERVAL)

    light.on = False
    print("done")


if __name__ == '__main__':
    main()


"""
Sample snippets

    # Get the bridge state (This returns the full dictionary that you can explore)
    b.get_api()

    # Prints if light 1 is on or not
    b.get_light(1, 'on')

    # Set brightness of lamp 1 to max
    b.set_light(1, 'bri', 254)

    # Set brightness of lamp 2 to 50%
    b.set_light(2, 'bri', 127)

    # Turn lamp 2 on
    b.set_light(2,'on', True)

    # You can also control multiple lamps by sending a list as lamp_id
    b.set_light( [1,2], 'on', True)

    # Get the name of a lamp
    b.get_light(1, 'name')

    # You can also use light names instead of the id
    b.get_light('Kitchen')
    b.set_light('Kitchen', 'bri', 254)

    # Also works with lists
    b.set_light(['Bathroom', 'Garage'], 'on', False)

    # The set_light method can also take a dictionary as the second argument to do more fancy stuff
    # This will turn light 1 on with a transition time of 30 seconds
    command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}
    b.set_light(1, command)

"""