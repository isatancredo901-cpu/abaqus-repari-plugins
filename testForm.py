
#-*- coding: utf-8 -*-
import importlib
from abaqusGui import *
import testDB
# Note: The above form of the import statement is used for the prototype
# application to allow the module to be reloaded while the application is
# still running. In a non-prototype application you would use the form:
# from myDB import MyDB

#

###########################################################################
# Class definition
###########################################################################

class TestForm(AFXForm):
    [
        ID_WARNING,
    ] = range(AFXForm.ID_LAST, AFXForm.ID_LAST + 1)
    def __init__(self, owner):

        AFXForm.__init__(self, owner)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_WARNING,
                  TestForm.onCmdWarning)
        # Command
        # self.cmd = AFXGuiCommand(self, 'myCommand', 'myObject')
                # 创建三个命令，对应同一个对象但不同方法
        self.cmd = AFXGuiCommand(self, method='execute', 
                                       objectName='RSGen_Master', registerQuery=False)
        
        self.pluginDir = AFXStringKeyword(self.cmd, 'pluginDir', TRUE,"")
        self.cmdType = AFXStringKeyword(self.cmd, 'cmdType', TRUE, "CREATE")
        # Create the command and keywords.模型参数
        # self.cmd = AFXGuiCommand(self, method='execute', objectName='RSGen_Master', registerQuery=False)
        ##
        
        #基板参数
        self.mLength = AFXFloatKeyword(self.cmd, 'mLength', TRUE, 150, 8)
        self.mWidth = AFXFloatKeyword(self.cmd, 'mWidth', TRUE, 100, 8)
        self.mHeight = AFXFloatKeyword(self.cmd, 'mHeight', TRUE, 0, 8)
        # self.mLayerThichness = AFXFloatKeyword(self.cmd, 'mLayerThichness', TRUE, 0.125, 8)
        self.mThickness = AFXFloatKeyword(self.cmd, 'mThickness', TRUE, 0.125, 8)
        self.mNumLayer = AFXIntKeyword(self.cmd, 'mNumLayer', TRUE,32)
        self.mLayerAngle = AFXStringKeyword(self.cmd, 'mLayerAngle', TRUE, '45/0/45/90/45/0/45/90/45/0/45/90/45/0/45/90/90/-45/0/45/90/-45/0/45/90/-45/0/45/90/-45/0/45')
        self.mPitDiameter = AFXFloatKeyword(self.cmd, 'mPitDiameter', TRUE, 10, 8)
        ########材料文件参数
        self.mMaterialFileKw = AFXStringKeyword(self.cmd, 'mMaterialFileKw', TRUE, '')
        self.mOdbFileKw = AFXStringKeyword(self.cmd, 'mOdbFileKw', TRUE, '')
        ########修补参数
        self.modifyType = AFXIntKeyword(self.cmd, 'modifyType', TRUE, 0)
        #补片
        self.tbWidth = AFXFloatKeyword(self.cmd, 'tbWidth', TRUE, 20, 8)
        self.tbHeight = AFXFloatKeyword(self.cmd, 'tbHeight', TRUE, 20, 8)
        self.tbLayerNum = AFXIntKeyword(self.cmd, 'tbLayerNum', TRUE, 8)
        self.tbLayerAngle = AFXStringKeyword(self.cmd, 'tbLayerAngle', TRUE, '45/0/-45/90/90/-45/0/45')
        self.glueThickness = AFXFloatKeyword(self.cmd, 'glueThickness', TRUE, 0.1, 8)
        #阶梯
        self.jtNum = AFXIntKeyword(self.cmd, 'jtNum', TRUE, 4)
        #斜接
        self.xjAngle = AFXFloatKeyword(self.cmd, 'xjAngle', TRUE, 10, 8)
        
        
        ###边界条件参数
        self.lrGap = AFXFloatKeyword(self.cmd, 'lrGap', TRUE, 1.2)
        self.tbGap = AFXFloatKeyword(self.cmd, 'tbGap', TRUE, 0)
        # self.fixCondition = AFXFloatKeyword(self.cmd, 'fixCondition', TRUE, 0.0, 8)
        # self.disCondition = AFXFloatKeyword(self.cmd, 'disCondition', TRUE, 0.0, 8)
        self.disValue = AFXFloatKeyword(self.cmd, 'disValue', TRUE, 1000)
        
        
        ##求解设置
        
        
        self.jobName = AFXStringKeyword(self.cmd, 'jobName', TRUE, 'Job-1')
        self.numOfCpus = AFXIntKeyword(self.cmd, 'numOfCpus', TRUE, 1)
        self.mSubroutineFileKw = AFXStringKeyword(self.cmd, 'mSubroutineFileKw', TRUE, '')

        
        #########后处理
        self.parseOdbType = AFXIntKeyword(self.cmd, 'parseOdbType', TRUE, 0)
        
        ###
        self.tableKw = AFXTableKeyword(self.cmd, 'tableKw', True,2)
        self.tableKw.setColumnType(0, AFXTABLE_TYPE_FLOAT)
        self.tableKw.setColumnType(1, AFXTABLE_TYPE_FLOAT)
        
        #
        self.matParaDict = AFXStringKeyword(self.cmd, 'matParaDict', True,"{}")
        
        ##
        self.tbType = AFXIntKeyword(self.cmd, 'tbType', TRUE, 0)
        self.tbShape = AFXIntKeyword(self.cmd, 'tbShape', TRUE, 0)
        self.pressBC = AFXIntKeyword(self.cmd, 'pressBC', TRUE, 0)
        #######################
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def getFirstDialog(self):

        # Note: The style below is used for the prototype application to 
        # allow the dialog to be reloaded while the application is
        # still running. In a non-prototype application you would use:
        #
        # return MyDB(self)
        
        # Reload the dialog module so that any changes to the dialog 
        # are updated.
        #
        importlib.reload(testDB)
        return testDB.TestDB(self)
    
    
    def showMessage(self, message):
        getAFXApp().getAFXMainWindow().writeToMessageArea(str(message))
   
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def issueCommands(self):
        cmd_str = self.cmdType
   
    
        # Since this is a prototype application, just write the command to
        # the Message Area so it can be visually verified. If you have 
        # defined a "real" command, then you can comment out this method to
        # have the command issued to the kernel.
        #
        # In a non-prototype application you normally do not need to write
        # the issueCommands() method.
        #
        cmds = self.getCommandString()
        getAFXApp().getAFXMainWindow().writeToMessageArea(cmds)
        
        # ##############
        self.deactivateIfNeeded()
        AFXForm.issueCommands(self)
   
        return TRUE
      
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def onCmdWarning(self, sender, sel, ptr):
        if sender.getPressedButtonId() == \
            AFXDialog.ID_CLICKED_YES:
                self.issueCommands()
                
                
