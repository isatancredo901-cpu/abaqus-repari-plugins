#-*- coding: utf-8 -*-
############
import sys
from abaqus import *
from abaqusConstants import *
from caeModules import *
from odbAccess import *
import numpy as np
############


############

#################
modelData = globals().get("modelData", {})
odbName = modelData.get('mOdbFileKw') or (modelData.get('jobName', 'Job-1') + '.odb')
#################

# odbName = r"C:\Users\Binz\Desktop\2026-3-4-pygui-plugin-7000-7days\Temp\ABQPlugin\Well-Analysis.odb"
odb = session.openOdb(
    name=odbName, 
    readOnly=False)
#A
session.viewports['Viewport: 1'].setValues(displayedObject=odb)
# session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
#     variableLabel='RF1', outputPosition=ELEMENT_NODAL, )
session.viewports['Viewport: 1'].odbDisplay.display.setValues(
    plotState=CONTOURS_ON_DEF)

xyList = session.xyDataListFromField(odb=odb, outputPosition=NODAL, variable=((
    'RF', NODAL, ((COMPONENT, 'RF1'), )), ), nodeSets=("SET-RES", ))
np.savetxt("Force.txt",xyList[0].data)
