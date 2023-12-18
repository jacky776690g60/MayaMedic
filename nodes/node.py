""" =================================================================
| node.py -- Python/MayaMedic/nodes/node.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

from typing import *
from enum import Enum, auto

import maya.cmds as cmds

LJUST = 15


class __AutoName(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name


class NodeNames(__AutoName):
    '''
    Possible maya node names
    
    Examples:
    ---------
    >>> cmds.createNode(nd.NodeNames.nCloth.name, name="name" + 'Shape')
    
    '''
    # Transform
    transform   = auto()
    joint       = auto()
    # Shape Nodes: These nodes are usually children of transform nodes and represent geometric shapes.
    mesh         = auto()
    nurbsCurve   = auto()
    nurbsSurface = auto()
    subdiv       = auto()
    # Maya Light
    directionalLight = auto()
    pointLight       = auto()
    spotLight        = auto()
    areaLight        = auto()
    volumeLight      = auto()
    ambientLight     = auto()
    # Arnold
    aiAreaLight         = auto()
    aiMeshLight         = auto()
    aiPhotometricLight  = auto()
    aiSkyDomeLight      = auto()
    aiLightPortal       = auto()
    aiPhysicalSky       = auto()
    #
    aiStandardSurface   = auto()
    # camera
    camera = auto()
    # maya material
    lambert         = auto()
    blinn           = auto()
    phong           = auto()
    surfaceShader   = auto()
    # Dynamics and Simulation Nodes
    particle    = auto()
    fluidShape  = auto()
    nCloth      = auto()
    nRigid      = auto()





class MayaNode:
    '''Maya Base Node'''
    
    def __init__(self, name:str, transform: str, shape: str, verbose=False) -> None:
        self.transform   = transform
        self.shape       = shape
        
        if verbose:
            print(f"[CREATED] Node: {name:<{LJUST}} | Transform: {self.transform:<{LJUST}} | Shape: {self.shape:<{LJUST}}")
    
    
    def hide(self) -> None:
        cmds.hide(self.transform)
        
    def move(self, position: Tuple[float, float, float]) -> None:
        cmds.move(*position, self.transform)
    
    def rotate(self, rotation: Tuple[float, float, float]) -> None:
        cmds.rotate(*rotation, self.transform)
        
    
    def connetAttr(self, attr: str, kTransform: str, kattr: str, nextAvailable=True):
        cmds.connectAttr(
            f"{self.transform}.{attr}",
            f"{kTransform}.{kattr}",
            nextAvailable=nextAvailable
        )
        
        
    def disconnectAttr(self):
        raise NotImplementedError()