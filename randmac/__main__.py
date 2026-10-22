# /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  _ _  _  _| _ _  _  _
# | (_|| |(_|| | |(_|(_
#

import sys

from . import __version__ as about
from .helpers import _setup_parser
from .randmac import RandMac


def main(argv: list[str] | None = None) -> int:
    """Set up args and print a random mac address"""
    arg_parser = _setup_parser(
        {"__author__": about.__author__, "__version__": about.__version__}
    )
    args = arg_parser.parse_args(argv)
    if args.mac is None:
        if args.partial:
            arg_parser.error(
                "--partial needs a MAC address to keep the vendor (OUI) portion from"
            )
        print(RandMac("00:00:00:00:00:00", False).mac)
        return 0
    try:
        random_mac = RandMac(args.mac, args.partial)
    except ValueError as error:
        arg_parser.error(str(error))
    print(random_mac.mac)
    return 0


def init() -> None:
    """Handle main init"""
    if __name__ == "__main__":
        sys.exit(main())


init()
