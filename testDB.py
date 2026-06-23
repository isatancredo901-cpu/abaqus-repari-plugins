#-*- coding:utf-8 -*-
from abaqusGui import *
import json
import numpy as np
import os
###########################################################################
# Class definition
###########################################################################
thisPath = os.path.abspath(__file__)
thisDir = os.path.dirname(thisPath)

def TEXT(s = "测试"):
    return s.decode('utf-8').encode('gbk')
  

class TestDB(AFXDataDialog):
    [
        ID_CLICKED_CREATE_MODEL,
        ID_CLICKED_UPDATE_MATERIAL,
        ID_CLICKED_UPDATE_MODEL,
        ID_CLICKED_SELECT_MATRIAL,
        ID_CLICKED_PARSEODB,
        ID_CLICKED_UPDATE_BC,
        ID_LOAD_CSV,
        ID_DATA_PREVIEW,
        ID_CLICKED_SUBMIT,
        
    ] = range(AFXDataDialog.ID_LAST, AFXDataDialog.ID_LAST + 9)
    def __init__(self, form):
        AFXDataDialog.__init__(self, form, 'composite_Repair_Strength_Analysis V1.0',
          0, # DECOR_RESIZE|DIALOG_ACTIONS_SEPARATOR,
         w=800,h=500)
        ##
        self.form = form
        ###
        self.dataDict = {}

        #functions

        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_CREATE_MODEL,TestDB.omCmdSelectCreateModel)        ## 创建模型
        FXMAPFUNC(self, SEL_COMMAND, self.ID_LOAD_CSV,TestDB.omCmdLoadCSV) #加载csv
        FXMAPFUNC(self, SEL_COMMAND, self.ID_DATA_PREVIEW,TestDB.omCmdDataPreview) #数据预览
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_UPDATE_MODEL,TestDB.omCmdUpdateModel)#更新模型
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_UPDATE_MATERIAL,TestDB.omCmdUpdateMaterial)#更新模型
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_PARSEODB,TestDB.omCmdParseODB)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_UPDATE_BC,TestDB.omCmdUpdateBC)
        FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_SUBMIT,TestDB.omCmdSelectSubmit)
        ###
        self.form.pluginDir.setValue(thisDir)
        # FXMAPFUNC(self, SEL_COMMAND, self.ID_CLICKED_AUTOMATIC, TestDB.omCmdSelectAutomatic)
        ###
        ###################
        ### First page  ###
        length = 12
        ###################
        tabBook1 = FXTabBook(self, None, 0, LAYOUT_FILL_X|LAYOUT_FILL_Y)
        FXTabItem(tabBook1, TEXT("模型参数设置"))
        #                                                               x  y  w  h  pl pr pt pb
        tab1Frame = FXVerticalFrame(tabBook1, FRAME_RAISED | FRAME_SUNKEN, 0, 0, 0, 0, 4, 10, 7, 5)
        # tabBook2 = FXTabBook(tab1Frame, None, 0, LAYOUT_FILL_X)
        # For modeling dimensionality
        
        
        #########第一个页面
        # 创建一个 GroupBox，标题为 a
        GroupBox_a = FXGroupBox(p=tab1Frame, text=TEXT("模型参数设置"),opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        row1 = FXHorizontalFrame(GroupBox_a)
        aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        AFXTextField(aligner, length, TEXT("长度:"),form.mLength)
        self.plate_layer_thickness=AFXTextField(aligner, length, TEXT("铺层厚度:"),form.mThickness)
        AFXTextField(aligner,length, TEXT("凹坑直径:"),form.mPitDiameter)
        ########
        aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        AFXTextField(aligner, length, TEXT("宽度:"),form.mWidth)
        self.plate_layer_num=AFXTextField(aligner,length, TEXT("铺层数量:"),form.mNumLayer)
        #proce
        aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        self.plate_height = AFXTextField(aligner, length, TEXT("高度:"),form.mHeight)
        self.plate_glue_thickness=AFXTextField(aligner,length, TEXT("胶结层厚度:"),form.glueThickness)
        self.plate_height.disable()
        #
        aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        # AFXTextField(aligner, length, labelText=TEXT("长度sss:"))
       
        #
        aligner = AFXVerticalAligner(GroupBox_a, pl=0, pr=0, pt=0, pb=0)
        AFXTextField(aligner, 88, TEXT("铺层角度："),form.mLayerAngle)
        ####
        # FXLabel(aligner, TEXT("修补参数:"), ic=None, opts=LABEL_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        
        GroupBox_c = FXGroupBox(tab1Frame, text=TEXT("修补参数设置"),opts=FRAME_GROOVE|LAYOUT_FILL_X,h=198) #|LAYOUT_FIX_HEIGHT,h=180
        #
        row1 = FXHorizontalFrame(GroupBox_c)
        FXLabel(row1, TEXT("选择修补类型:"), ic=None, opts=LABEL_NORMAL, x=0, y=0, w=0, h=0, pl=DEFAULT_PAD, pr=DEFAULT_PAD, pt=DEFAULT_PAD, pb=DEFAULT_PAD)
        #
        
        
        sw1 = FXSwitcher(row1)

        FXRadioButton(row1,TEXT('贴补式'), sw1, FXSwitcher.ID_OPEN_FIRST, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 6, 0, 3, 5)
        FXRadioButton(row1,TEXT('阶梯式'), sw1,FXSwitcher.ID_OPEN_FIRST+1, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 100, 0,3, 5)
        FXRadioButton(row1,TEXT('斜接式'), sw1, FXSwitcher.ID_OPEN_FIRST+2, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL, 0, 0, 0, 0, 85, 0, 3, 5)
        #############
        # 创建修补参数 TabBook（先不添加Tab项，动态添加）
        # 创建三个独立的 GroupBox，分别放置三种修补参数
        # ========== 贴补参数 GroupBox ==========
        self.tb_group = FXGroupBox(GroupBox_c, text=TEXT("贴补参数"),
                                opts=FRAME_GROOVE | LAYOUT_FILL_X)
        tb_aligner = AFXVerticalAligner(self.tb_group, pl=0, pr=0, pt=0, pb=0)

        row_tb1 = FXHorizontalFrame(tb_aligner, LAYOUT_FILL_X)
        
        ###
        # 贴补类型 Radio 按钮组
        FXLabel(row_tb1, TEXT("贴补类型:"), None, LAYOUT_CENTER_Y, pl=0, pr=10)
        self.tb_type_sw = FXSwitcher(row_tb1)
        self.tb_type_double = FXRadioButton(row_tb1, TEXT("双面贴补"), self.tb_type_sw, 
                                                FXSwitcher.ID_OPEN_FIRST, LAYOUT_SIDE_LEFT | RADIOBUTTON_NORMAL, pl=0, pr=10)
        # self.tb_type_single = FXRadioButton(row_tb1, TEXT("单面贴补"), self.tb_type_sw, 
        #                                         FXSwitcher.ID_OPEN_FIRST+1, LAYOUT_SIDE_LEFT | RADIOBUTTON_NORMAL, pl=0, pr=10)
    
        self.tb_type_sw.setCurrent(0)  # 默认单面贴补
        ##
        FXLabel(row_tb1, TEXT("贴补形状:"), None, LAYOUT_CENTER_Y, pl=0, pr=10)
        self.tb_shape_sw = FXSwitcher(row_tb1)
        self.tb_shape_circle = FXRadioButton(row_tb1, TEXT("圆形贴补"), self.tb_shape_sw, 
                                                FXSwitcher.ID_OPEN_FIRST, LAYOUT_SIDE_LEFT | RADIOBUTTON_NORMAL, pl=0, pr=10)
        # self.tb_shape_rectangle = FXRadioButton(row_tb1, TEXT("矩形贴补"), self.tb_shape_sw, 
        #                                         FXSwitcher.ID_OPEN_FIRST + 1, LAYOUT_SIDE_LEFT | RADIOBUTTON_NORMAL, pl=0, pr=10)
        self.tb_shape_sw.setCurrent(0)  # 默认单面贴补

        row_tb1 = FXHorizontalFrame(tb_aligner, LAYOUT_FILL_X)
        


        #########

        
        AFXTextField(row_tb1, 10, TEXT("铺层数量:"), self.form.tbLayerNum,
                    opts=AFXTEXTFIELD_INTEGER | LAYOUT_CENTER_Y)
        AFXTextField(row_tb1, 10, TEXT("胶层厚度(mm):"), self.form.glueThickness,
                    opts=AFXTEXTFIELD_FLOAT | LAYOUT_CENTER_Y)
        
        self.tbWidth = AFXTextField(row_tb1, 10, TEXT("宽度(mm):"), self.form.tbWidth,
                    opts=AFXTEXTFIELD_FLOAT | LAYOUT_CENTER_Y)
        self.tbHeight = AFXTextField(row_tb1, 10, TEXT("高度(mm):"), self.form.tbHeight,
                    opts=AFXTEXTFIELD_FLOAT | LAYOUT_CENTER_Y)

        row_tb2 = FXHorizontalFrame(tb_aligner, LAYOUT_FILL_X)
        AFXTextField(row_tb2, 60, TEXT("补片铺层角度:"), self.form.tbLayerAngle,
                    opts=AFXTEXTFIELD_STRING | LAYOUT_CENTER_Y)

        # ========== 阶梯参数 GroupBox ==========
        self.jt_group = FXGroupBox(GroupBox_c, text=TEXT("阶梯参数"),
                                opts=FRAME_GROOVE | LAYOUT_FILL_X)
        jt_aligner = AFXVerticalAligner(self.jt_group, pl=0, pr=0, pt=0, pb=0)

        row_jt1 = FXHorizontalFrame(jt_aligner, LAYOUT_FILL_X)
        AFXTextField(row_jt1, 10, TEXT("阶梯数量:"), self.form.jtNum,
                    opts=AFXTEXTFIELD_INTEGER | LAYOUT_CENTER_Y)
        AFXTextField(row_jt1, 10, TEXT("胶层厚度(mm):"), self.form.glueThickness,
                    opts=AFXTEXTFIELD_FLOAT | LAYOUT_CENTER_Y)

        # ========== 斜接参数 GroupBox ==========
        self.xj_group = FXGroupBox(GroupBox_c, text=TEXT("斜接参数"),
                                opts=FRAME_GROOVE | LAYOUT_FILL_X)
        xj_aligner = AFXVerticalAligner(self.xj_group, pl=0, pr=0, pt=0, pb=0)

        row_xj1 = FXHorizontalFrame(xj_aligner, LAYOUT_FILL_X)
        AFXTextField(row_xj1, 10, TEXT("斜接角度(°):"), self.form.xjAngle,
                    opts=AFXTEXTFIELD_FLOAT | LAYOUT_CENTER_Y)
        AFXTextField(row_xj1, 10, TEXT("胶层厚度(mm):"), self.form.glueThickness,
                    opts=AFXTEXTFIELD_FLOAT | LAYOUT_CENTER_Y)

        # 初始隐藏阶梯和斜接，只显示贴补
        # self.jt_group.hide()
        # self.xj_group.hide()

        # FXButton(p=self, text='Create Model',
        #  tgt=self.form.cmd_create, sel=AFXMode.ID_ACTIVATE)
        GroupBox_b = FXGroupBox(p=tab1Frame, text=TEXT("材料参数设置"),opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        row1 = FXHorizontalFrame(GroupBox_b)
        aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        
        # 2. 文本输入框
        #File Selector
        fileHandler = FileDBFileHandler(form, 'mMaterialFile', ' (*.json)',TEXT("选择材料数据文件"))
        File_Text = AFXTextField(p=row1, ncols=56, labelText=TEXT('材料json文件:'), tgt=form.mMaterialFileKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=row1, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
        ######
        FXButton(
            p=row1,
            text=TEXT('加载材料参数'),
            tgt=self,
            sel=self.ID_DATA_PREVIEW,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y
        )

   
    #####################
     # 创建主布局
        group_box = FXGroupBox(tab1Frame, TEXT("材料参数汇总"), FRAME_GROOVE | LAYOUT_FILL_X )
        
        # 创建文本显示区域（放在 GroupBox 内）
        self.text_area = FXText(group_box, None, 0, LAYOUT_FILL_X)
        self.text_area.setEditable(True)
    
    #####################

            
        # 创建一个水平容器
        #  tabBook1
        button_row = FXHorizontalFrame(tab1Frame, LAYOUT_FILL_X, 
                                        x=0, y=0, w=0, h=0, 
                                        pl=10, pr=10, pt=5, pb=5)

        # 在水平容器中添加按钮
        FXButton(button_row, TEXT("创建几何模型"), None, self, self.ID_CLICKED_CREATE_MODEL,
                opts=BUTTON_NORMAL | LAYOUT_CENTER_X,
                x=0, y=0, w=0, h=0, pl=10, pr=10)

        FXButton(button_row, TEXT("更新几何模型"), None, self, self.ID_CLICKED_UPDATE_MODEL,
                opts=BUTTON_NORMAL | LAYOUT_CENTER_X,
                x=0, y=0, w=0, h=0, pl=10, pr=10)
        
 
        FXButton(button_row, TEXT("更新材料参数"), None, self, self.ID_CLICKED_UPDATE_MATERIAL,
                opts=BUTTON_NORMAL | LAYOUT_CENTER_X,
                x=0, y=0, w=0, h=0, pl=10, pr=10)

        
        # GroupBox_b = FXGroupBox(p=tab1Frame, text=TEXT("材料参数预览"),opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        # row1 = FXHorizontalFrame(GroupBox_b)
        # aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        # mat_preview = FXText(GroupBox_b, tgt=None,  opts=LAYOUT_FILL_X,x=0, y=0, h=120)
        # mat_preview.appendText(TEXT("材料参数预览"),len(TEXT("材料参数预览")))


        ###########################################
        ###################
        ### Second page ###
        ###################
         # 创建标签页

        
        ##########################边界条件
        FXTabItem(tabBook1, TEXT('边界条件和求解设置'))
        #                                                              x  y  w  h  pl pr pt pb
        tab2Frame = FXVerticalFrame(tabBook1, FRAME_RAISED | FRAME_SUNKEN, 0, 0, 0, 0, 4, 10, -7, 5)
        tabBook2 = FXTabBook(tab2Frame, None, 0, LAYOUT_FILL_X)
        va = AFXVerticalAligner(tab2Frame)
        # 创建一个 GroupBox，标题为 a
        GroupBox_a = FXGroupBox(tab2Frame, text=TEXT("边界条件设置"),opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        row1 = FXHorizontalFrame(GroupBox_a)
        aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        input_row = FXHorizontalFrame(row1, LAYOUT_FILL_X, 
                              x=0, y=0, w=0, h=0,
                              pl=10, pr=10, pt=5, pb=5)
        # 
        AFXTextField(input_row, 12, TEXT("左右间距:"),tgt=form.lrGap)
        self.tbGap = AFXTextField(input_row, 12, TEXT("上下间距:"),tgt = form.tbGap)
        self.tbGap.disable()
        AFXTextField(input_row, 12, TEXT("载荷值:"),tgt = form.disValue)
        
        ###########
        self.compressBc  = FXCheckButton(
        input_row,                          # 父窗口
        TEXT("压缩(默认是拉伸)"),                  # 标签文
            )
        #
        self.compressBc.hide()
        #
                
        # #
        # button_row = FXHorizontalFrame(tab2Frame, LAYOUT_FILL_X, 
        #                                 x=0, y=0, w=0, h=0, 
        #                                 pl=10, pr=10, pt=5, pb=5)

        # # 在水平容器中添加按钮
        # FXButton(button_row, TEXT("创建几何模型"), None, self, self.ID_CLICKED_CREATE_MODEL,
        #         opts=BUTTON_NORMAL | LAYOUT_CENTER_X,
        #         x=0, y=0, w=0, h=0, pl=10, pr=10)

        # FXButton(button_row, TEXT("更新几何模型"), None, self, self.ID_CLICKED_UPDATE_MODEL,
        #         opts=BUTTON_NORMAL | LAYOUT_CENTER_X,
        #         x=0, y=0, w=0, h=0, pl=10, pr=10)
        
 
        FXButton(input_row, TEXT("更新边界条件"), None, self, self.ID_CLICKED_UPDATE_BC,
                opts=BUTTON_NORMAL | LAYOUT_CENTER_X,
                x=0, y=0, w=0, h=0, pl=10, pr=10)
     
        ############

                #
        GroupBox_a = FXGroupBox(tab2Frame, text=TEXT("求解设置"),opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        container = FXVerticalFrame(GroupBox_a)
        row1 = FXHorizontalFrame(container)
        #aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0)
        kd_bp_input= AFXTextField(row1, length, labelText=TEXT("Job名称:"),tgt=form.jobName,x=0,y=0,w=0,h=0,pl=20,pr=50)
        kd_bp_input= AFXTextField(row1, length, labelText=TEXT("CPU数量:"),tgt = form.numOfCpus,x=0,y=0,w=0,h=0,pl=20,pr=20)
        ################################
        row2 = FXHorizontalFrame(container)
                        #File Selector
        fileHandler = FileDBFileHandler(form, 'mSubroutineFile', ' (*.for)',TEXT("选择Fortran子程序文件"))
        File_Text = AFXTextField(p=row2, ncols=56, labelText=TEXT('子程序Fortran文件:'), tgt=form.mSubroutineFileKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=row2, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y, x=0, y=0, w=0, h=0, pl=1, pr=1, pt=1, pb=1)
        
        

        
        
        vf = FXVerticalFrame(tab2Frame, 0, 0, 0, 0, 0, 12, 10, 10, 10)
        va = AFXVerticalAligner(tab2Frame)
        vh = FXHorizontalFrame(va)
        
        # FXButton(vh, TEXT("创建模型"),None, self, self.ID_CLICKED_MANUAL,x=0, y=0, w=0, h=0,pl=20,pr=20)
        FXButton(vh, TEXT("提交计算"),None, self, self.ID_CLICKED_SUBMIT,x=0, y=0, w=0, h=0,pl=20,pr=20)
        #######
        
        
        
        
        ###########################
        
        
        
        
        #结果page 页面
        FXTabItem(tabBook1, TEXT('结果计算'))
        #                                                              x  y  w  h  pl pr pt pb
        tab2Frame = FXVerticalFrame(tabBook1, FRAME_RAISED | FRAME_SUNKEN, 0, 0, 0, 0, 4, 10, -7, 5)
        tabBook2 = FXTabBook(tab2Frame, None, 0, LAYOUT_FILL_X)
        va = AFXVerticalAligner(tab2Frame)
        
        GroupBox_a = FXGroupBox(tab2Frame, text=TEXT("求解类型"),opts=FRAME_GROOVE|LAYOUT_FILL_X)
        #
        row1 = FXVerticalFrame(GroupBox_a)
        aligner = FXHorizontalFrame(row1, pl=0, pr=0, pt=0, pb=0,opts=LAYOUT_FILL_X)
        
        # 2. 文本输入框
        fileHandler = FileDBFileHandler(form, 'mOdbFile', ' (*.odb)',TEXT("选择结果ODB文件"))
        File_Text = AFXTextField(p=aligner, ncols=46, labelText=TEXT('结果ODB文件:'), tgt=form.mOdbFileKw, sel=0,
            opts=AFXTEXTFIELD_STRING|LAYOUT_CENTER_Y,pl=30)
        icon = afxGetIcon('fileOpen', AFX_ICON_SMALL )
        FXButton(p=aligner, text='	Select File\nFrom Dialog', ic=icon, tgt=fileHandler, sel=AFXMode.ID_ACTIVATE,
            opts=BUTTON_NORMAL|LAYOUT_FILL_X|LAYOUT_CENTER_Y)
        
                
        FXButton(
            p=aligner,
            text=TEXT('提交后处理'),
            tgt=self,
            sel=self.ID_CLICKED_PARSEODB,
            opts=BUTTON_NORMAL|LAYOUT_CENTER_Y
        )
        
        
        #############
        #########
        aligner = FXHorizontalFrame(row1, pl=0, pr=0, pt=0, pb=0)
        sw2 = FXSwitcher(aligner)
        FXLabel(aligner, TEXT("设置分析类型:"),x=0,y=0,w=0,h=0,pt=2)
        rdb_stiffness = FXRadioButton(aligner,TEXT('刚度'), sw2, FXSwitcher.ID_OPEN_FIRST, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL,0, 0, 0, 0, 6, 0, 2, 5)
        # rdb_risk = FXRadioButton(aligner,TEXT('屈曲载荷'), sw2,FXSwitcher.ID_OPEN_FIRST+1, LAYOUT_SIDE_LEFT|RADIOBUTTON_NORMAL,0, 0, 0, 0, 50, 50,2, 5)
        
        # self.XP_btn = FXButton(aligner, TEXT('计算'),None, self, self.ID_CLICKED_MANUAL,x=0, y=0, w=0, h=0,pl=20,pr=20)
        
                                     

         # 创建一个 GroupBox，标题为 a
        GroupBox_a = FXGroupBox(tab2Frame, text=TEXT("结果显示"),opts=FRAME_GROOVE|LAYOUT_FILL_X|LAYOUT_FILL_Y)
        row1 = FXHorizontalFrame(GroupBox_a,opts=AFXTABLE_EDITABLE|LAYOUT_FILL_X|LAYOUT_FILL_Y)
        aligner = AFXVerticalAligner(row1, pl=0, pr=0, pt=0, pb=0,opts=AFXTABLE_EDITABLE|LAYOUT_FILL_X|LAYOUT_FILL_Y)
        table = AFXTable(aligner, 1, 4, 1, 4, None, 0, AFXTABLE_EDITABLE|LAYOUT_FILL_X|LAYOUT_FILL_Y)
        table.setPopupOptions(AFXTable.POPUP_CUT|AFXTable.POPUP_COPY|AFXTable.POPUP_DELETE_ROW|AFXTable.POPUP_CLEAR_CONTENTS|AFXTable.POPUP_WRITE_TO_FILE)
        table.setLeadingRows(1)
        table.setLeadingColumns(1)
        table.setColumnWidth(1, 100)
        table.setColumnType(1, AFXTable.TEXT)
        table.setColumnWidth(2, 100)
        table.setColumnType(2, AFXTable.TEXT)
        table.setColumnWidth(3, 100)
        table.setColumnType(3, AFXTable.FLOAT)
        table.setLeadingRowLabels('Job Name\tType\tValue')
        table.setStretchableColumn( table.getNumColumns()-1 )
        table.showHorizontalGrid(True)
        table.showVerticalGrid(True)
        ####
        self.table = table
        ################################################
        #
        self.form = form
        #########
        self.sw1 = sw1
        self.sw2 = sw2
        self.modifyType = form.modifyType #修补类型
        
   
        
        # self.r_hd_jc_input = hd_jc_input #胶层厚度
        # self.r_num_jt_input = num_jt_input #阶梯-数目
        # self.r_jd_jt_input = jd_jt_input #阶梯-角度
        
        # #
        # self.r_num_bp_input = num_bp_input #补片-数量
        # self.r_hd_bp_input = hd_bp_input # 补片-厚度
        
        #########后处理
        self.parseOdbType = form.parseOdbType
        
        ########
        self.isFirst = True
        self.dataPreviewDB = None
        return
    
    def getMatParams(self):
        jsonData = self.text_area.getText()
        self.form.matParaDict.setValue(jsonData)
        
        return
    
    
    def omCmdUpdateBC(self, sender, sel, ptr):
        self.getMatParams()
        self.form.cmdType.setValue("updateBC")
        self.form.issueCommands() 
        return
    
    
    
    def omCmdUpdateModel(self, sender, sel, ptr):
        self.getMatParams()
        self.form.cmdType.setValue("updateModel")
        self.form.issueCommands() 
        return
    
    def omCmdUpdateMaterial(self, sender, sel, ptr):
        self.getMatParams()
        self.form.cmdType.setValue("updateMaterial")
        self.form.issueCommands() 
        return
    ##加载csv文件
    def omCmdLoadCSV(self, sender, sel, ptr):
        return
    def omCmdDataPreview(self, sender, sel, ptr):
        jsonFile = self.form.mMaterialFileKw.getValue()
        self.form.showMessage(jsonFile)
        with open(jsonFile,'r') as f:
            matDataString = f.read()
        matString_compact = json.dumps(json.loads(matDataString), separators=(',', ':'))

        self.text_area.setText(matString_compact)
        return
    
        
    
    #####解析odb结果
 
    def omCmdParseODB(self, sender, sel, ptr):
        self.form.cmdType.setValue("parseODB")
        # self.form.issueCommands() 
        self.form.showMessage("parseod")
        data = np.loadtxt("Force.txt")
        ##################
        data = np.loadtxt("Force.txt")
        forces = data[:, 1]
        max_force = np.max(forces)
        ###################
        jobName = self.form.mOdbFileKw.getValue()
        basename = os.path.basename(jobName)           # Job-test.odb
        jobName_without_ext = os.path.splitext(basename)[0]
        ##################
        index = self.form.parseOdbType.getValue()
        type = [TEXT("刚度计算"),TEXT("强度计算")][index]
        ####
        rows = self.table.getNumRows()
        current_rows = rows
        self.table.insertRows(current_rows, 1)
        
        ###
        self.table.setItemValue(rows, 1, jobName_without_ext)
        self.table.setItemValue(current_rows, 2, type)
        self.table.setItemValue(current_rows, 3, str(max_force))
        
        ###
        self.form.showMessage(str(rows))
        return

    
    def processUpdates(self):
        ################
        nLayer = self.form.mNumLayer.getValue()
        layerThickness = self.form.mThickness.getValue()
        glueThickness = self.form.glueThickness.getValue()
        height = nLayer*layerThickness
        if(nLayer > 1):
            height += glueThickness * (nLayer-1)
        
        self.form.mHeight.setValue(height)
        
        # self.form.showMessage(str(height))
        

        
        
        #################
        # self.getMatParams()
        current = self.sw1.getCurrent()
        self.form.modifyType.setValue(current)
        
        # 根据选择的类型显示对应的 GroupBox
        if current == 0:  # 贴补式
            self.tb_group.show()
            self.jt_group.hide()
            self.xj_group.hide()
        elif current == 1:  # 阶梯式
            self.tb_group.hide()
            self.jt_group.show()
            self.xj_group.hide()
        elif current == 2:  # 斜接式
            self.tb_group.hide()
            self.jt_group.hide()
            self.xj_group.show()
            
        ##############
        type = self.tb_type_sw.getCurrent()
        self.form.tbType.setValue(type)
        shape = self.tb_shape_sw.getCurrent()
        self.form.tbShape.setValue(shape)
        if(shape == 0):
            self.tbHeight.hide()
            self.tbWidth.setLabelText(TEXT("半径(mm):"))
            pass
        elif(shape == 1):
            self.tbWidth.setLabelText(TEXT("宽度(mm):"))
            self.tbHeight.show()
        
        ##考虑压缩边界
        f = self.compressBc.getCheck()
        i = 0
        if(f):i=1
        self.form.pressBC.setValue(i)
        
        # 后处理类型
        if self.sw2.getCurrent() == 0:
            self.parseOdbType.setValue(0)
        elif self.sw2.getCurrent() == 1:
            self.parseOdbType.setValue(1)
            
            
    ##加载材料
    def omCmdSelectLoadMaterial(self, sender, sel, ptr):
        return
    


    ##创建模型
    def omCmdSelectCreateModel(self, sender, sel, ptr):
        self.getMatParams()
        self.form.cmdType.setValue("createModel")
        self.form.showMessage("create...")
        self.form.issueCommands() 
        return 
    
    ###设置材料
    
    
    
    ##计算求解
    def omCmdSelectSubmit(self, sender, sel, ptr):
        self.form.cmdType.setValue("submitJob")
        self.form.issueCommands() 
        return
    
    ###施加边界条件method A
    def omCmdSelectApplyBC(self, sender, sel, ptr):
        self.form.cmdType.setValue("applyBC")
        self.form.issueCommands() 
        return
    
    ##时间边界条件 method B

    
    ###后处理
    def omCmdSelectPostProcess(self, sender, sel, ptr):
        self.form.cmdType.setValue("postProcess")
        self.form.issueCommands() 
        return
    
    
    

    
    


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def show(self):
        
        # Note: This method is only necessary because the prototype
        # application allows changes to be made in the dialog code and
        # reloaded while the application is still running. Normally you
        # would not need to have a show() method in your dialog.
        
        # Resize the dialog to its default dimensions to account for
        # any widget changes that may have been made.
        #
        self.resize(self.getDefaultWidth(), self.getDefaultHeight())
        AFXDataDialog.show(self)


####################


###########################################################################
# Class definition
###########################################################################

class Composite_Repair_Strength_AnalysisDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*'):
        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, Composite_Repair_Strength_AnalysisDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):
       fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), 'Select a File',
           self.filenameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
       fileDb.setReadOnlyPatterns('*.odb')
       fileDb.create()
       fileDb.showModal()

############文件选择

class FileDBFileHandler(FXObject):

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __init__(self, form, keyword, patterns='*',title="Select a File"):
        self.titleKw = title

        self.form = form
        self.patterns = patterns
        self.patternTgt = AFXIntTarget(0)
        exec('self.fileNameKw = form.%sKw' % keyword)
        self.readOnlyKw = AFXBoolKeyword(None, 'readOnly', AFXBoolKeyword.TRUE_FALSE)
        FXObject.__init__(self)
        FXMAPFUNC(self, SEL_COMMAND, AFXMode.ID_ACTIVATE, FileDBFileHandler.activate)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def activate(self, sender, sel, ptr):
        
        print(self.patterns,self.patternTgt,self.fileNameKw)
        
        fileDb = AFXFileSelectorDialog(getAFXApp().getAFXMainWindow(), self.titleKw,
           self.fileNameKw, self.readOnlyKw,
           AFXSELECTFILE_ANY, self.patterns, self.patternTgt)
        fileDb.setReadOnlyPatterns('*.csv')
        fileDb.create()
        fileDb.showModal()
