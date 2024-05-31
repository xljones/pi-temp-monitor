# pi-temp-monitor
Python scripts to monitor Raspberry Pi temperature

Tested with Python v3.12, on Raspberry Pi 3 (2015)

## Requirements

N/A

## Usage

Run `python -m app [-h]`

## Help

View the help file with `python -m app -h

```
usage: python -m app [-h] [-o] [-f] [-g]

Raspberry Pi Temperature Monitor (v3.0.0)

optional arguments:
  -h, --help        show this help message and exit
  -o, --once        Just show one instance of the temperature
  -f, --fahrenheit  Show temperature in degress Fahrenheit, default is to use
                    degrees Celsius
  -g, --graph       Show bar graph of temperatures to track trend
```
