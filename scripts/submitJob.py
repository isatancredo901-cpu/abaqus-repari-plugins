#-*- coding: utf-8 -*-
######################
modelData = globals()["modelData"]
jobName = modelData['jobName']
cpus = modelData['numOfCpus']
subroutineFile = modelData['mSubroutineFileKw']
mdb.Job(name=jobName, model='Model-1', description='', type=ANALYSIS,
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
    memoryUnits=PERCENTAGE, explicitPrecision=DOUBLE_PLUS_PACK,
    nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF,
    contactPrint=OFF, historyPrint=OFF, userSubroutine=subroutineFile, scratch='',
    resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=cpus,
    activateLoadBalancing=False, numThreadsPerMpiProcess=1,
    multiprocessingMode=DEFAULT, numCpus=cpus)
#
mdb.jobs[jobName].submit(consistencyChecking=OFF)