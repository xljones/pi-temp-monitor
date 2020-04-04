'''
    Script:  pi-temp.monitor.py
    Author:  Xander Jones (xander@xljones.com)
    Web:     xljones.com
    Date:    4 April 2020
'''

import os
import re
import argparse
import datetime
import time

_VERSION = "1.0.0"

class TemperatureController:
    current_temp = -999
    args = []
    def __init__(self, argsin):
        args = argsin

    def _get_temperature(self, fahrenheit):
        system_cmd = os.popen("vcgencmd measure_temp")
        temp_str = system_cmd.read()
        regex_pattern = re.compile("temp=([\d\.]+)'[CF]")
        regex_matches = regex_pattern.match(temp_str)
        self.current_temp = float(regex_matches.group(1))
        if args.fahrenheit:
            self.current_temp = (self.current_temp * (9/5)) + 32
        return(round(self.current_temp,1))

    def _get_timestamp(self):
        now = datetime.datetime.now()
        return (now.strftime("%d/%m//%Y, %H:%M:%S"))

    def monitor_temperature(self):
        output = "     {0}: {1}*{2}         ".format(self._get_timestamp(), self._get_temperature(args.fahrenheit), "F" if args.fahrenheit else "C")
        if args.once:
            print(output)
            print()
        else:
            while (True):
                print(output, end="\r")
                time.sleep(1)


def print_header():
    print("")
    print("     Raspberry Pi Temperature Monitor")
    print("     Xander Jones v{0}".format(_VERSION))
    print("")



if (__name__ == "__main__"):
    p = argparse.ArgumentParser(description='Raspberry Pi Temperature Monitor (v{0})'.format(_VERSION))
    # p.add_argument('-v', '--verbose', help='Turn on verbose logging', action='store_true')
    # p.add_argument('-r', '--record', help='Record data to file')
    p.add_argument('-o', '--once', help='Just show one instance of the temperature', action='store_true')
    p.add_argument('-f', '--fahrenheit', help='Show temperature in degress Fahrenheit, default is to use degrees Celsius', action='store_true')
    args = p.parse_args()

    print_header()
    tcon = TemperatureController(args)
    tcon.monitor_temperature()
