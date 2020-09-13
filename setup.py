# -*- coding: utf-8 -*-

import sys
import os
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# 'setup.py publish' shortcut.
if sys.argv[-1] == "build":
    os.system("python setup.py sdist bdist_wheel")
    sys.exit()

# load the package's __version__.py module as a dictionary
about = {}
with open(os.path.join(here, "randmac", "__version__.py")) as f:
    exec(f.read(), about)

try:
    with open("README.md", "r") as f:
        readme = f.read()
except FileNotFoundError:
    long_description = about["__description__"]

requires = []

# Magic here:
setup(
    name=about["__title__"],
    version=about["__version__"],
    packages=find_packages(exclude=("tests",)),
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    python_requires=">3.2,",
    install_requires=requires,
    url=about["__url__"],
    entry_points={"console_scripts": ["randmac=randmac.__main__:main"]},
    keywords=["randmac", "random mac", "random mac address"],
    license=about["__license__"],
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.2",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Utilities",
    ],
)
