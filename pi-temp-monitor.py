'''
    Script:  pi-temp.monitor.py
    Author:  Xander Jones (xander@xljones.com)
    Web:     xljones.com
    Date:    4 April 2020
'''

import argparse
import tvc

_VERSION = "2.0.0"

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='Raspberry Pi Temperature Monitor (v{0})'.format(_VERSION))
    # p.add_argument('-v', '--verbose', help='Turn on verbose logging', action='store_true')
    # p.add_argument('-r', '--record', help='Record data to file')
    p.add_argument('-o', '--once', help='Just show one instance of the temperature', action='store_true')
    p.add_argument('-f', '--fahrenheit', help='Show temperature in degress Fahrenheit, default is to use degrees Celsius', action='store_true')
    p.add_argument('-g', '--graph', help='Show bar graph of temperatures to track trend', action='store_true')
    args = p.parse_args()

    tempcontroller = tvc.TemperatureViewController(args, _VERSION)

    if args.graph:
        tempcontroller.graph_temperature()
    else:
        tempcontroller.text_temperature()
