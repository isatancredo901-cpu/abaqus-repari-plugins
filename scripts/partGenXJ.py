
# -*- coding: utf-8 -*-

from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=132.135406494141,
    height=82.2037048339844)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
import math
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


def createXJ(partName = "Part-xj",r=100,depth=10,deg=45):
    #########斜接修复
    import math
    rad = math.radians(deg)
    plist = [
        (0,0),
        (r,0),
        (r+depth/math.tan(rad),depth),
        (0,depth),
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
    p = mdb.models['Model-1'].Part(name=partName, dimensionality=THREE_D,
        type=DEFORMABLE_BODY)
    p = mdb.models['Model-1'].parts[partName]
    p.BaseSolidRevolve(sketch=s, angle=360, flipRevolveDirection=OFF)
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
p = createBase(partName="Part-1",L=Length,H = Height,Depth=Depth,R=0)
a.Instance(name='Part-1-1', part=p, dependent=ON)


#######################创建斜接
###
p = createXJ("Part-x",R,Depth,45)
a = mdb.models['Model-1'].rootAssembly
a.Instance(name='Part-x-1', part=p, dependent=ON)
a.rotate(instanceList=('Part-x-1', ), axisPoint=(0.0, 0.0, 0.0),
    axisDirection=(1.0, 0.0, 0.0), angle=90.0)
################
#创建part-base = part-1 - part-x
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanCut(name='Part-base',
    instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'],
    cuttingInstances=(a.instances['Part-x-1'], ), originalInstances=DELETE)
del a.features['Part-base-1']
#########创建part-cohesive = part-x - part-xj
p = mdb.models['Model-1'].parts["Part-x"]
a = mdb.models['Model-1'].rootAssembly
a.Instance(name='Part-x-1', part=p, dependent=ON)
a.rotate(instanceList=('Part-x-1', ), axisPoint=(0.0, 0.0, 0.0),
    axisDirection=(1.0, 0.0, 0.0), angle=90.0)
#
p = createXJ("Part-xj",R-0.1,Depth,45)
a = mdb.models['Model-1'].rootAssembly
a.Instance(name='Part-xj-1', part=p, dependent=ON)
a.rotate(instanceList=('Part-xj-1', ), axisPoint=(0.0, 0.0, 0.0),
    axisDirection=(1.0, 0.0, 0.0), angle=90.0)
##
a = mdb.models['Model-1'].rootAssembly
a.InstanceFromBooleanCut(name='Part-cohesive',
    instanceToBeCut=mdb.models['Model-1'].rootAssembly.instances['Part-x-1'],
    cuttingInstances=(a.instances['Part-xj-1'], ), originalInstances=DELETE)
del a.features['Part-cohesive-1']

############
for partName in ["Part-1","Part-x"]:
    del mdb.models['Model-1'].parts[partName]


##############
# a = mdb.models['Model-1'].rootAssembly
# a.InstanceFromBooleanMerge(name='Part-model', instances=(
#     a.instances['Part-base-1'], a.instances['Part-xj-1'], ),
#     keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)

###################复合材料分层############
##########

###########
############
def partLayer(partName = "Part-base",Nlayers = 4,layer = 0.1,Cohesive = 0.1):
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

a = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['Part-xj']
a.Instance(name='Part-xj-1', part=p, dependent=ON)
a.Instance(name='Part-xj-2', part=p, dependent=ON)
a.rotate(instanceList=('Part-xj-1',"Part-xj-2" ), axisPoint=(0.0, 0.0, 0.0),
    axisDirection=(1.0, 0.0, 0.0), angle=90.0)
#
a.InstanceFromBooleanMerge(name='Part-fix', instances=(
    a.instances['Part-xj-1'], a.instances['Part-xj-2'], ),
    originalInstances=DELETE, domain=GEOMETRY)
del a.features['Part-fix-1']

########################################
#######################
partLayer("Part-base",Nlayers = Nlayers,layer =layer,Cohesive = Cohesive)
partLayer("Part-cohesive",Nlayers = Nlayers,layer =layer,Cohesive = Cohesive)
partLayer("Part-fix",Nlayers = Nlayers,layer =layer,Cohesive = Cohesive)
#################装配


######################
####
###################
# cells = p.cells
# ####################
#
# dl = modelData['lrGap']
# p = mdb.models['Model-1'].parts['Part-base']
# p.PartitionCellByPlaneThreePoints(cells=p.cells,
#                                       point1=(-Length/2.+dl, 0, 0),
#                                       point2=(-Length/2.+dl, 1, 0),
#                                       point3=(-Length/2.+dl, 0, 1))
# #
# p = mdb.models['Model-1'].parts['Part-base']
# p.PartitionCellByPlaneThreePoints(cells=p.cells,
#                                       point1=(Length/2.-dl, 0, 0),
#                                       point2=(Length/2.-dl, 1, 0),
#                                       point3=(Length/2.-dl, 0, 1))
#
#
# ##################
#
# SSS
#
# ###################
# ##
# dl = modelData['tbGap']
# p = mdb.models['Model-1'].parts['Part-base']
# p.PartitionCellByPlaneThreePoints(cells=p.cells,
#                                       point1=(0, -Height/2. + dl, 0),
#                                       point2=(0, -Height/2.+ dl, 1),
#                                       point3=(1, -Height/2.+ dl, 0))
#
# ###
# dl = modelData['tbGap']
# p = mdb.models['Model-1'].parts['Part-base']
# p.PartitionCellByPlaneThreePoints(cells=p.cells,
#                                       point1=(0, Height/2.- dl, 0),
#                                       point2=(0, Height/2.- dl, 1),
#                                       point3=(1, Height/2.- dl, 0))
# ##############
# dl= modelData['lrGap']
# p = mdb.models['Model-1'].parts['Part-base']
# pickedCells = p.cells.getByBoundingBox(xMin=-Length/2., yMin=-Height/2., zMin=0.0,
#                                        xMax=-Length/2. + dl, yMax=Height/2., zMax=Depth)
# p.Set(cells=pickedCells, name='Set-left')
# #
# pickedCells = p.cells.getByBoundingBox(xMin=Length/2. - dl, yMin=-Height/2., zMin=0.0,
#                                        xMax=Length/2. , yMax=Height/2., zMax=Depth)
# p.Set(cells=pickedCells, name='Set-right')
##




# dl = modelData['tbGap']
# p = mdb.models['Model-1'].parts['Part-base']
# pickedCells = p.cells.getByBoundingBox(xMin=-Length/2., yMin=-Height/2., zMin=0.0,
#                                        xMax=-Length/2. + dl, yMax=Height/2., zMax=Depth)
# p.Set(cells=pickedCells, name='Set-left')
# #
# pickedCells = p.cells.getByBoundingBox(xMin=Length/2. - dl, yMin=-Height/2., zMin=0.0,
#                                        xMax=Length/2. , yMax=Height/2., zMax=Depth)
# p.Set(cells=pickedCells, name='Set-right')

####################
# SSSSSSSS
# #########################################
# ###修补参数
# type = modelData['repair']['type']
# repair = modelData['repair']
#
# if(type == 0):
#     r = repair['a']
#     depth = repair['b']
#     p = circleRepair("Part-circle",r,depth)
#     a.Instance(name='Part-circle-1', part=p, dependent=ON)
#     a.translate(instanceList=('Part-circle-1',), vector=(0.0, 0.0, -depth))
#     #
#
#     a.Instance(name='Part-circle-2', part=p, dependent=ON)
#     a.translate(instanceList=('Part-circle-2',), vector=(0.0, 0.0,Depth))
#     pass
# elif(type == 1):
#     pass
# elif(type == 2):
#     pass
#
#

#
#
# ###########阶梯修复
#
# #################



######