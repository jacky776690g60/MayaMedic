"""
contains utilities for transform node
"""
""" =================================================================
| transform.py -- Python/MayaMedic/utility/transform.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """
from typing import *

import maya.cmds as cmds

from utility.parser import normalize_rgb
from nodes.camera import Camera

def create_colored_group(
    group_name: str, 
    nRGB:       Tuple[float, float, float],
    *objects:   str
) -> str:
    """
    Create a colored group in Autodesk Maya and parent the specified objects to it

    Params:
    -------
    - `group_name`: The name of the new group to be created.
    - `nRGB`:       A tuple representing the *normalized* RGB (ranging from 0 to 1)
    - `*objects`:   An arbitrary number of Maya objects (str) to be parented to the group.

    Example:
    --------
    >>> create_colored_group("myGroup", (1, 0, 0), "cube1", "sphere1")
    'myGroup'
    """
    # Create a new empty group
    group = cmds.group(em=True, name=group_name)
    
    # Add objects to the group
    if objects:
        for obj in objects: cmds.parent(obj, group)
            
    nRGB = normalize_rgb(*nRGB)
    
    # Set the group color
    cmds.setAttr(group + ".useOutlinerColor", True)
    cmds.setAttr(group + ".outlinerColor",    nRGB[0], nRGB[1], nRGB[2])
    return group

    