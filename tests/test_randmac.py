# /usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  _ _  _  _| _ _  _  _
# | (_|| |(_|| | |(_|(_
#

import sys

sys.path.insert(0, "../randmac/")
from randmac import RandMac


class Test_RandMac(object):
    def test_partial(self):
        assert len(RandMac("000000000000", generate_partial=True)) == 12
        assert len(RandMac("00.00.00.00.00.00", generate_partial=True)) == 17
        assert len(RandMac("00-00-00-00-00-00", generate_partial=True)) == 17
        assert len(RandMac("00:00:00:00:00:00", generate_partial=True)) == 17
        assert len(RandMac("0000.0000.0000", generate_partial=True)) == 14
        assert "123456" in str(RandMac("123456AABBCC", generate_partial=True))
        assert "12:34:56" in str(RandMac("12:34:56:AA:BB:CC", generate_partial=True))

    def test_mac(self):
        laa_hex = [
            "2",
            "6",
            "a",
            "e",
        ]
        assert "123456" not in RandMac("123456AABBCC")
        assert "12:34:56" not in RandMac("12:34:56:AA:BB:CC")
        assert RandMac("00:00:00:00:00:00")[1].lower() in laa_hex
        assert RandMac("00.00.00.00.00.00")[1].lower() in laa_hex
        assert RandMac("00-00-00-00-00-00")[1].lower() in laa_hex
        assert RandMac("0000.0000.0000")[1].lower() in laa_hex
        assert RandMac("000000000000")[1].lower() in laa_hex
