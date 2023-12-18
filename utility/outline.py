"""
functions related to selection and outline
"""

""" =================================================================
| outline.py -- Python/MayaMedic/utility/outline.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """


import importlib
from typing import *

import maya.cmds as cmds

from components import polygon
importlib.reload(polygon)


class SelectionNotFoundError(Exception):
    def __init__(self, selection_name: str, message: str=None):
        self.message = message if message else f"No selection found in Maya: {selection_name}"
        super().__init__(self.message)


# =============================
# Objects
# =============================
def selected_objects() -> List[str]:
    "get all kinds of objects"
    return cmds.ls(selection=True, long=True)




# =============================
# selection
# =============================
def get_parents(obj_path: str) -> str | None:
    '''
    Examples:
    ---------
    >>> otl.get_parents('aiAreaLight1')
    '''
    parent = cmds.listRelatives(obj_path, parent=True, fullPath=True)
    return parent[0] if parent else None


def parent_to(child: str, parent: str):
    cmds.parent(child, parent, add=True, shape=True)


# =============================
# Freeze
# =============================
def freeze_all(obj_path: str):
    cmds.makeIdentity(
        obj_path, 
        apply=True, 
        translate=True, rotate=True, scale=True, 
        normal=False, preserveNormals=True
    )




# =============================
# Components
# =============================
def selected_components() -> List[str]:
    return cmds.ls(selection=True, flatten=True)

def filter_expand(selection_mask: int) -> List[str]:
    return cmds.filterExpand(selected_components(), selectionMask=selection_mask, expand=True) or []

def get_selected_components(component_type: str, selection_mask: int) -> List[str]:
    selected = filter_expand(selection_mask)
    if not selected:
        raise SelectionNotFoundError(component_type)
    return selected

def selected_polygons() -> List[polygon.Polygons]:
    "Get selected polygons"
    # return get_selected_components("polygons", 12)
    return [polygon.Polygons(s) for s in get_selected_components("polygons", 12)]

def selected_vertices() -> List[str]:
    "Get selected polygon vertices"
    return get_selected_components("vertices", 31)

def selected_edges() -> List[str]:
    "Get selected polygon edges"
    return get_selected_components("edges", 32)

def selected_faces():
    "Get selected polygon faces"
    return [polygon.Face(s) for s in get_selected_components("faces", 34)]

def selected_UVs() -> List[str]:
    "Get selected polygon UVs"
    return get_selected_components("UVs", 35)

