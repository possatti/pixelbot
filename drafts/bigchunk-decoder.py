#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import argparse
import sys
import re
import os

print(sys.version, file=sys.stderr)

"""
https://github.com/pixelcanvasio/timelapse-bot
"""

colors = [
    (255, 255, 255),
    (228, 228, 228),
    (136, 136, 136),
    (34, 34, 34),
    (255, 167, 209),
    (229, 0, 0),
    (229, 149, 0),
    (160, 106, 66),
    (229, 217, 0),
    (148, 224, 68),
    (2, 190, 1),
    (0, 211, 221),
    (0, 131, 199),
    (0, 0, 234),
    (207, 110, 228),
    (130, 0, 128),
]

def main():
    with open(args.bigchunk_path, 'rb') as f:
        all_bytes = f.read()

    numbers = []
    for byte in all_bytes:
        numbers.append(byte >> 4)
        numbers.append(byte & 0x0F)

    rgbs = list(map(lambda n: colors[n], numbers))

    # sequential_pixels = []
    # for i, rgb in enumerate(rgbs):
    #   pass


    # Record everything on an image. I need proof that this works!
    img = Image.new('RGB', (960,960))
    img.putdata(rgbs)
    img.save('0.0-bigchunk.png')

# Arguments and options
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('bigchunk_path')
    args = parser.parse_args(['/home/possatti/0.0.bmp'])
    main()