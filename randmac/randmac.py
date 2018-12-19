# -*- coding: utf-8 -*-

"""
Randomizes the 6 digit NIC portion of the MAC address required for input.

Optional argument will generate a 12-digit LAA.

Supported MAC address formats:
    MM:MM:MM:SS:SS:SS
    MM-MM-MM-SS-SS-SS
    MMMM.MMSS.SSSS
    MMMMMMSSSSSS
"""

import argparse
import random
import sys
import os
import textwrap
from enum import Enum


def _setup_parser(_about: dict) -> argparse:
    """Setup parser for arguments passed in from the CLI.

    Returns:
      argparse object.
    """
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
            Generates MAC addresses. By default will only generate a new NIC 
              portion for the input MAC address.

            Optionally generate a 12-digit Locally Administrated Address.
 
            Only supports 12-digit MAC addresses.
            """
        ),
        epilog="Made with Python by {}".format(_about["__author__"]),
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "mac", nargs="?", default="empty", help="mac address required for output format"
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {}".format(_about["__version__"]),
    )
    parser.add_argument(
        "-f",
        "--full",
        action="store_true",
        help="generates a 12-digit LAA",
    )
    return parser


class RandMac:  # pylint: disable=too-few-public-methods
    _LOCAL = ["2", "6", "a", "e"]

    _HEX = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
    ]

    _LOWERCASE = True

    class Format(Enum):
        """type of MAC address formats"""

        HYPHEN = 1
        COLON = 2
        PERIOD = 3
        CISCO = 4
        NONE = 5
        UNKNOWN = 6

    def __init__(self, mac: str, is_12_digit_mac=None) -> None:
        trimmed = self._trim_separator(mac)
        _chars = []
        for _char in trimmed:
            if _char not in self._HEX:
                _chars.append(_char)
        if _chars:
            raise ValueError("Invalid characters in MAC format {}".format(_chars))
        if len(trimmed) != 12:
            raise ValueError("MAC must be 12 digits but found {}".format(len(trimmed)))

        _format = self._get_mac_format(mac)

        if is_12_digit_mac:
            not_formatted = self._build_random_twelve_digit()
        else:
            not_formatted = self._build_random_nic(trimmed)
        self.mac = self._build_mac_with_separator(
            self._set_lettercase(not_formatted), _format
        )

    def __repr__(self) -> str:
        return repr(self.mac)

    @staticmethod
    def _trim_separator(mac: str) -> str:
        """removes separator from MAC address"""
        return mac.translate(str.maketrans("", "", ":-."))

    @staticmethod
    def _set_lettercase(string: str) -> str:
        """determines lettercase for MAC address"""
        return (
            string.lower() if bool(any(c.islower() for c in string)) else string.upper()
        )

    @staticmethod
    def _ins(source: str, insert: str, position: int) -> str:
        """inserts value at a certain position in the source"""
        return source[:position] + insert + source[position:]

    def _build_mac_with_separator(self, mac: str, _format: Format) -> str:
        """builds the type of separator used"""
        if _format == self.Format.HYPHEN:
            return self._ins(
                self._ins(
                    self._ins(self._ins(self._ins(mac, "-", 2), "-", 5), "-", 8),
                    "-",
                    11,
                ),
                "-",
                14,
            )
        if _format == self.Format.COLON:
            return self._ins(
                self._ins(
                    self._ins(self._ins(self._ins(mac, ":", 2), ":", 5), ":", 8),
                    ":",
                    11,
                ),
                ":",
                14,
            )
        if _format == self.Format.PERIOD:
            return self._ins(
                self._ins(
                    self._ins(self._ins(self._ins(mac, ".", 2), ".", 5), ".", 8),
                    ".",
                    11,
                ),
                ".",
                14,
            )
        if _format == self.Format.CISCO:
            return self._ins(self._ins(mac, ".", 4), ".", 9)
        if _format == self.Format.NONE:
            return mac
        if _format == self.Format.UNKNOWN:
            return "mac format unknown"

    def _get_mac_format(self, mac: str) -> str:
        """set the mac format style"""
        if mac.count("-") == 5 and "." not in mac and ":" not in mac:
            return self.Format.HYPHEN
        if mac.count(":") == 5 and "." not in mac and "-" not in mac:
            return self.Format.COLON
        if mac.count(".") == 5 and ":" not in mac and "-" not in mac:
            return self.Format.PERIOD
        if mac.count(".") == 2 and ":" not in mac and "-" not in mac:
            return self.Format.CISCO
        if len(mac) == 12:
            return self.Format.NONE
        if "." not in mac and ":" not in mac and "-" not in mac:
            return self.Format.UNKNOWN
        else:
            return self.Format.NONE

    def _build_random_nic(self, mac: str) -> str:
        """randomize 6-digit NIC portion of a mac"""
        vendor = ""
        random_nic = ""
        for c in mac[:6]:
            vendor += c
        for c in mac[-6:]:
            random_nic += random.choice(self._HEX)
        return vendor + random_nic

    def _build_random_twelve_digit(self) -> str:
        """randomize 12-digit mac"""
        mac = ""
        for number in range(0, 12):
            if number == 1:
                mac += random.choice(self._LOCAL)
            else:
                mac += random.choice(self._HEX)
        return mac


def main() -> None:
    _here = os.path.abspath(os.path.dirname(__file__))

    # load the package's __version__.py module as a dictionary
    _about = {}

    with open(os.path.join(_here, "__version__.py")) as f:
        exec(f.read(), _about)

    arg_parser = _setup_parser(_about)
    args = arg_parser.parse_args()
    if args.mac == "empty":
        arg_parser.print_help()
    else:
        format_mac = args.mac
        if args.full:
            random_mac = RandMac(format_mac, True)
        else:
            random_mac = RandMac(format_mac, False)
        print(random_mac.mac)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(-1)
    sys.exit(0)
