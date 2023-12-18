""" =================================================================
| configuration.py -- Python/MayaMedic/utility/configuration.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

import maya.cmds as cmds

def set_scene_units(unit_name: str, verbose=False):
    available_linear_units = ["mm","cm","m","in","ft","yd"]
    
    if unit_name not in available_linear_units:
        raise ValueError("Can only use one of the unites: {}".format(available_linear_units))
    
    if (current_unit:= cmds.currentUnit(query=True, linear=True)) != unit_name:
        cmds.currentUnit(linear=unit_name)
        if verbose: print("Scene units set to centimeters.")
    else:
        if verbose: print("Scene is already in centimeters.")