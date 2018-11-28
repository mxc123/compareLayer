#!usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author:MCC
@file: compareLayer
@time: 2018/11/21 18:43
"""
import os
import json

import maya.cmds as cmds
DESKPATH = os.path.join(os.path.expanduser("~"), 'Desktop')
DESKPATH = DESKPATH.replace("Documents\\",'')
def writeErrorMessage(data):
    lastDict = {}
    if os.path.exists("%s/errorLayer.json" % DESKPATH):

        with open("%s/errorLayer.json" % DESKPATH, "r") as file:
            datas = json.loads(file.read())
            for ii in datas.keys():
                if ii == data.keys()[0]:

                    lastDict = {ii: dict(datas[ii], **data[data.keys()[0]])}
                else:
                    lastDict = dict(datas, **data)

        with open("%s/errorLayer.json" % DESKPATH, "w") as f:
            json.dump(lastDict, f)

    else:
        with open("%s/errorLayer.json" % DESKPATH, "a") as f:
            json.dump(data, f)

    return True

def run(path,modePath):
    lastDict = {}
    otherDict = {}
    otherData = []
    cmds.file(path, o=1, f=1)
    maFileNamePath = cmds.file(loc=1, q=1)
    # maFile_baseName = os.path.basename(maFileNamePath)
    # maFile_step = maFile_baseName.split("_")[1]

    maFilePath = os.path.dirname(maFileNamePath)
    if "Texture" in maFilePath:
        jsonFileNamePath = "%s/layer.json" % maFilePath.replace("Texture", "Mod")

    elif "Rig" in maFilePath:
        jsonFileNamePath = "%s/layer.json" % maFilePath.replace("Rig", "Mod")

    # jsonFilePath = os.path.basename(maFilePath)
    # old_name = os.path.basename(cmds.file(loc=1,q=1)).split(".")[0]
    # name_split_list = old_name.split("_")
    # name_split_list.remove(name_split_list[-2])
    # name_split_list[-1] = name_split_list[-1][:4]
    # file_name = '_'.join(name_split_list)
    # if 'tex' in file_name:
    # new_file = file_name.replace("tex","model")
    # elif 'rig' in file_name:
    # new_file = file_name.replace("rig","model")
    # json_path = os.path.dirname(os.path.dirname(os.path.dirname(cmds.file(loc=1,q=1))))+"/model/approved/"+new_file+".json"

    # if os.path.exists(json_path):
    if os.path.exists(jsonFileNamePath):
        with open(jsonFileNamePath, 'r') as load_f:
            model_data = json.load(load_f)

        for ii in model_data:
            if cmds.objExists(ii.split("|", 1)[1]):
                pass
            else:
                otherData.append(ii.split("|", 1)[1])

        otherDict[path]=otherData
        lastDict[modePath]=otherDict
    if otherDict:
        writeErrorMessage(lastDict)

    return True




