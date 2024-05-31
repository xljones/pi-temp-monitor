import argparse

from app.temperatures import TemperatureViewController

_VERSION = "3.0.0"

if (__name__ == "__main__"):
    p = argparse.ArgumentParser(
        description=f"Raspberry Pi Temperature Monitor (v{_VERSION})"
    )
    p.add_argument('-o', '--once', help='Just show one instance of the temperature', action='store_true')
    p.add_argument('-f', '--fahrenheit', help='Show temperature in degress Fahrenheit, default is to use degrees Celsius', action='store_true')
    p.add_argument('-g', '--graph', help='Show bar graph of temperatures to track trend', action='store_true')
    args = p.parse_args()

    tempcontroller = TemperatureViewController(args, _VERSION)

    if args.graph:
        tempcontroller.graph_temperature()
    else:
        tempcontroller.text_temperature()
