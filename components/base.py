""" =================================================================
| base.py -- Python/MayaMedic/components/base.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

import maya.cmds as cmds

class BaseComponent():
    "Absolute base component"
    def __init__(self, specifier: str) -> None:
        if not isinstance(specifier, str):
            raise ValueError("Specifier must be a string: {}".format(self.specifier))
        
        if not cmds.objExists(specifier):
            raise ValueError("Object does not exist in the scene: {}".format(self.specifier))
        
        self.specifier = specifier
        "example: `'pCube[0].f[0]'`"
        
    @property
    def name(self):
        "Same as `self.specifier`"
        return self.specifier