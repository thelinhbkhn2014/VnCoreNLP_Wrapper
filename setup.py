#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import re
from os import path

from setuptools import find_packages, setup


PACKAGE_NAME = "py_vncorenlp"
here = path.abspath(path.dirname(__file__))

with io.open("%s/__init__.py" % PACKAGE_NAME, "rt", encoding="utf8") as f:
    version = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
]

setup(
    name="py_vncorenlp",
    version=version,
    description="A Python Wrapper for VnCoreNLP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/thelinhbkhn2014/VnCoreNLP_Wrapper',
    author="Linh The Nguyen",
    author_email="toank45sphn@gmail.com",
    maintainer="linhthenguyen",
    maintainer_email="toank45sphn@gmail.com",
    classifiers=classifiers,
    keyword="vncorenlp",
    packages=find_packages(),
    install_requires=["pyjnius"],
    python_requires=">=3.6",
)