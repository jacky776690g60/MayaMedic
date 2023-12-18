""" =================================================================
| nativegui.py -- Python/MayaMedic/interface/nativegui.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

import os, pathlib, re, importlib
from typing import *
from typing import Optional
from enum import Enum

import maya.cmds as cmds
import maya.utils as utils

import utility.general as gen
importlib.reload(gen)
import interface.nativeuibase as ui
importlib.reload(ui)



# =========================================================================
# Font
# =========================================================================
class NativeFont(Enum):
    boldLabelFont         = "boldLabelFont" 
    smallBoldLabelFont    = "smallBoldLabelFont" 
    tinyBoldLabelFont     = "tinyBoldLabelFont" 
    plainLabelFont        = "plainLabelFont" 
    smallPlainLabelFont   = "smallPlainLabelFont" 
    obliqueLabelFont      = "obliqueLabelFont" 
    smallObliqueLabelFont = "smallObliqueLabelFont" 
    fixedWidthFont        = "fixedWidthFont" 
    smallFixedWidthFont   = "smallFixedWidthFont" 

# =========================================================================
# Poopup
# =========================================================================
class Popup():
    # =============================
    # dunders
    # =============================
    def __init__(self,
        # window_id:              str,
        title:                  str,
        widthHeight:            Tuple[int, int],
        sizeable:               bool                = False,
        resizeToFitChildren:    bool                = False,
        backgroundColor:        Tuple[float, ...]   = (.1,.1,.1)
    ) -> None:
        self.window_id = '_'.join(title.split(" "))
        
        self.deleteWindow_byId(self.window_id)
        
        self.window_id = cmds.window(
            self.window_id, 
            title               = title, 
            widthHeight         = widthHeight,
            sizeable            = sizeable,
            resizeToFitChildren = resizeToFitChildren,
            backgroundColor     = backgroundColor,
            # closeCommand        = self.clear_window_contents
        )
        
    def __str__(self) -> str:
        return self.window_id
    
    
        
    # =============================
    # functions
    # =============================
    def showWindow(self):
        cmds.showWindow(self.window_id)

    def destroy(self):
        cmds.deleteUI(self.window_id, window=True)
        
    # def clear_window_contents(self):
    #     # Check if the window exists
    #     if cmds.window(self.window_id, exists=True):
    #         # Get all children of the window
    #         child_elements = cmds.columnLayout(self.window_id, query=True, childArray=True) or []

    #         # Loop through the children and delete each one
    #         for child in child_elements:
    #             cmds.deleteUI(child)


    # =============================
    # config
    # =============================
    def setSize(self, window_size: Tuple[int, int]):
        cmds.window(self.window_id, edit=True, widthHeight=window_size)
        
    def setBackgroundColor(self, nRGB: Tuple[float, float, float]):
        cmds.window(self.window_id, edit=True, bgc=nRGB)
        
    def setParent(self, parent: str):
        cmds.window(self.window_id, edit=True, parent=parent)
        
    # =============================
    # layouts
    # =============================
    def addScrollLayout(self, 
        verticalScrollBarAlwaysVisible=True, 
        # horizontalScrollBarThickness=300, 
        # verticalScrollBarThickness=16
    ) -> str:
        '''
        Returns:
        --------
        - `Full path name to the control`
        '''
        cmds.setParent(self.window_id)
        return cmds.scrollLayout(
            verticalScrollBarAlwaysVisible,
            # horizontalScrollBarThickness    = horizontalScrollBarThickness,
            # verticalScrollBarThickness      = verticalScrollBarThickness
        )



    


    # =============================
    # Static
    # =============================
    @staticmethod
    def deleteWindow_byId(window_id: str) -> bool:
        if cmds.window(window_id, exists=True): # Delete existing popup
            cmds.deleteUI(window_id, window=True)
            return True
        return False
    
    


# =========================================================================
# Layouts
# =========================================================================
class ScrollLayout(ui.Layout):
    _class_command = cmds.scrollLayout
    
    def __init__(self, parent: str=None) -> None:
        self.layout = cmds.scrollLayout() if not parent else \
            cmds.scrollLayout(parent=parent)
        super().__init__(self.layout)




class ColumnLayout(ui.Layout):
    _class_command = cmds.columnLayout
    
    def __init__(self,
        adjustableColumn=True,
        parent: str=None
    ) -> None:
        self.layout = cmds.columnLayout(adjustableColumn=adjustableColumn) if not parent else \
            cmds.columnLayout(adjustableColumn=adjustableColumn, parent=parent)

        super().__init__(self.layout)
        
        
        
class RowLayout(ui.Layout):
    _class_command = cmds.rowLayout
    
    def __init__(self,
        numberOfColumns = 3,
        # adjustableRow=True,
        parent: str=None
    ) -> None:
        self.layout = cmds.rowLayout(numberOfColumns=numberOfColumns) if not parent else \
            cmds.rowLayout(numberOfColumns=numberOfColumns, parent=parent)

        super().__init__(self.layout)
        
    

class FrameLayout(ui.Layout):
    _class_command = cmds.frameLayout
    
    def __init__(self,
        label: str,
        collapsable=True,
        parent: str=None
    ) -> None:
        
        
        self.layout = cmds.frameLayout(label=label, collapsable=collapsable) if not parent else \
            cmds.frameLayout(label=label, collapsable=collapsable, parent=parent)

        super().__init__(self.layout)
        
    @property
    def font(self) -> float:
        return self._class_command(self.name, query=True, font=True)
    @font.setter
    def font(self, font: NativeFont):
        return self._class_command(self.name, edit=True, font=font.value)
    
    
    @property
    def labelWidth(self) -> float:
        return self._class_command(self.name, query=True, labelWidth=True)
    @labelWidth.setter
    def labelWidth(self, labelWidth: float):
        return self._class_command(self.name, edit=True, labelWidth=labelWidth)
    
    
    @property
    def marginHeight(self) -> float:
        return self._class_command(self, query=True, marginHeight=True)
    @marginHeight.setter
    def marginHeight(self, marginHeight: float):
        return self._class_command(self, edit=True, marginHeight=marginHeight)
    
    @property
    def marginWidth(self) -> float:
        return self._class_command(self, query=True, marginWidth=True)
    @marginWidth.setter
    def marginWidth(self, marginWidth: float):
        return self._class_command(self, edit=True, marginWidth=marginWidth)
    



# =========================================================================
# Button
# =========================================================================
class Button(ui.UIBase):
    _class_command = cmds.button
    
    def __init__(self,
        label: str,
        command: Callable,
        height = 30,
        parent: str = None 
    ) -> None:
        label = ' | '.join(label.split("|"))

        self.transform = cmds.button(label=label, command=command, height=height) if not parent else \
            cmds.button(label=label, command=command, height=height, parent=parent)
        super().__init__(self.transform)
        
    def __repr__(self) -> str:
        return super().__repr__()
    
    

# =========================================================================
# Text
# =========================================================================
class Text(ui.UIBase):
    _class_command = cmds.text
    
    def __init__(self,
        label: str,
        width: float,
        align: str = "left"
    ) -> None:
        self.instance = cmds.text(label=label, width=width, align=align)
        super().__init__(self.instance)
        
    def setFont(self, font_name: NativeFont):
        cmds.text(self.instance, edit=True, font=font_name.value)
        
    def setHeight(self, height: int):
        cmds.text(self.instance, edit=True, height=height)



# =========================================================================
# Sliders
# =========================================================================
class AssociatedColorSlider(ui.AttributeSlider):
    _class_command = cmds.attrColorSliderGrp
    
    def __init__(self,
        label:  str,
        attr:   str
    ) -> None:
        '''
        Examples:
        ---------
        >>> cmds.attrColorSliderGrp(
        ...     label='Color', 
        ...     at=light + ".color"
        ... )
        '''
        self.instance = cmds.attrColorSliderGrp(
            label   = label,
            at      = attr
        )
        super().__init__(self.instance, attr=attr)
        
    
class AssociatedFieldSlider(ui.AttributeSlider):
    _class_command = cmds.attrFieldSliderGrp
    
    def __init__(self, 
        label:  str, 
        attr:   str,
        min:    float   = 0,
        max:    float   = 100,
    ) -> None:
        '''
        >>> cmds.attrFieldSliderGrp(
        ...     label='Exposure', 
        ...     at=light + ".exposure"
        ... )
        '''
        self.instance = cmds.attrFieldSliderGrp(
            label   = label,
            at      = attr,
            min     = min,
            max     = max,
        )
        super().__init__(self.instance, attr)

    # =============================
    # Getters & setters
    # =============================
    def setPrecision(self, precision: int):
        self._class_command(self.name, edit=True, pre=precision)
    
    

# =========================================================================
# CheckBox
# =========================================================================
class CheckBox(ui.UIBase):
    _class_command = cmds.checkBox
    
    def __init__(self, 
        label=""
    ) -> None:
        self.transform = cmds.checkBox(label=label)
        super().__init__(self.transform)
        
    def setChangeCommand(self, callback: Callable):
        self._class_command(self.transform, edit=True, changeCommand=callback)
        
        
# ==========================================================================
# Selectors
# ==========================================================================



# ==========================================================================
# ColorSwatch
# ==========================================================================
class ColorSwatch(ui.UIBase):
    _class_command = cmds.canvas
    
    def __init__(self, 
        name:   str | None      = None,
        width:  int             = 50,
        height: int             = 20,
        rgb:    Tuple[int, ...] = (0, 0, 0)
    ) -> None:
        fullpath = cmds.canvas(name, width=width, height=height)
        super().__init__(name=fullpath)
        
        self._class_command(self.name, edit=True, rgbValue=rgb)
        
    