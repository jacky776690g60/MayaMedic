""" =================================================================
| parser.py -- Python/MayaMedic/utility/parser.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

from typing import *
import math

def normalize_rgb(*args) -> Tuple[float, float, float]:
    """
    Normalize RGB values to a tuple of floats ranging from 0 to 1.

    Params:
    -------
    - *args: RGB values provided either as a single string "R, G, B" or as three separate integers.

    Returns:
    --------
    - Tuple: Normalized RGB values.
        
    Examples:
    ---------
    >>> normalize_rgb("255, 0, 0")  # (1.0, 0.0, 0.0)
    >>> normalize_rgb(0, 128, 255) # (0.0, 0.501..., 1.0)
    """
    if   len(args) == 1 and isinstance(args[0], str):                   rgb = tuple(map(int, args[0].split(',')))
    elif len(args) == 3 and all(isinstance(v, int) for v in args):      rgb = args
    elif all(0 <= v <= 1 for v in args if isinstance(v, (int, float))): return args
    else:
        raise ValueError("RGB values must be provided as a single string 'R, G, B' or as three separate integers.")

    if any(v < 0 or v > 255 for v in rgb):
        raise ValueError("RGB values must be in the range of 0 to 255.")

    normalized_rgb = tuple(v / 255.0 for v in rgb)
    return normalized_rgb


def kelvin_to_rgb(kelvin: float) -> Tuple[float, float, float]:
    # Clamp the temperature in the 1000-40000 range
    temp = kelvin / 100.0
    temp = min(max(temp, 10.0), 400.0)

    # Calculate red
    if temp <= 66.0:
        red = 255
    else:
        red = temp - 60.0
        red = 329.698727446 * (red ** -0.1332047592)
        red = min(max(red, 0), 255)

    # Calculate green
    if temp <= 66.0:
        green = temp
        green = 99.4708025861 * math.log(green) - 161.1195681661
    else:
        green = temp - 60.0
        green = 288.1221695283 * (green ** -0.0755148492)
    green = min(max(green, 0), 255)

    # Calculate blue
    if temp >= 66.0:
        blue = 255
    elif temp <= 19.0:
        blue = 0
    else:
        blue = temp - 10.0
        blue = 138.5177312231 * math.log(blue) - 305.0447927307
        blue = min(max(blue, 0), 255)

    return normalize_rgb(int(red), int(green), int(blue))