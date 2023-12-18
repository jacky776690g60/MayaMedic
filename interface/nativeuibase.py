""" =================================================================
| nativeuibase.py -- Python/MayaMedic/interface/nativeuibase.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

from typing import *
from abc import ABC, abstractclassmethod

import maya.cmds as cmds

# ======================================================================
# Base
# ======================================================================
class UIBase(ABC):
    ''' Base class for controlling maya UI (`except window`)'''
    _class_command = None
    
    "Base for native UI class"
    def __init__(self, name: str | None = None) -> None:
        self.name = name
        
    def __del__(self):
        # NOTE: Don't use this because it will go out of scope even if the window is not closed by user
        # if self._class_command(self.name, exists=True):
        #     cmds.deleteUI(self.name)
        ...
    
    def __repr__(self) -> str:
        return self.name
    
    def __str__(self) -> str:
        return self.name
    
    # =============================
    # Getters & setters & Properties
    # =============================
    @property
    def annotation(self):
        return self._class_command(self.name, query=True, annotation=True)
    @annotation.setter
    def annotation(self, ann: str):
        self._class_command(self.name, edit=True, annotation=ann)
    
    
    @property
    def width(self) -> float:
        # TODO: testing
        return self._class_command(self.name, query=True, width=True)
    @width.setter
    def width(self, width: float):
        self._class_command(self.name, edit=True, width=width)


    @property
    def height(self) -> float:
        # TODO: testing
        return self._class_command(self.name, query=True, height=True)
    @height.setter
    def height(self, height: float):
        self._class_command(self.name, edit=True, height=height)

    @property
    def fullPathName(self) -> str:
        return self._class_command(self, query=True, fullPathName=True)
    
    
    def exists(self) -> bool:
        return self._class_command(self.name, exists=True)
    
    
    def isObscured(self) -> bool:
        '''
        Return whether the control can actually be seen by the user. The 
        control will be obscured if its state is invisible, if it is blocked
        (entirely or partially) by some other control, if it or a parent 
        layout is unmanaged, or if the control's window is invisible 
        or iconified.
        '''
        #TODO: testing
        return self._class_command(self.name, query=True, isObscured=True)
    
    
    # =============================
    # functions
    # =============================
    def setParent(self, parent_name: str):
        self._class_command(self.name, edit=True, parent=parent_name)
    
    def setBackgroundColor(self, nRGB: Tuple[float, float, float]):
        self._class_command(self.name, edit=True, bgc=nRGB)
        
    def setSize(self, width: int, height: int):
        self._class_command(self.name, edit=True, width=width, height=height)    
        


# ======================================================================
# Layouts
# ======================================================================
class Layout(UIBase):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        
    def __repr__(self) -> str:
        return super().__repr__()
    
    @property
    def childArray(self) -> List[str]:
        return self._class_command(self, query=True, childArray=True)


# ======================================================================
# Sliders
# ======================================================================    
class AttributeSlider(UIBase):
    def __init__(self, 
        name: str, 
        attr: str
    ) -> None:
        ''''''
        super().__init__(name)
        self.attribute = attr


    def set_value_change_callback(self, callback: Callable) -> None:
        '''
        Register a callback function that gets called when the color changes.
        '''
        cmds.scriptJob(
            attributeChange = [self.attribute, callback], 
            parent          = self
        )
    
    # =============================
    # Getters & Setters
    # =============================   
    @property
    def value(self) -> Union[float, Tuple[float, ...]]:
        return cmds.getAttr(self.attribute)
    
    
    @property
    def isEnabled(self) -> bool:
        return self._class_command(self.name, query=True, enable=True)
    @isEnabled.setter
    def isEnabled(self, enable: bool):
        self._class_command(self.name, edit=True, enable=enable)
    
