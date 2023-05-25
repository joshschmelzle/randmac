# /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  _ _  _  _| _ _  _  _
# | (_|| |(_|| | |(_|(_
#

import os
import platform
import sys

from .randmac import RandMac
from .helpers import _setup_parser


def main():
    """ Set up args and retrieve a random mac address """
    _here = os.path.abspath(os.path.dirname(__file__))

    # load the package's __version__.py module as a dictionary
    _about = {}

    with open(os.path.join(_here, "__version__.py")) as f:
        exec(f.read(), _about)

    arg_parser = _setup_parser(_about)
    args = arg_parser.parse_args()
    if args.mac == "empty":
        random_mac = RandMac("00:00:00:00:00:00", False)
        print(random_mac.mac)
    else:
        format_mac = args.mac
        if args.partial:
            random_mac = RandMac(format_mac, True)
        else:
            random_mac = RandMac(format_mac, False)
        print(random_mac.mac)


def init() -> None:
    """ Handle main init """
    if __name__ == "__main__":
        sys.exit(main())


init()
