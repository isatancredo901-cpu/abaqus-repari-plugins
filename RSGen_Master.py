
# -*- coding: utf-8 -*-
import os
from pyexpat import model
import sys
import re
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1')
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
import json
#########

############主函数


##########创建模型
def createModel():
    Mdb()
    return



##########更新模型
def updateModel():
    return
    




###########更新材料
def updateMaterial():
    return




############提交计算

#############后处理

def parseODB():
    pluginDir = modelData['pluginDir']
    execfile(os.path.join(pluginDir,"scripts//parseOdb.py"))
    return


###############
def updateModel():
    pluginDir = modelData['pluginDir']
    #####
    # globals()["modelData"] = modelData
    ##################
    TYPE = modelData['modify']['type']
    if(TYPE == 0):
        execfile(os.path.join(pluginDir,"scripts//partGenTP.py"))
    elif(TYPE==1):
        execfile(os.path.join(pluginDir,"scripts//partGenJT.py"))
    elif(TYPE == 2):
        execfile(os.path.join(pluginDir,"scripts//partGenXJ.py"))
    #
    execfile(os.path.join(pluginDir,"scripts//genModel.py"))
    return




def updateMaterial():
    #####################创建材料参数
    pluginDir = modelData['pluginDir']
    execfile(os.path.join(pluginDir,"scripts//updateMaterial.py"))
    return
def updateBcCondition():
    updateModel()
    return

def submitJob():
    pluginDir = modelData['pluginDir']
    execfile(os.path.join(pluginDir,"scripts//submitJob.py"))
    return


def string2list(string):
    return [float(i) for i in string.split("/")]

def execute(pluginDir='C:\\Users\\Binz\\Desktop\\Undelivered _pro\\prototypeApp', cmdType='createModel', mLength=150, mWidth=100, mHeight=1.025, mThickness=0.125, mNumLayer=5, mLayerAngle='45/0/-45/90/45', mPitDiameter=10, mMaterialFileKw='C:/Users/Binz/Desktop/Undelivered _pro/prototypeApp/material.json', mOdbFileKw='', modifyType=0, tbWidth=20, tbHeight=20, tbLayerNum=4, tbLayerAngle='0/10/20/40', glueThickness=0.1, jtNum=4, xjAngle=10, lrGap=1.2, tbGap=1.2, disValue=1000, jobName='Job-1', numOfCpus=1, mSubroutineFileKw='', parseOdbType=0, tableKw=(), matParaDict='{"material":{"adhesive":{"power":1.45,"de":[2.058,2.563,2.563],"qd":[122,136,136],"elastic":[100000,100000,100000],"density":1.2e-09},"base":{"depvar":90,"data":[126000,10400,10400,0.312,0.312,0.45,4500,4500,3280,0,0.06,1,1,1,1,1,1,1,2076,1357,50.9,187,55.4,150,1,1,66,66,66,1,1,1,1,1,20,10,0.1,1,1],"density":1.522e-09},"cohesiveZero":{"power":1.45,"de":[2.058,2.563,2.563],"qd":[122,136,136],"elastic":[100000,100000,100000],"density":1.2e-09}}}', tbType=0, tbShape=0, pressBC=0):
       # 构建 modelData 字典
    layerAngle = string2list(mLayerAngle)
    tbLayerAngle = string2list(tbLayerAngle)
    
    matParaDict = json.loads(matParaDict)

    modelData = {
    "tbLayerAngle":tbLayerAngle,
    "layerAngle":layerAngle,
    "disValue":disValue,
    "pluginDir":pluginDir,
    "jobName":jobName,
    "length":mLength,
    "height":mWidth,
    "depth":mHeight, #全部厚度
    "type":modifyType,
    "nlayers":len(layerAngle),
    "lrGap":lrGap,
    "tbGap":tbGap,
    "thickness":mThickness, #铺层厚度
    "cohesive":glueThickness, #是否内聚力层"
    "layers":layerAngle,
    "r": mPitDiameter, #缺陷半径
    "numOfCpus":numOfCpus,
    "mSubroutineFileKw":mSubroutineFileKw,
    "modify":{
        "type":modifyType, #0:贴片 1：斜接式 2:阶梯型
        "cohesive":glueThickness, #胶接厚度
        "tbShape":tbShape,
        "tbType":tbType,

        "a":2.0,
        "b":0.3,
        "r":tbWidth, #半径
        "n":tbLayerNum #层数
    }#,
  
    # "material":{
    #     "adhesive":{
    #         "density":1.2E-09,
    #         "elastic":[100000,100000,100000],
    #         "qd":[122,136,136],
    #         "power":1.45,
    #         "de":[2.058,2.563,2.563],
    #     },
    #     "base":{
    #             "density":1.522E-09,
    #             "data":[126000,10400,10400,0.312,0.312,0.45,4500,4500,
    #                     3280,0,0.06,1,1,1,1,1,2076,1357,50.9,187,55.4,
    #                     150,1,1,66,66,66,1,1,1,1,1,
    #                     20,10,0.1,1,1],
    #             "depvar":90},

    #     "cohesiveZero":{
    #         "density":1.2E-09,
    #         "elastic":[100000,100000,100000],
    #         "qd":[122,136,136],
    #         "power":1.45,
    #         "de":[2.058,2.563,2.563]
    #     }
    # }
}
    modelData.update(matParaDict)
    

    # 存入全局变量
    globals()["modelData"] = modelData
    
    if(cmdType=='createModel'):
        Mdb()
        updateModel()
    elif(cmdType=='updateModel'):
        Mdb()
        updateModel()
    elif(cmdType=='updateMaterial'):
        updateMaterial()
    elif(cmdType=='updateBC'):
        Mdb()
        updateBcCondition()
    elif(cmdType=='submitJob'):
        submitJob()
    elif(cmdType=='parseODB'):
        parseODB()
    return







# execute()