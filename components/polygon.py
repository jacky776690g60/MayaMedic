""" =================================================================
| polygon.py -- Python/MayaMedic/components/polygon.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

import maya.cmds as cmds

from .base import BaseComponent

class Face(BaseComponent):
    "A polygon face"
    def __init__(self, specifier: str) -> None:
        super().__init__(specifier)

    # =============================
    # functions
    # =============================
    def delete(self):
        cmds.delete(self.name)
        
    
class Polygons(BaseComponent):
    "A polygons object"
    
    def __init__(self, specifier: str) -> None:
        shapes = cmds.listRelatives(specifier, allDescendents=True, shapes=True, fullPath=True) or []
        
        if not any(cmds.objectType(shape, isType='mesh') for shape in shapes):
            raise ValueError("Object is not a polygonal mesh: {}".format(specifier))
        
        super().__init__(specifier)
                
    @property
    def area(self):
        "Calculate and return the total surface area of the polygonal object."
        face_areas = cmds.polyEvaluate(self.name, area=True)
        if face_areas is None:
            raise RuntimeError("Failed to calculate face areas. Ensure the object is a valid polygonal mesh.")
        return face_areas
    
    
    def apply_smooth(self, divisions: int, wipe_history=True):
        "Apply a smoothing operation (history) to the polygonal mesh."
        if divisions < 0:
            raise ValueError("Divisions must be a non-negative integer.")
        
        history = cmds.polySmooth(self.name, dv=divisions)
        
        if wipe_history:
            cmds.delete(self.name, constructionHistory=True)
            # cmds.delete(history)
        
        