#-*- coding: utf-8 -*-
modelData = globals()["modelData"]
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