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


class Test_RandMac_More(object):
    def test_laa_unicast_bits(self):
        for _ in range(500):
            first = int(str(RandMac())[:2], 16)
            assert first & 0b10, "locally administered bit must be set"
            assert not first & 0b01, "multicast bit must be clear"

    def test_partial_keeps_whole_oui(self):
        for _ in range(100):
            assert str(RandMac("ab:cd:ef:00:00:00", True)).startswith("ab:cd:ef:")

    def test_lettercase_follows_sample(self):
        upper = str(RandMac("AA:BB:CC:DD:EE:FF", True))
        assert upper.startswith("AA:BB:CC:")
        assert upper == upper.upper()
        lower = str(RandMac("aa:bb:cc:dd:ee:ff", True))
        assert lower == lower.lower()
        default = str(RandMac())
        assert default == default.lower()

    def test_cisco_and_period_formats(self):
        cisco = str(RandMac("0000.0000.0000"))
        assert [len(p) for p in cisco.split(".")] == [4, 4, 4]
        period = str(RandMac("00.00.00.00.00.00"))
        assert [len(p) for p in period.split(".")] == [2] * 6

    def test_invalid_input_raises_value_error(self):
        import pytest

        with pytest.raises(ValueError, match="Invalid characters"):
            RandMac("zz:zz:zz:zz:zz:zz")
        with pytest.raises(ValueError, match="12 digits"):
            RandMac("00:11:22")

    def test_default_sample_and_dunder_methods(self):
        mac = RandMac()
        assert len(mac) == 17
        assert mac[2] == ":"
        assert repr(mac) == repr(str(mac))
