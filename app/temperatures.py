import os
import re
import time
from datetime import datetime
from typing import Any


class TemperatureViewController:
    clock_speed = {
        "setpoint": -999.0,
        "current": -999.0,
    }
    temperature = {"current": -999.0}

    def __init__(self, args: Any, version: str) -> None:
        self._args = args
        self._version = version

    def graph_temperature(self) -> None:
        raise NotImplementedError("Graphing is not implemented yet")

    def text_temperature(self) -> None:
        OUTPUT = (
            "{timestamp} (CPU {current_cpu_speed}"
            "/{setpoint_cpu_speed}GHz): {temperature}     "
        )

        self._print_header()
        while True:
            print(
                OUTPUT.format(
                    timestamp=self._get_timestamp(),
                    current_cpu_speed=self._get_clock_speed_current(),
                    setpoint_cpu_speed=self._get_clock_speed_setpoint(),
                    temperature=self._format_temperature(
                        temperature=self._get_temperature(),
                    ),
                ),
                end="\r" if not self._args.once else "",
            )
            if self._args.once:
                print("\n")
                break
            else:
                time.sleep(1)

    def _print_header(self) -> None:
        print("")
        print(f"Raspberry Pi Temperature Monitor v{self._version}")
        print("")

    @staticmethod
    def _sys_cmd_and_regex(command: str, regex_pattern: str) -> str:
        response = os.popen(command).read()
        regex = re.compile(regex_pattern)
        matches = regex.match(response)
        assert matches
        return matches.group(1)

    def _get_temperature(self) -> float:
        temperature_str = self._sys_cmd_and_regex(
            command="vcgencmd measure_temp",
            regex_pattern=r"temp=([\d\.]+)'[CF]",
        )
        self.temperature["current"] = float(temperature_str)
        return round(self.temperature["current"], 1)

    def _get_clock_speed_setpoint(self) -> float:
        # Returns clock speed in kHz
        clock_speed = self._sys_cmd_and_regex(
            command="vcgencmd get_config arm_freq",
            regex_pattern=r"arm_freq=([\d\.]+)",
        )
        self.clock_speed["setpoint"] = float(clock_speed) / 1_000
        return round(self.clock_speed["setpoint"], 1)

    def _get_clock_speed_current(self) -> float:
        # Returns clock speed in Hz
        clock_speed = self._sys_cmd_and_regex(
            command="vcgencmd measure_clock arm",
            regex_pattern=r"frequency\(\d+\)=([\d\.]+)",
        )
        self.clock_speed["current"] = float(clock_speed) / 1_000_000_000
        return round(self.clock_speed["current"], 1)

    def _format_temperature(
        self,
        temperature: float,
    ) -> str:
        TEMPLATE = "{temperature}°{unit}"

        if self._args.fahrenheit:
            return TEMPLATE.format(
                temperature=(temperature * (9 / 5)) + 32,
                unit="F",
            )

        return TEMPLATE.format(temperature=temperature, unit="C")

    def _get_timestamp(self) -> str:
        return datetime.now().strftime("%d/%m//%Y, %H:%M:%S")
