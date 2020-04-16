# pi-temp-monitor 
Python scripts to monitor Raspberry Pi temperature

Tested with Python v3.7.3, on Raspberry Pi 2 Model B (v1.1)

## Requirements
None other than basic Python install on Raspbian.

## Running the script
Run `python3 pi-temp-monitor.py [-o] [-f]` to get the basic output

## Help
```
usage: pi-temp-monitor.py [-h] [-o] [-f]

Raspberry Pi Temperature Monitor (v1.0.1)

optional arguments:
  -h, --help        show this help message and exit
  -o, --once        Just show one instance of the temperature
  -f, --fahrenheit  Show temperature in degrees Fahrenheit, default is to use
                    degrees Celsius
```
