#!usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author:MCC
@file: export_json
@time: 2018/11/21 18:13
"""
import os
import json
import maya.cmds as cmds
def run(path):
    print "++++++++++++++++++"
    cmds.file(path, o=1, f=1)
    maFilePath = cmds.file(loc=1, q=1)
    jsonFilePath = os.path.dirname(maFilePath)

    def getModelTypeChildren(masterLayer=''):
        if masterLayer:
            if not cmds.objExists(masterLayer):
                return '%s group does not exists,please check your file at first!' % masterLayer
            transf = cmds.listRelatives(masterLayer, ad=True, type='transform', fullPath=True)
        else:
            transf = cmds.ls(type='transform', long=True)
        if transf:
            return transf

    data = getModelTypeChildren()
    print "data:",data
    print "jsonFilePath:",jsonFilePath
    print "maFilePath:",maFilePath
    with open("%s/layer.json" % jsonFilePath, "w") as f:
        json.dump(data, f, indent=4)
    return jsonFilePath



