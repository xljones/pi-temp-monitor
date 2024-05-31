from datetime import datetime
import math
import os
import re
import time

from app.graphing import CursesBarGraph


class TemperatureViewController:
    clock_speed = {
        "setpoint": -999,
        "current": -999,
        "setpoint_last_update": datetime.now(),
    }
    temperature = {"current": -999}

    def __init__(self, args, version):
        self._args = args
        self._version = version

    def _print_header(self) -> None:
        print("")
        print(f"Raspberry Pi Temperature Monitor v{self._version}")
        print("")

    def _get_temperature(self, fahrenheit: bool) -> float:
        system_cmd = os.popen("vcgencmd measure_temp")
        get_str = system_cmd.read()
        regex_pattern = re.compile(r"temp=([\d\.]+)'[CF]")
        regex_matches = regex_pattern.match(get_str)
        self.temperature["current"] = float(regex_matches.group(1))
        if self._args.fahrenheit:
            self.temperature["current"] = (
                self.temperature["current"] * (9 / 5)
            ) + 32
        return round(self.temperature["current"], 1)

    def _get_clock_speed_setpoint(self) -> float:
        # Returns clock speed in kHz
        system_cmd = os.popen("vcgencmd get_config arm_freq")
        get_str = system_cmd.read()
        regex_pattern = re.compile(r"arm_freq=([\d\.]+)")
        regex_matches = regex_pattern.match(get_str)
        self.clock_speed["setpoint"] = (
            float(regex_matches.group(1)) / 1000
        )  # Command returns in MHz, /1000 convert to GHz
        self.clock_speed["setpoint_last_update"] = datetime.now()
        return round(self.clock_speed["setpoint"], 1)

    def _get_clock_speed_current(self) -> float:
        # Returns clock speed in Hz
        system_cmd = os.popen("vcgencmd measure_clock arm")
        get_str = system_cmd.read()
        regex_pattern = re.compile(r"frequency\(\d+\)=([\d\.]+)")
        regex_matches = regex_pattern.match(get_str)
        self.clock_speed["current"] = (
            float(regex_matches.group(1)) / 1000000000
        )  # Command returns in Hz, /1000000 to convert to GHz
        return round(self.clock_speed["current"], 1)

    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%d/%m//%Y, %H:%M:%S")

    def graph_temperature(self) -> None:
        with CursesBarGraph() as bar_graph:
            while True:
                values = []
                for i in range(200):
                    values.append(100 * (math.sin(0.05 + i / 20.0) + 1) / 2.0)
                bar_graph.update(values)

    def text_temperature(self) -> None:
        self._print_header()
        output = "{0} (CPU {1}/{2}GHz): {3}°{4}     "
        while True:
            print(
                output.format(
                    self._get_timestamp(),
                    self._get_clock_speed_current(),
                    self._get_clock_speed_setpoint(),
                    self._get_temperature(self._args.fahrenheit),
                    "F" if self._args.fahrenheit else "C",
                ),
                end="\r" if exit else "",
            )
            if self._args.once:
                print("\n")
                break
            else:
                time.sleep(1)
            
