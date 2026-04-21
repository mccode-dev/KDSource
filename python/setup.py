#!/usr/bin/env python3

"""KDSource installer script using setuptools.
"""

import os
import re

import setuptools
from setuptools import find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

# Get long description from README
with open(os.path.join(HERE, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Get version
with open(
    os.path.join(HERE, "kdsource/__init__.py"), encoding="utf-8"
) as file:
    VERSION = re.search(r"__version__ = \"(.*?)\"", file.read()).group(1)


setuptools.setup(
    name="kdsource",
    version=VERSION,
    author="Osiris Inti Abbate",
    author_email="intiabbate@gmail.com",
    description="Python API for KDSource package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/inti-abbate/KDSource",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License ::",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "numpy",
        "scipy",
        "matplotlib",
        "KDEpy",
        "joblib",
        "scikit-learn",
        "mcpl",
        "Pillow",
        "astropy",
        "h5py",
        "pandas",
        "uncertainties"
    ],
    python_requires=">=3.6",
    extras_require={
        "docs": [
            "sphinx",
            "sphinxcontrib-katex",
            "sphinx-numfig",
            "jupyter",
            "sphinxcontrib-svg2pdfconverter",
            "sphinx-rtd-theme",
        ],
        "test": ["pytest"],
    },
)
