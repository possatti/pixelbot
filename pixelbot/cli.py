#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division
from pixelbot.factory import create

import argparse
import sys
import re
import os

print(sys.version, file=sys.stderr)

def main():
    default_template_location = os.path.realpath(os.path.join(os.path.dirname(__file__), 'bot_templates', 'pixelbot-fetch-template.js'))
    # Arguments and options fot the CLI.
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('file_path', help='The file indicating what should be built by the robot. It can be an image or a text file.')
    parser.add_argument('x_offset', type=int, help='X coordinate for where in the canvas the drawing should be painted.')
    parser.add_argument('y_offset', type=int, help='Y coordinate for where in the canvas the drawing should be painted.')
    parser.add_argument('fingerprint', help='Your fingerprint.')
    parser.add_argument('-t', '--bot-template', default=default_template_location, help='Location do the template which will produce the bot.')
    parser.add_argument('-s', '--save-to', metavar='file_path', dest='save_path', help='Where the bot script should be saved to. Defaults to <file_path> terminating with `.js`.')
    args = parser.parse_args()

    # Decide where to save the bot to.
    if args.save_path:
        bot_save_path = args.save_path
    else:
        bot_save_path = re.sub(r'\.\w+$', '.js', args.file_path)

    create(args.file_path, args.x_offset, args.y_offset,
        args.fingerprint, args.bot_template, bot_save_path)


if __name__ == '__main__':
    main()
