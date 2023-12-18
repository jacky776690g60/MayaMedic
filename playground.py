''' This script is just for testing. '''

import importlib
import maya.cmds as cmds

import nodes.node as nd
importlib.reload(nd)
import utility.outline as otl
importlib.reload(otl)

if __name__ == "__main__":
    'test your code here...'
    
    # print(nd.NodeNames.transform.name)
    
    # cmds.createNode(nd.NodeNames.nCloth.name, name="name" + 'Shape')
    
    print(otl.get_parents('aiAreaLight1'))