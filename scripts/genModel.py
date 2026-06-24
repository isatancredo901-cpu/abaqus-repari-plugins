#-*- coding: utf-8 -*-
# ####################
#####################创建材料参数
matDict = modelData["material"]
###########基体
mBase = matDict['base']
mdb.models['Model-1'].Material(name='Mat-base')
mdb.models['Model-1'].materials['Mat-base'].Density(table=((mBase['density'], ), ))
mdb.models['Model-1'].materials['Mat-base'].Depvar(n=mBase['depvar'])
mdb.models['Model-1'].materials['Mat-base'].UserMaterial(mechanicalConstants=mBase['data'])
#############胶层
mBase = matDict['adhesive']
mdb.models['Model-1'].Material(name='Mat-cohesive')
mdb.models['Model-1'].materials['Mat-cohesive'].Density(table=((mBase['density'], ), ))
mdb.models['Model-1'].materials['Mat-cohesive'].Elastic(type=TRACTION, table=(mBase['elastic'], ))
mdb.models['Model-1'].materials['Mat-cohesive'].QuadsDamageInitiation(table=(mBase['qd'], ))
# mdb.models['Model-1'].materials['Mat-cohesive'].quadeDamageInitiation.DamageEvolution(
#     type=ENERGY, mixedModeBehavior=BK, power=mBase['power'], table=(mBase['de'], ))
mdb.models['Model-1'].materials['Mat-cohesive'].quadsDamageInitiation.DamageEvolution(
    type=ENERGY, mixedModeBehavior=BK, power=mBase['power'], table=(mBase['de'], ))
###########################
mBase = matDict['cohesiveZero']
mdb.models['Model-1'].Material(name='Mat-cohesiveZero')
mdb.models['Model-1'].materials['Mat-cohesiveZero'].Density(table=((mBase['density'], ), ))
mdb.models['Model-1'].materials['Mat-cohesiveZero'].Elastic(type=TRACTION, table=(mBase['elastic'], ))
mdb.models['Model-1'].materials['Mat-cohesiveZero'].QuadsDamageInitiation(table=(mBase['qd'], ))
mdb.models['Model-1'].materials['Mat-cohesiveZero'].quadsDamageInitiation.DamageEvolution(
    type=ENERGY, mixedModeBehavior=BK, power=mBase['power'], table=(mBase['de'], ))
##################截面属性
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-base',
    material='Mat-base', thickness=None)
mdb.models['Model-1'].CohesiveSection(name='Section-adhesive',
    material='Mat-cohesive', response=TRACTION_SEPARATION,
    outOfPlaneThickness=None)

mdb.models['Model-1'].CohesiveSection(name='Section-cohesiveZero',
    material='Mat-cohesiveZero', response=TRACTION_SEPARATION,
    outOfPlaneThickness=None)
#########################分不同情况判断
if(TYPE in [1,2]):
        #装配
    a = mdb.models['Model-1'].rootAssembly
    session.viewports['Viewport: 1'].setValues(displayedObject=a)
    a = mdb.models['Model-1'].rootAssembly
    p = mdb.models['Model-1'].parts['Part-base']
    a.Instance(name='Part-base-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['Part-cohesive']
    a.Instance(name='Part-cohesive-1', part=p, dependent=ON)
    p = mdb.models['Model-1'].parts['Part-fix']
    a.Instance(name='Part-fix-1', part=p, dependent=ON)
    a = mdb.models['Model-1'].rootAssembly
    a.InstanceFromBooleanMerge(name='Part-model', instances=(
        a.instances['Part-base-1'], a.instances['Part-cohesive-1'],
        a.instances['Part-fix-1'], ), keepIntersections=ON,
        originalInstances=SUPPRESS, domain=GEOMETRY)
    ##############
    ################粘接胶层材料
    p = mdb.models['Model-1'].parts['Part-cohesive']
    region = regionToolset.Region(cells=p.cells)
    p.SectionAssignment(region=region, sectionName='Section-cohesiveZero',
        offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',
        thicknessAssignment=FROM_SECTION)
    ####
    pComposite = ['Part-base',"Part-fix"]
    for i,partName in enumerate(pComposite):
        ########################
        p = mdb.models['Model-1'].parts['Part-model']
        nlayers = modelData['nlayers']
        for i in range(nlayers-1):
            region = p.sets['Set-{}-cohesive-{}'.format(partName,i+1)]
            p.SectionAssignment(region=region, sectionName='Section-adhesive', offset=0.0,
                offsetType=MIDDLE_SURFACE, offsetField='',
                thicknessAssignment=FROM_SECTION)
        #
        layers = modelData['layers']
        for i in range(nlayers):
            region = p.sets['Set-{}-layer-{}'.format(partName,i+1)]
            p.SectionAssignment(region=region, sectionName='Section-base', offset=0.0,
                offsetType=MIDDLE_SURFACE, offsetField='',
                thicknessAssignment=FROM_SECTION)
            #
            p.MaterialOrientation(region=region,
                                                                        orientationType=DISCRETE, axis=AXIS_3,
                                                                        normalAxisDefinition=VECTOR,
                                                                        normalAxisVector=(0.0, 0.0, 1.0),
                                                                        flipNormalDirection=False,
                                                                        normalAxisDirection=AXIS_3,
                                                                        primaryAxisDefinition=VECTOR,
                                                                        primaryAxisVector=(1.0, 0.0, 0.0),
                                                                        primaryAxisDirection=AXIS_1,
                                                                        flipPrimaryDirection=False,
                                                                        additionalRotationType=ROTATION_ANGLE,
                                                                        additionalRotationField='', angle=layers[i],
                                                                        stackDirection=STACK_3)
    #############################################

#######


###
if(TYPE == 0):
        # 装配
    a = mdb.models['Model-1'].rootAssembly
    a.InstanceFromBooleanMerge(name='Part-model', instances=(
        a.instances['Part-1-1'], a.instances['Part-x-1'], a.instances['Part-x-2'],
    ), keepIntersections=ON, originalInstances=DELETE, domain=GEOMETRY)

    pComposite = ['Part-base']
    for i, partName in enumerate(pComposite):
        ########################
        # p = mdb.models['Model-1'].parts[partName]
        p = mdb.models['Model-1'].parts['Part-model']
        nlayers = modelData['nlayers']
        for i in range(nlayers - 1):
            region = p.sets['Set-{}-cohesive-{}'.format(partName, i + 1)]
            p.SectionAssignment(region=region, sectionName='Section-adhesive', offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
        #
        layers = modelData['layerAngle'][:nlayers]
        for i in range(nlayers):
            region = p.sets['Set-{}-layer-{}'.format(partName, i + 1)]
            p.SectionAssignment(region=region, sectionName='Section-base', offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
            #
            p.MaterialOrientation(region=region,
                                                                    orientationType=DISCRETE, axis=AXIS_3,
                                                                    normalAxisDefinition=VECTOR,
                                                                    normalAxisVector=(0.0, 0.0, 1.0),
                                                                    flipNormalDirection=False,
                                                                    normalAxisDirection=AXIS_3,
                                                                    primaryAxisDefinition=VECTOR,
                                                                    primaryAxisVector=(1.0, 0.0, 0.0),
                                                                    primaryAxisDirection=AXIS_1,
                                                                    flipPrimaryDirection=False,
                                                                    additionalRotationType=ROTATION_ANGLE,
                                                                    additionalRotationField='', angle=layers[i],
                                                                    stackDirection=STACK_3)
    #############################################
    #part-x
    pComposite = ['Part-x']
    for i, partName in enumerate(pComposite):
        ########################
        # p = mdb.models['Model-1'].parts[partName]
        p = mdb.models['Model-1'].parts['Part-model']
        nlayers = modelData['modify']['n']
        for i in range(nlayers - 1):
            region = p.sets['Set-{}-cohesive-{}'.format(partName, i + 1)]
            p.SectionAssignment(region=region, sectionName='Section-adhesive', offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
        #
        layers = modelData['tbLayerAngle'][:nlayers]
        for i in range(nlayers):
            region = p.sets['Set-{}-layer-{}'.format(partName, i + 1)]
            p.SectionAssignment(region=region, sectionName='Section-base', offset=0.0,
                                offsetType=MIDDLE_SURFACE, offsetField='',
                                thicknessAssignment=FROM_SECTION)
            #
            p.MaterialOrientation(region=region,
                                                                    orientationType=DISCRETE, axis=AXIS_3,
                                                                    normalAxisDefinition=VECTOR,
                                                                    normalAxisVector=(0.0, 0.0, 1.0),
                                                                    flipNormalDirection=False,
                                                                    normalAxisDirection=AXIS_3,
                                                                    primaryAxisDefinition=VECTOR,
                                                                    primaryAxisVector=(1.0, 0.0, 0.0),
                                                                    primaryAxisDirection=AXIS_1,
                                                                    flipPrimaryDirection=False,
                                                                    additionalRotationType=ROTATION_ANGLE,
                                                                    additionalRotationField='', angle=layers[i],
                                                                    stackDirection=STACK_3)
        #
        region = p.sets['Set-{}-cohesive-{}'.format(partName, nlayers)]
        p.SectionAssignment(region=region, sectionName='Section-cohesiveZero', offset=0.0,
                            offsetType=MIDDLE_SURFACE, offsetField='',
                            thicknessAssignment=FROM_SECTION)




################################################


#########建立参考点
Length = modelData['length']
Height = modelData['height']
Depth = globals()['totalDepth']

a = mdb.models['Model-1'].rootAssembly
a.ReferencePoint(point=(-Length/2., 0.0, Depth/2.))
a.ReferencePoint(point=(Length/2., 0.0, Depth/2.))
######切割方便加载
dl = modelData['lrGap']
p = mdb.models['Model-1'].parts['Part-model']
p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                    point1=(-Length/2.+dl, 0, 0),
                                    point2=(-Length/2.+dl, 1, 0),
                                    point3=(-Length/2.+dl, 0, 1))
#
p = mdb.models['Model-1'].parts['Part-model']
p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                    point1=(Length/2.-dl, 0, 0),
                                    point2=(Length/2.-dl, 1, 0),
                                    point3=(Length/2.-dl, 0, 1))


dl = modelData['tbGap']
if(dl >= 1e-3):
    p = mdb.models['Model-1'].parts['Part-model']
    p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                        point1=(0, -Height/2. + dl, 0),
                                        point2=(0, -Height/2.+ dl, 1),
                                        point3=(1, -Height/2.+ dl, 0))

    ###
    dl = modelData['tbGap']
    p = mdb.models['Model-1'].parts['Part-model']
    p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                        point1=(0, Height/2.- dl, 0),
                                        point2=(0, Height/2.- dl, 1),
                                        point3=(1, Height/2.- dl, 0))
##############
dl= modelData['lrGap']
p = mdb.models['Model-1'].parts['Part-model']
pickedCells = p.cells.getByBoundingBox(xMin=-Length/2., yMin=-Height/2., zMin=0.0,
                                    xMax=-Length/2. + dl, yMax=Height/2., zMax=Depth)
p.Set(cells=pickedCells, name='Set-left')
#
pickedCells = p.cells.getByBoundingBox(xMin=Length/2. - dl, yMin=-Height/2., zMin=0.0,
                                    xMax=Length/2. , yMax=Height/2., zMax=Depth)
p.Set(cells=pickedCells, name='Set-right')
#




# dl = modelData['tbGap']
# p = mdb.models['Model-1'].parts['Part-model']
# pickedCells = p.cells.getByBoundingBox(xMin=-Length/2., yMin=-Height/2., zMin=0.0,
#                                     xMax=-Length/2. + dl, yMax=Height/2., zMax=Depth)
# p.Set(cells=pickedCells, name='Set-left')
# #
# pickedCells = p.cells.getByBoundingBox(xMin=Length/2. - dl, yMin=-Height/2., zMin=0.0,
#                                     xMax=Length/2. , yMax=Height/2., zMax=Depth)
# p.Set(cells=pickedCells, name='Set-right')
############分析步
mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-1', previous='Initial',
    improvedDtMethod=ON)
########
##相互作用
a1 = mdb.models['Model-1'].rootAssembly
r1 = a1.referencePoints
refPoints1=(r1[r1.keys()[1]], )
region1=regionToolset.Region(referencePoints=refPoints1)
a1 = mdb.models['Model-1'].rootAssembly
region2=a1.instances['Part-model-1'].sets['Set-left']
mdb.models['Model-1'].Coupling(name='Constraint-left', controlPoint=region1,
    surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
    localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
##########
a1 = mdb.models['Model-1'].rootAssembly
r1 = a1.referencePoints
refPoints1=(r1[r1.keys()[0]], )
region1=regionToolset.Region(referencePoints=refPoints1)
a1 = mdb.models['Model-1'].rootAssembly
region2=a1.instances['Part-model-1'].sets['Set-right']
mdb.models['Model-1'].Coupling(name='Constraint-right', controlPoint=region1,
    surface=region2, influenceRadius=WHOLE_SURFACE, couplingType=KINEMATIC,
    localCsys=None, u1=ON, u2=ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)

########边界条件
a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[r1.keys()[1]], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='BC-left', createStepName='Step-1',
    region=region, u1=0.0, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0,
    amplitude=UNSET, fixed=OFF, distributionType=UNIFORM, fieldName='',
    localCsys=None)

###载荷
disValue = modelData['disValue']
mdb.models['Model-1'].TabularAmplitude(name='Amp-1', timeSpan=STEP,
    smooth=SOLVER_DEFAULT, data=((0.0, 0.0), (1.0, 1.0)))
a3 = mdb.models['Model-1'].rootAssembly
r1 = a3.referencePoints
refPoints1=(r1[r1.keys()[0]], )
region = regionToolset.Region(referencePoints=refPoints1)
mdb.models['Model-1'].DisplacementBC(name='BC-right', createStepName='Step-1',
    region=region, u1=disValue, u2=0.0, u3=0.0, ur1=0.0, ur2=0.0, ur3=0.0,
    amplitude='Amp-1', fixed=OFF, distributionType=UNIFORM, fieldName='',
    localCsys=None)

####mesh
p = mdb.models['Model-1'].parts['Part-model']
p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                    point1=(0, 0, 0),
                                    point2=(0,0,1),
                                    point3=(0,1,0))
#
p.PartitionCellByPlaneThreePoints(cells=p.cells,
                                    point1=(0,0,0),
                                    point2=(0,0,1),
                                    point3=(1,0,0))
############
p = mdb.models['Model-1'].parts['Part-model']
p.seedPart(size=4.0, deviationFactor=0.1, minSizeFactor=0.1)
c = p.cells
pickedRegions = c
# p.setMeshControls(regions=pickedRegions, technique=SWEEP,
#     algorithm=MEDIAL_AXIS)
p.generateMesh()
#####################
elemType1 = mesh.ElemType(elemCode=COH3D8, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=COH3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=UNKNOWN_TET, elemLibrary=STANDARD)
#
elemType4 = mesh.ElemType(elemCode=C3D8R, elemLibrary=STANDARD, 
    kinematicSplit=AVERAGE_STRAIN, secondOrderAccuracy=OFF, 
    hourglassControl=DEFAULT, distortionControl=DEFAULT)
elemType5 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType6 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
######
cohesiveCell = None
baseCesll = None
p = mdb.models['Model-1'].parts['Part-model']
allSets = p.sets.keys()

for i,setName in enumerate(allSets):
    pSet = p.sets[setName]
    
    if('cohesive' in setName.lower()):
        if(cohesiveCell == None):
            cohesiveCell = pSet.cells
        else:
            cohesiveCell += pSet.cells
            
    if("layer" in setName.lower()):
        if(baseCesll == None):
            baseCesll = pSet.cells
        else:
            baseCesll += pSet.cells
pickedRegions =(cohesiveCell,  )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,
    elemType3))

#
pickedRegions =(baseCesll,  )
p.setElementType(regions=pickedRegions, elemTypes=(elemType4, elemType5,
    elemType6))

#########

a = mdb.models['Model-1'].rootAssembly
r1 = a.referencePoints
refPoints1=(r1[r1.keys()[0]], )
a.Set(referencePoints=refPoints1, name='Set-res')
#: The set 'Set-res' has been created (1 reference point).
##############
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
    'RF', 'CSTRESS', 'EVF', 'SDV'))
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(
    numIntervals=200)
##############
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
regionDef=mdb.models['Model-1'].rootAssembly.sets['Set-res']
mdb.models['Model-1'].HistoryOutputRequest(name='H-Output-2', 
    createStepName='Step-1', variables=('U1', 'U2', 'U3', 'RF1', 'RF2', 'RF3'), 
    numIntervals=200, region=regionDef, sectionPoints=DEFAULT, rebar=EXCLUDE)
###########
####################
###for debug
#mdb.models['Model-1'].steps['Step-1'].setValues(massScaling=((SEMI_AUTOMATIC, 
#    MODEL, AT_BEGINNING, 1000.0, 0.0, None, 0, 0, 0.0, 0.0, 0, None), ), 
#    improvedDtMethod=ON)
#################
