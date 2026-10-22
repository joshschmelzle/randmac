# /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  _ _  _  _| _ _  _  _
# | (_|| |(_|| | |(_|(_
#

"""
Generates a 12-digit LAA MAC address

Optional argument will generate 6 digit NIC portion of the MAC address.

Supported MAC address formats:
    MM:MM:MM:SS:SS:SS
    MM-MM-MM-SS-SS-SS
    MM.MM.MM.SS.SS.SS
    MMMM.MMSS.SSSS
    MMMMMMSSSSSS
"""

import secrets
from enum import Enum


class RandMac(object):  # pylint: disable=too-few-public-methods
    """A random MAC address in the same format as a sample MAC address"""

    # second hex digit of a locally administered, unicast address
    _LOCAL = ["2", "6", "a", "e"]

    _HEX = "0123456789abcdef"

    class Format(Enum):
        """type of MAC address formats"""

        HYPHEN = 1
        COLON = 2
        PERIOD = 3
        CISCO = 4
        NONE = 5
        UNKNOWN = 6

    def __init__(
        self, mac: str | None = None, generate_partial: bool | None = None
    ) -> None:
        if mac is None:
            mac = "11:11:11:11:11:11"
        uppercase = self._is_uppercase(mac)
        mac = mac.lower()
        trimmed = self._trim_separator(mac)
        _chars = [_char for _char in trimmed if _char not in self._HEX]
        if _chars:
            raise ValueError("Invalid characters in MAC format {}".format(_chars))
        if len(trimmed) != 12:
            raise ValueError("MAC must be 12 digits but found {}".format(len(trimmed)))

        _format = self._get_mac_format(mac)

        if generate_partial:
            not_formatted = self._build_random_nic(trimmed)
        else:
            not_formatted = self._build_random_twelve_digit()
        if uppercase:
            not_formatted = not_formatted.upper()
        self.mac = self._build_mac_with_separator(not_formatted, _format)

    def __repr__(self) -> str:
        return repr(str(self.mac))

    def __str__(self) -> str:
        return str(self.mac)

    def __getitem__(self, item: int | slice) -> str:
        return str(self.mac)[item]

    def __len__(self) -> int:
        return len(str(self.mac))

    @staticmethod
    def _trim_separator(mac: str) -> str:
        """removes separator from MAC address"""
        return mac.replace(":", "").replace("-", "").replace(".", "")

    @staticmethod
    def _is_uppercase(mac: str) -> bool:
        """True when the sample MAC uses uppercase hex letters and no lowercase ones"""
        return any(c.isupper() for c in mac) and not any(c.islower() for c in mac)

    @staticmethod
    def _split(mac: str, size: int) -> list[str]:
        return [mac[i : i + size] for i in range(0, len(mac), size)]

    def _build_mac_with_separator(self, mac: str, _format: Format) -> str:
        """builds the type of separator used"""
        if _format == self.Format.HYPHEN:
            return "-".join(self._split(mac, 2))
        if _format == self.Format.COLON:
            return ":".join(self._split(mac, 2))
        if _format == self.Format.PERIOD:
            return ".".join(self._split(mac, 2))
        if _format == self.Format.CISCO:
            return ".".join(self._split(mac, 4))
        if _format == self.Format.NONE:
            return mac
        return "mac format unknown"

    def _get_mac_format(self, mac: str) -> Format:
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
        return self.Format.NONE

    def _build_random_nic(self, mac: str) -> str:
        """randomize 6-digit NIC portion of a mac"""
        return mac[:6] + "".join(secrets.choice(self._HEX) for _ in range(6))

    def _build_random_twelve_digit(self) -> str:
        """randomize 12-digit mac"""
        return "".join(
            secrets.choice(self._LOCAL) if number == 1 else secrets.choice(self._HEX)
            for number in range(12)
        )
