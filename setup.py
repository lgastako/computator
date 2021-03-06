#!/usr/bin/env python

import os
from setuptools import setup
from setuptools import find_packages


if __name__ == "__main__":
    setup(name="computator",
          version="0.0.1",
          description="Graph-alike.",
          author="John Evans",
          author_email="lgastako@gmail.com",
          url="https://github.com/lgastako/computator",
          packages=find_packages(),
          provides=["computator"])
