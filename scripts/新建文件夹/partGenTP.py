
# -*- coding: utf-8 -*-
import math
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=132.135406494141,
    height=82.2037048339844)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()

#

#######设置相关模型参数

##########
def createBase(partName="Part-base",L=100,H = 200,Depth=2.0,R=0.):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(-L/2., -H/2.), point2=(L/2., H/2.))
    if(R != 0):
        s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(R,0))
    p = mdb.models['Model-1'].Part(name=partName, dimensionality=THREE_D,
                                   type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partName]
    p.BaseSolidExtrude(sketch=s, depth=Depth)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    return p

####修复建模

def circleRepair(partName="Part-circle",R = 12.,Depth=1.0):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(R,0))
    p = mdb.models['Model-1'].Part(name=partName, dimensionality=THREE_D,
                                   type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partName]
    p.BaseSolidExtrude(sketch=s, depth=Depth)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    return p

def createCohesive():
    #########斜接修复
    deg = 15.
    rad = math.radians(deg)
    plist = [
        (0,0),
        (R,0),
        (R+Depth/math.tan(rad),Depth),
        (0,Depth),
        (0,0)
    ]
    ################
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.ConstructionLine(point1=(0.0, -100.0), point2=(0.0, 100.0))
    s.FixedConstraint(entity=g[2])
    for i in range(len(plist)-1):
        s.Line(point1=plist[i], point2=plist[i+1])
    p = mdb.models['Model-1'].Part(name='Part-xj', dimensionality=THREE_D,
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts['Part-xj']
    p.BaseSolidRevolve(sketch=s, angle=360, flipRevolveDirection=OFF)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts['Part-xj']
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    return p

#创建贴片修复，贴片厚度包括内聚力层
def createTP(partName = "Part-xj",r=100,depth=10):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                                sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.CircleByCenterPerimeter(center=(0.0, 0.0), point1=(r, 0))
    p = mdb.models['Model-1'].Part(name=partName, dimensionality=THREE_D,
                                   type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partName]
    p.BaseSolidExtrude(sketch=s, depth=depth)
    s.unsetPrimaryObject()
    p = mdb.models['Model-1'].parts[partName]
    session.viewports['Viewport: 1'].setValues(displayedObject=p)
    del mdb.models['Model-1'].sketches['__profile__']
    return p

    ########

    #
    # a.InstanceFromBooleanCut(name='Part-base1',
    #     instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-base-1'],
    #     cuttingInstances=(a3.instances['Part-xj-1'], ), originalInstances=DELETE)
    # ##########
#建模参数
###
modelData = globals()["modelData"]
###
Length = modelData['length']
Height = modelData["height"]
Depth = modelData['depth']
R = modelData['r']
#
Cohesive = modelData['cohesive']
Nlayers = modelData['nlayers']
layer = Depth*1.0/Nlayers
Depth += (Nlayers-1)*Cohesive
#
globals()["totalDepth"] = Depth
#########
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = createBase(partName="Part-base",L=Length,H = Height,Depth=Depth,R=R)
a.Instance(name='Part-1-1', part=p, dependent=ON)

#############
#######################创建斜接
###
modifyDict = modelData['modify']
nLayers = modifyDict['n']
mCohesive = modifyDict['cohesive']
mDepth = layer * nLayers
mDepth += (nLayers-1)*Cohesive
#
r = modifyDict['r']

#建立贴片模型
p = createTP("Part-x",r,mDepth+mCohesive)
partName = "Part-x"
##############
dz = 0.0
for i in range(nLayers-1):
    dz += layer
    p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                      point1=(0,0,dz),
                                      point2=(1,0,dz),
                                      point3=(0,1,dz))
    #
    dz += Cohesive
    p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                      point1=(0, 0, dz),
                                      point2=(1, 0, dz),
                                      point3=(0, 1, dz))
dz = mDepth
p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                  point1=(0, 0, dz),
                                  point2=(1, 0, dz),
                                  point3=(0, 1, dz))
#
nl, nc = 1, 1
cells_sorted = sorted(p.cells, key=lambda c: c.pointOn[0][2])
for i, cell in enumerate(cells_sorted):
    index = cell.index
    cells = p.cells[index:index + 1]
    if ((i + 1) % 2 == 0):
        p.Set(cells=cells, name='Set-{}-cohesive-{}'.format(partName, nc))
        nc += 1
    else:
        p.Set(cells=cells, name='Set-{}-layer-{}'.format(partName, nl))
        nl += 1

###############
a = mdb.models['Model-1'].rootAssembly
a.Instance(name='Part-x-1', part=p, dependent=ON)
a.translate(instanceList=('Part-x-1', ), vector=(.0, 0.0, -mDepth-mCohesive))
#
a.Instance(name='Part-x-2', part=p, dependent=ON)

a.rotate(instanceList=('Part-x-2', ), axisPoint=(0.0, 0.0, 0.0),
    axisDirection=(1.0, 0.0, 0.0), angle=180.0)
a.translate(instanceList=('Part-x-2', ), vector=(.0, 0.0, Depth+mDepth+mCohesive))

###################复合材料分层############
###########
############
def partLayer(partName = "Part-base"):
    dz = 0.
    for i in range(Nlayers-1):
        dz += layer
        p = mdb.models['Model-1'].parts[partName]
        p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                          point1=(0,0,dz),
                                          point2=(1,0,dz),
                                          point3=(0,1,dz))
        #
        #

        dz += Cohesive
        p = mdb.models['Model-1'].parts[partName]
        p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                          point1=(0, 0, dz),
                                          point2=(1, 0, dz),
                                          point3=(0, 1, dz))
        #
    nl,nc = 1,1
    p = mdb.models['Model-1'].parts[partName]
    cells_sorted = sorted(p.cells, key=lambda c: c.pointOn[0][2])
    for i,cell in enumerate(cells_sorted):
        index = cell.index
        cells = p.cells[index:index+1]
        if((i+1)%2 == 0):
            p.Set(cells=cells, name='Set-{}-cohesive-{}'.format(partName,nc))
            nc += 1
        else:
            p.Set(cells=cells, name='Set-{}-layer-{}'.format(partName,nl))
            nl += 1
########################################
########################################
#######################
partLayer("Part-base")
#################装配
