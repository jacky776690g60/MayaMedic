""" =================================================================
| general.py -- Python/MayaMedic/utility/general.py
|
| Created by Jack on 12/06, 2023
| Copyright © 2023 jacktogon. All rights reserved.
================================================================= """

"""
Visit: https://help.autodesk.com/view/MAYAUL/2024/ENU/?guid=__CommandsPython_index_html
"""

import maya.cmds as cmds


class Colors:
    ''' Contains a bunch of cool colors '''
    jasper               = (0.84, 0.41, 0.33)
    coral                = (0.97, 0.53, 0.39)
    bittersweet          = (1.00, 0.35, 0.37)
    blush                = (0.92, 0.39, 0.55)
    sunglow              = (1.00, 0.79, 0.23)
    selective_yellow     = (1.00, 0.72, 0.01)
    yellow_green         = (0.54, 0.79, 0.15)
    mint_cream           = (0.94, 0.97, 0.96)
    google_blue          = (0.26, 0.52, 0.96)
    google_red           = (0.86, 0.27, 0.22)
    rose                 = (0.97, 0.15, 0.52)
    grape                = (0.45, 0.04, 0.72)
    mermaid_tail         = (0.30, 0.88, 0.71)
    unreal_neon_purple   = (0.73, 0.49, 0.95)
    unreal_blue          = (0.06, 0.07, 0.15)
    chinese_black        = (0.08, 0.08, 0.08)
    eclipse_black        = (0.07, 0.07, 0.07)


def print_cmds_info(command: str):
    """
    print info for commands
    
    Examples:
    ---------
    >>> print_cmds_info("frameLayout")
    >>> print_cmds_info("columnLayout")
    """
    helpInfo = cmds.help(command)
    print(helpInfo)


def objExists(name_path: str) -> bool:
    """
    Check if object exists based on condition(s)
    
    Examples:
    ---------
    >>> objExists("namespace1:objectName")
    >>> objExists("parent|child")
    >>> objExists("|topLevelParent|...|parent|objectName")
    >>> objExists("name-*")
    """
    return cmds.objExists(name_path)