""" =================================================================
| arnold.py -- Python/MayaMedic/nodes/arnold.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """
import importlib
from typing import *

import maya.cmds as cmds

import utility.general as gen
importlib.reload(gen)
from . import node as nd
importlib.reload(nd)



def setRendererToArnold():
    cmds.setAttr("defaultRenderGlobals.currentRenderer", "arnold", type="string")



class AiLight(nd.MayaNode):
    
    def __init__(self,
        nodename:   nd.NodeNames,
        name:       str, 
        position:   Tuple[float, float, float] = None,
        rotation:   Tuple[float, float, float] = None,
    ) -> None:
        super().__init__(
            name      = name,
            transform = (tf := cmds.createNode('transform',name=name)), 
            shape     = cmds.createNode(nodename.name, name=name + 'Shape', parent=tf)
        )
        
        if position: self.move(position)
        if rotation: self.rotate(rotation)
        
        # ~~~~~~~~ turn on Illuminates By Default ~~~~~~~~
        self.connectLightSet()
        
    # =============================
    # Getters & Setters
    # =============================
    @property
    def intensity(self) -> float:
        return cmds.getAttr(self.shape + '.intensity')
    @intensity.setter
    def intensity(self, intensity: float) -> float:
        return cmds.setAttr(self.shape + '.intensity', intensity)
    
    
    @property
    def exposure(self) -> float:
        return cmds.getAttr(self.shape + '.exposure')
    @exposure.setter
    def exposure(self, exposure: float) -> float:
        return cmds.setAttr(self.shape + '.exposure', exposure)
    
    
    @property
    def normalize(self) -> bool:
        return cmds.getAttr(self.shape + '.normalize')
    @normalize.setter
    def normalize(self, normalize: bool) -> bool:
        return cmds.setAttr(self.shape + '.normalize', normalize)
    
    # =============================
    # Functions
    # =============================
    def connectLightSet(self, lightSetTransform: str='defaultLightSet') -> None:
        '''This will check `Illuminates By Default` '''        
        self.connetAttr('instObjGroups[0]', lightSetTransform, 'dagSetMembers')
        
        
        
        
    # =============================
    # Static
    # =============================
    @staticmethod
    def getAllAiLights() -> Dict[str, Tuple[List[str], Tuple[int, ...]]]:
        arnold_light_types = {
            "Area Lights":         (nd.NodeNames.aiAreaLight.name,         gen.Colors.jasper),
            "Mesh Lights":         (nd.NodeNames.aiMeshLight.name,         gen.Colors.unreal_neon_purple),
            "Photometric Lights":  (nd.NodeNames.aiPhotometricLight.name,  gen.Colors.google_blue),
            "Sky Dome Lights":     (nd.NodeNames.aiSkyDomeLight.name,      gen.Colors.google_red),
        }
        aiLights = {}
        for section, (light_type, color) in arnold_light_types.items():
            listed_lgt = cmds.ls( type=light_type )
            if listed_lgt: aiLights[section] = listed_lgt, color
        return aiLights