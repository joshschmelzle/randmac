# /usr/bin/env python3
# -*- coding: utf-8 -*-

import re

import pytest

from randmac import __version__ as about
from randmac.__main__ import main


def run(capsys, *args):
    assert main(list(args)) == 0
    return capsys.readouterr().out.strip()


def test_default_is_laa_unicast_colon(capsys):
    mac = run(capsys)
    assert re.fullmatch(r"[0-9a-f]{2}(:[0-9a-f]{2}){5}", mac)
    first = int(mac[:2], 16)
    assert first & 0b10 and not first & 0b01


@pytest.mark.parametrize(
    "sample, pattern",
    [
        ("00-11-22-33-44-55", r"[0-9a-f]{2}(-[0-9a-f]{2}){5}"),
        ("0011.2233.4455", r"[0-9a-f]{4}(\.[0-9a-f]{4}){2}"),
        ("001122334455", r"[0-9a-f]{12}"),
    ],
)
def test_output_matches_sample_format(capsys, sample, pattern):
    assert re.fullmatch(pattern, run(capsys, sample))


def test_partial_keeps_vendor(capsys):
    mac = run(capsys, "-p", "12:34:56:aa:bb:cc")
    assert mac.startswith("12:34:56:")
    assert len(mac) == 17


def test_partial_without_mac_is_an_error(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["-p"])
    assert exc.value.code == 2
    assert "--partial needs a MAC address" in capsys.readouterr().err


@pytest.mark.parametrize("bad", ["zz", "00:11:22:33:44", "00:11:22:33:44:5g"])
def test_invalid_mac_is_a_clean_error(capsys, bad):
    with pytest.raises(SystemExit) as exc:
        main([bad])
    assert exc.value.code == 2
    err = capsys.readouterr().err
    assert "Traceback" not in err
    assert "randmac: error:" in err


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert capsys.readouterr().out.strip() == f"randmac {about.__version__}"
