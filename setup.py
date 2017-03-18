#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
    author="Diogo Fernandes",
    author_email="diogoabfernandes@gmail.com",
    description="A Python DNS crawler for finding indentical domain names under different TLDs",
    name="domfind",
    version="1.0",
    license="see LICENSE",
    packages=find_packages(),
    scripts=["domfind"],
    url="https://github.com/diogo-fernan/domfind",
)
