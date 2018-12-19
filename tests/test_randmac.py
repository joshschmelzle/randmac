import pytest
import sys

sys.path.insert(0, "../randmac/")
from randmac import randmac


class TestRandMac(object):
    def testrandomnic(self):
        assert len(randmac.nic_portion("00.00.00.00.00.00")) == 17
        assert len(randmac.nic_portion("0000.0000.0000")) == 14
        assert "123456" in randmac.nic_portion("123456AABBCC")

    def testmac(self):
        assert randmac.twelve_digit_mac("00:00:00:00:00:00")[1].lower() in [
            "2",
            "6",
            "a",
            "e",
        ]
        assert randmac.twelve_digit_mac("00.00.00.00.00.00")[1].lower() in [
            "2",
            "6",
            "a",
            "e",
        ]
        assert randmac.twelve_digit_mac("00-00-00-00-00-00")[1].lower() in [
            "2",
            "6",
            "a",
            "e",
        ]
        assert randmac.twelve_digit_mac("0000.0000.0000")[1].lower() in [
            "2",
            "6",
            "a",
            "e",
        ]
        assert randmac.twelve_digit_mac("000000000000")[1].lower() in [
            "2",
            "6",
            "a",
            "e",
        ]
