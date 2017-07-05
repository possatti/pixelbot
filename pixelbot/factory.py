from __future__ import print_function, division
from string import Template

import math
import sys
import re

class Point:
    """Represents a pixel that will be painted."""
    def __init__(self, x, y, color=4):
        self.x = x
        self.y = y
        self.color = color
    def __str__(self):
        return '{{x:{x}, y:{y}, color:{color}}}'.format(**self.__dict__)

COLORS = [
    (255, 255, 255),
    (228, 228, 228),
    (136, 136, 136),
    (34,  34,  34),
    (255, 167, 209),
    (229, 0,   0),
    (229, 149, 0),
    (160, 106, 66),
    (229, 217, 0),
    (148, 224, 68),
    (2,   190, 1),
    (0,   211, 221),
    (0,   131, 199),
    (0,   0,   234),
    (207, 110, 228),
    (130, 0,   128),
]

def parse_text_file(file_path):
    """Parse a text file into a list of points to paint on pixelcanvas.io."""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    points = []
    for row, line in enumerate(lines):
        for col, character in enumerate(line):
            try:
                color = int(character)
                points.append(Point(col, row, color))
            except:
                pass

    return points

def parse_image_file(image_path):
    """Parse an image into a list of points to paint on pixelcanvas.io."""

    from PIL import Image
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print('File \'{}\' does not exist.'.format(image_path), file=sys.stderr)
    image_data = image.getdata()
    print('Parsing image \'{}\' with resolution {}x{}.'.format(image_path, image.width, image.height), file=sys.stderr)

    # Iterate through each pixel, build a equivalent point.
    points = []
    for y in range(image.height):
        for x in range(image.width):
            # Use a fancy index, because all pixels are in a single array.
            i = x + y*image.width
            pixel = image_data[i]

            # Only use this pixel if it is not transparent.
            if pixel[3] != 0:
                # Here comes a the trick part. We consider the RGB, as a 3D space.
                # and calculate the euclidean distance from the pixel's color,
                # and each of the avaiable colors. We do this, so that we find
                # the best color to represent that pixel (since we have a limited
                # color pallete).
                minimum_distance = 256**3
                for color_index, color in enumerate(COLORS):
                    distance = math.sqrt((pixel[0] - color[0])**2 + (pixel[1] - color[1])**2 + (pixel[2] - color[2])**2)
                    if distance < minimum_distance:
                        minimum_distance = distance
                        best_color = color_index
                points.append(Point(x, y, best_color))
    return points

def produce_bot(points, ox, oy, fingerprint, template_path, save_path):
    """Use the bot template to produce bot ready for use."""

    # Prepare template.
    with open(template_path) as f:
        lines = f.readlines()
    template = Template(''.join(lines))
    print('Using template from `{}`.'.format(template_path), file=sys.stderr)

    # Join points on a single string.
    points_string = ''
    for point in points:
        points_string += str(point) + ', '

    # Produce and save the bot.
    bot_content = template.substitute(
        points=points_string,
        ox=ox, oy=oy,
        fingerprint=fingerprint)
    with open(save_path, 'w') as f:
        f.write(bot_content)


def create(file_path, ox, oy, fingerprint, template_path, save_path):
    print('Parsing file...', file=sys.stderr)
    if file_path.endswith('.txt'):
        points = parse_text_file(file_path)
    elif re.match(r'.*\.(png|bmp|jpg|jpeg|gif)$', file_path):
        points = parse_image_file(file_path)
    else:
        print('Can\'t produce any bot from \'{}\'. '.format(file_path), file=sys.stderr)
        exit(1)
    print('Number of points produced: {}.'.format(len(points)), file=sys.stderr)

    # Create and save the bot.
    print('Saving bot to \'{}\'...'.format(save_path), file=sys.stderr)
    produce_bot(points, ox, oy, fingerprint, template_path, save_path)
    print('All done.', file=sys.stderr)
