""" =================================================================
| camera.py -- Python/MayaMedic/nodes/camera.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """
from typing import *

import maya.cmds as cmds

import utility.general as gen
from .node import MayaNode
from utility.parser import normalize_rgb



class Camera(MayaNode):
    ''' A maya camera '''
    
    def __init__(self, 
        name:               str, 
        is_orthographic:    bool                        = False,
        parent_name:        str                         = None,
        position:           Tuple[float, float, float]  = None, 
        rotation:           Tuple[float, float, float]  = (0, 0, 0), 
    ):
        if gen.objExists(name): print(f"{name} already exists, using a different name.")
        self.camera, self.camera_shape = cmds.camera(name=name, orthographic=is_orthographic)
        super().__init__(transform=self.camera, shape=self.camera_shape)
    
        if parent_name: cmds.parent(self.camera, parent_name)
    
        print(f"Created camera: {self.camera} | with shape: {self.camera_shape}")
        
        if position: self.position = position
        if rotation: self.rotation = rotation
        
    

    # =============================
    # Properties getters & setters
    # =============================
    # ~~~~~~~~ transform ~~~~~~~~
    @property
    def position(self) -> Tuple[float, float, float]:
        return tuple(cmds.xform(self.camera, query=True, worldSpace=True, translation=True))
    @position.setter
    def position(self, position: Tuple[float, float, float]):
        cmds.move(position[0], position[1], position[2], self.camera)


    @property
    def rotation(self) -> Tuple[float, float, float]:
        return tuple(cmds.xform(self.camera, query=True, worldSpace=True, rotation=True))
    @rotation.setter
    def rotation(self, rotation: Tuple[float, float, float]):
        cmds.rotate(rotation[0], rotation[1], rotation[2], self.camera)

    # ~~~~~~~~ cam properties ~~~~~~~~
    @property
    def focalLength(self) -> float:
        return cmds.getAttr(self.camera_shape+'.focalLength')
    @focalLength.setter
    def focalLength(self, focal_length: float):
        return cmds.setAttr(self.camera_shape+'.focalLength', focal_length)
    
    
    @property
    def has_depthOfField(self) -> bool:
        """Enabling this will introduce more computational complexity"""
        return cmds.getAttr(self.camera_shape+'.depthOfField')
    @has_depthOfField.setter
    def has_depthOfField(self, value: bool):
        return cmds.setAttr(self.camera_shape+'.depthOfField', value)
    
    
    @property
    def focusDistance(self) -> float:
        "control where the camera should focus. If objects not in range, blurred"
        return cmds.getAttr(self.camera_shape+'.focusDistance')
    @focusDistance.setter
    def focusDistance(self, focusDistance: float):
        return cmds.setAttr(self.camera_shape+'.focusDistance', focusDistance)
    
    
    @property
    def fStop(self) -> float:
        "aperture"
        return cmds.getAttr(self.camera_shape+'.fStop')
    @fStop.setter
    def fStop(self, fStop: float):
        return cmds.setAttr(self.camera_shape+'.fStop', fStop)
    
    
    @property
    def is_orthographic(self) -> bool:
        return cmds.getAttr(self.camera_shape+'.orthographic')
    @is_orthographic.setter
    def is_orthographic(self, value: bool):
        return cmds.setAttr(self.camera_shape+'.orthographic', value)
    
    
    @property
    def orthographicWidth(self) -> float:
        return cmds.getAttr(self.camera_shape+'.orthographicWidth')
    @orthographicWidth.setter
    def orthographicWidth(self, value: float):
        return cmds.setAttr(self.camera_shape+'.orthographicWidth', value)