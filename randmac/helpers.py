# /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  _ _  _  _| _ _  _  _
# | (_|| |(_|| | |(_|(_
#

import argparse
import textwrap


def _setup_parser(_about: dict) -> argparse:
    """Setup parser for arguments passed in from the CLI.

    Returns:
      argparse object.
    """
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """
            Generates MAC addresses. By default randmac will generate a 12-digit
            MAC address following the Locally Administrated Address (LAA) format.
            randmac only supports 12-digit (48-bit) MAC addresses.
            """
        ),
        epilog="Made with Python by {}".format(_about["__author__"]),
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "mac", nargs="?", default="empty", help="mac address required for output format"
    )
    parser.add_argument(
        "-p",
        "--partial",
        action="store_true",
        help="randomizes the NIC portion of a MAC address",
    )
    parser.add_argument(
        "-v",
        "-V",
        "--version",
        action="version",
        version="%(prog)s {}".format(_about["__version__"]),
    )
    return parser
