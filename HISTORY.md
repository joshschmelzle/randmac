Release History
===============

0.2.0 (2026-10-21)
------------------

- Require Python 3.13 or newer.
- Invalid MAC addresses now print a short error instead of a traceback.
- `randmac -p` with no MAC address is now an error instead of returning a fully random MAC.
- Output keeps the lettercase of the sample MAC address.
- Use the `secrets` module to generate addresses.
- Add type hints, more tests, and CI on Linux, Windows, and macOS with mypy.
- Publish releases to PyPI from GitHub Actions with Trusted Publishing.

0.0.2 (2023-05-23)
------------------

- Minor bug fixes and fix tests.
- Switch from setup.py to pyproject.toml.
- License change from MIT to BSD-3-Clause.

0.0.1 (2019-02-27)
------------------

- Uploaded to PyPi.

2018-12-19
------------------

- Conception.
