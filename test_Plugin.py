#-*- coding: utf-8 -*-
#插件注册
from abaqusGui import *
from abaqusConstants import ALL
import os
from testForm import TestForm
 
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

toolset = getAFXApp().getAFXMainWindow().getPluginToolset()
toolset.registerGuiMenuButton(
                              buttonText='Composite_Repair_Strength_Analysis V1.0',
                              object=TestForm(toolset),
                              messageId=AFXMode.ID_ACTIVATE,
                              icon=None,
                              kernelInitString='import RSGen_Master',
                              applicableModules=ALL,
                              version='N/A',
                              author='ASKCAE Group.',
                              description='composite_Repair_Strength_Analysis' ,
                              helpUrl='N/A'
                              )