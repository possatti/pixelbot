#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
from PIL import Image

import numpy as np
import argparse
import sys
import re
import os

print(sys.version, file=sys.stderr)

COLORS = [
    (255, 255, 255, 255),
    (228, 228, 228, 255),
    (136, 136, 136, 255),
    (34,  34,  34,  255),
    (255, 167, 209, 255),
    (229, 0,   0,   255),
    (229, 149, 0,   255),
    (160, 106, 66,  255),
    (229, 217, 0,   255),
    (148, 224, 68,  255),
    (2,   190, 1,   255),
    (0,   211, 221, 255),
    (0,   131, 199, 255),
    (0,   0,   234, 255),
    (207, 110, 228, 255),
    (130, 0,   128, 255),
]

def main():
    size = (8, 2)
    img = Image.new('RGBA', size)
    img.putdata(COLORS)
    img.save(args.save_path)

# Arguments and options
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('save_path')
    args = parser.parse_args()
    main()
