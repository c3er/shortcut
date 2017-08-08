#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

import config


def debug(*args, sep=" ", end="\n"):
    if config.debug:
        print(*args, sep=sep, end=end)


def getdirpath(file):
    return os.path.dirname(os.path.realpath(file))
