#!usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@author:MCC
@file: compareUI
@time: 2018/11/21 16:29
"""
import sys
import os
import subprocess
sys.path.append(r'C:\cgteamwork\bin\lib\pyside')
from PySide import QtGui as QtWidgets
from PySide import QtCore
from mouseDagClass import My_ListWidget
MAYABATCHPATH = r'D:/Autodesk Maya/Maya2017/bin/mayabatch.exe'

class MyWindows(QtWidgets.QDialog):
    def __init__(self,parent=None):
        super(MyWindows,self).__init__(parent)
        self._initUI()

    def _initUI(self):
        self.setWindowTitle(u"比对层级")
        self.resize(800,600)
        modelGroupBox = QtWidgets.QGroupBox(u'模型文件')
        self.modelListWidgets = My_ListWidget(self)
        modelListLayout = QtWidgets.QHBoxLayout()
        modelListLayout.addWidget(self.modelListWidgets)
        modelGroupBox.setLayout(modelListLayout)
        self.modelListWidgets.setDragEnabled(True)

        otherGroupBox = QtWidgets.QGroupBox(u'绑定/材质')
        self.compareListWidgets = My_ListWidget(self)
        compareListLayout = QtWidgets.QHBoxLayout()
        compareListLayout.addWidget(self.compareListWidgets)
        otherGroupBox.setLayout(compareListLayout)
        self.compareListWidgets.setDragEnabled(True)
        sureBtn = QtWidgets.QPushButton(u"确定")
        clearBtn = QtWidgets.QPushButton(u"清除")

        spliter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        spliter.addWidget(modelGroupBox)
        spliter.addWidget(otherGroupBox)
        btnLayout = QtWidgets.QHBoxLayout()
        btnLayout.addStretch(5)
        btnLayout.addWidget(clearBtn)
        btnLayout.addStretch(1)
        btnLayout.addWidget(sureBtn)

        lastLayout = QtWidgets.QVBoxLayout()
        lastLayout.addWidget(spliter)
        lastLayout.addLayout(btnLayout)
        self.setLayout(lastLayout)
        sureBtn.clicked.connect(self.messageInfo)
        clearBtn.clicked.connect(self.clearFun)

    def getModelMessage(self):
        maFileList=[]
        count = self.modelListWidgets.count()
        for ii in xrange(count):
            maFileList.append(self.modelListWidgets.item(ii).text())
        return maFileList

    def getOtherMessage(self):
        otherMaFileList = []
        count = self.compareListWidgets.count()
        for ii in xrange(count):
            otherMaFileList.append(self.compareListWidgets.item(ii).text())
        return otherMaFileList

    def getAboutRig(self,modelPath):
        modelBaseName = os.path.basename(modelPath)
        modelDirName = os.path.dirname(modelPath)
        rigBaseName = modelBaseName.replace("Mod","Rig")
        rigDirName = modelDirName.replace("Mod","Rig")
        rigPath= "%s/%s"%(rigDirName,rigBaseName)
        return rigPath

    def getAboutTexture(self,modelPath):
        modelBaseName = os.path.basename(modelPath)
        modelDirName = os.path.dirname(modelPath)
        texBaseName = modelBaseName.replace("Mod","Texture")
        texDirName = modelDirName.replace("Mod","Texture")
        texPath= "%s/%s"%(texDirName,texBaseName)
        return texPath

    def exportModelJson(self,dirPath):
        jsonLayerDir= os.path.dirname(dirPath)
        jsonLayerPath = "%s/layer.json"%jsonLayerDir
        if os.path.exists(jsonLayerPath):
            pass
        else:
            currentPath = os.path.dirname(__file__)
            melFile='%s/export_json.mel'%currentPath
            cmd = '"{mayaBatchPath}" -script "{melFile}" "{maPath}"'.format(
                mayaBatchPath = MAYABATCHPATH,
                melFile = melFile,
                maPath = dirPath,
                )
            subprocess.check_call(cmd, shell=True)

    def compareLayerMessages(self,maPath,currentFile):
        currentPath = os.path.dirname(__file__)
        melFile = '%s/compareMessage.mel' % currentPath
        cmd = '"{mayaBatchPath}" -script "{melFile}" "{maPath}" "{currentFile}"'.format(
            mayaBatchPath=MAYABATCHPATH,
            melFile=melFile,
            maPath=maPath,
            currentFile=currentFile,
        )
        subprocess.check_call(cmd, shell=True)


    def run(self):
        maFileList = self.getModelMessage()
        otherMaFileList = self.getOtherMessage()
        for ii in maFileList:
            self.exportModelJson(ii)
            rigPath = self.getAboutRig(ii)
            texPath = self.getAboutTexture(ii)
            print "rigPath",rigPath
            print "texPath",texPath
            print "otherMaFileList",otherMaFileList
            if rigPath in otherMaFileList:
                self.compareLayerMessages(rigPath,ii)
            if texPath in otherMaFileList:
                self.compareLayerMessages(texPath,ii)
        return True

    def messageInfo(self):
        if self.run():
            QtWidgets.QMessageBox.information(self,"message",u"比较层级完成")
        else:
            QtWidgets.QMessageBox.warning(self,"message",u"比较层级出错")

    def clearFun(self):
        self.modelListWidgets.clear()
        self.compareListWidgets.clear()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWindows = MyWindows()
    myWindows.show()
    sys.exit(app.exec_())




