# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

__GUI_ver__ = "1.0.11"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        font = QtGui.QFont()
        font.setFamily("Arial")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("logo.JPG"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        
###Main Window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 670)
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(1100, 670))
        MainWindow.setMaximumSize(QtCore.QSize(1100, 670))
        MainWindow.setFont(font)
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowTitle("API Import Manager")
        
###Central Widget
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
###Groupbox for filters=================================================
        self.groupBox_Filter = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Filter.setGeometry(QtCore.QRect(10, 0, 360, 125))
        self.groupBox_Filter.setObjectName("groupBox_Filter")
        self.groupBox_Filter.setTitle("Select filter")  
        
        font.setBold(False)
###Line 1
        self.line_1 = QtWidgets.QFrame(self.groupBox_Filter)
        self.line_1.setGeometry(QtCore.QRect(0, 15, 360, 2))
        self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_1.setObjectName("line_1")
###Line 2
        self.line_2 = QtWidgets.QFrame(self.groupBox_Filter)
        self.line_2.setGeometry(QtCore.QRect(0, 55, 360, 2))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")        
###Label Filter
        self.label_Filter = QtWidgets.QLabel(self.groupBox_Filter)
        self.label_Filter.setGeometry(QtCore.QRect(5, 15, 130, 15))
        self.label_Filter.setFont(font)
        self.label_Filter.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Filter.setObjectName("label_Filter")
        self.label_Filter.setText("Filter")
###Label Condition
        self.label_Condition = QtWidgets.QLabel(self.groupBox_Filter)
        self.label_Condition.setGeometry(QtCore.QRect(140, 15, 80, 15))
        self.label_Condition.setFont(font)
        self.label_Condition.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Condition.setObjectName("label_Condition")
        self.label_Condition.setText("Condition")
###Label Value        
        self.label_Value = QtWidgets.QLabel(self.groupBox_Filter)
        self.label_Value.setGeometry(QtCore.QRect(225, 15, 130, 15))
        self.label_Value.setFont(font)
        self.label_Value.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Value.setObjectName("label_Value")
        self.label_Value.setText("Value")
###Combobox Filter
        self.comboBox_Filter = QtWidgets.QComboBox(self.groupBox_Filter)
        self.comboBox_Filter.setGeometry(QtCore.QRect(5, 30, 130, 20))
        self.comboBox_Filter.setStyleSheet("border: 1px solid gray;")
        self.comboBox_Filter.setObjectName("comboBox_Filter")
        self.comboBox_Filter.addItem("NONE")
        self.comboBox_Filter.addItem("Campaign Enable")
        self.comboBox_Filter.addItem("Campaign Name")
        self.comboBox_Filter.addItem("Campaign Description")
        self.comboBox_Filter.addItem("Dialing Mode")
        self.comboBox_Filter.addItem("Lines Per Agent")
        self.comboBox_Filter.addItem("Maximum Lines Per Agent")
        self.comboBox_Filter.addItem("Minimum Call Duration")
        self.comboBox_Filter.addItem("Abandon Calls Limit Enable")
        self.comboBox_Filter.addItem("Abandon Calls Limit Percent")
        self.comboBox_Filter.addItem("Campaign Prefix Digits")
        self.comboBox_Filter.addItem("No Answer Ring Limit")
        self.comboBox_Filter.addItem("Maximum Attempts")
        self.comboBox_Filter.addItem("No Answer Delay")
        self.comboBox_Filter.addItem("Busy Signal Delay")
        self.comboBox_Filter.addItem("Customer Abandoned Delay")
        self.comboBox_Filter.addItem("Dialer Abandoned Delay")
        self.comboBox_Filter.addItem("Answering Machine Delay")
        self.comboBox_Filter.addItem("Personalized Callback")
        self.comboBox_Filter.addItem("Campaign Type")
        self.comboBox_Filter.addItem("Enable CPA")
        self.comboBox_Filter.addItem("Enable IP AMD")
        self.comboBox_Filter.addItem("Start Hours")
        self.comboBox_Filter.addItem("Start Minutes")
        self.comboBox_Filter.addItem("Start Date")
        self.comboBox_Filter.addItem("End Hours")
        self.comboBox_Filter.addItem("End Minutes")
        self.comboBox_Filter.addItem("End Date")
###Combobox Condition
        self.comboBox_Condition = QtWidgets.QComboBox(self.groupBox_Filter)
        self.comboBox_Condition.setEnabled(False)
        self.comboBox_Condition.setGeometry(QtCore.QRect(140, 30, 80, 20))
        self.comboBox_Condition.setStyleSheet("border: 1px solid gray;")
        self.comboBox_Condition.setObjectName("comboBox_Condition")
###Combobox Value        
        self.comboBox_Value = QtWidgets.QComboBox(self.groupBox_Filter)
        self.comboBox_Value.setEnabled(False)
        self.comboBox_Value.setEditable(True)
        self.comboBox_Value.setGeometry(QtCore.QRect(225, 30, 130, 20))
        self.comboBox_Value.setObjectName("comboBox_Value")
        self.comboBox_Value.setStyleSheet("QComboBox{border: 1px solid gray; background-color : white;}\n"
										"QComboBox::drop-down{border: 0px;}\n"
                                        "QComboBox::down-arrow{image: url(noimg);border-width: 0px;}")
###PushButton Retrieve
        self.pushButton_Retrieve = QtWidgets.QPushButton(self.groupBox_Filter)
        self.pushButton_Retrieve.setEnabled(False)
        self.pushButton_Retrieve.setGeometry(QtCore.QRect(5, 65, 70, 25))
        self.pushButton_Retrieve.setFont(font)
        self.pushButton_Retrieve.setObjectName("pushButton_Retrieve")
        self.pushButton_Retrieve.setText("&Retrieve")
###СheckBox Overwrite 
        self.checkBox_Overwrite = QtWidgets.QCheckBox(self.groupBox_Filter)
        self.checkBox_Overwrite.setEnabled(False)
        self.checkBox_Overwrite.setGeometry(QtCore.QRect(80, 65, 70, 25))
        self.checkBox_Overwrite.setFont(font)
        self.checkBox_Overwrite.setObjectName("checkBox_Overwrite") 
        self.checkBox_Overwrite.setText("Overwrite")        
###PushButton Import
        self.pushButton_Import = QtWidgets.QPushButton(self.groupBox_Filter)
        self.pushButton_Import.setEnabled(False)
        self.pushButton_Import.setGeometry(QtCore.QRect(150, 65, 70, 25))
        self.pushButton_Import.setFont(font)
        self.pushButton_Import.setObjectName("pushButton_Import")
        self.pushButton_Import.setText("&Import")
###PushButton Clear Import
        self.pushButton_ClearImport = QtWidgets.QPushButton(self.groupBox_Filter)
        self.pushButton_ClearImport.setEnabled(False)
        self.pushButton_ClearImport.setGeometry(QtCore.QRect(225, 65, 70, 25))
        self.pushButton_ClearImport.setFont(font)
        self.pushButton_ClearImport.setObjectName("pushButton_ClearImport")
        self.pushButton_ClearImport.setText("Clear import")
###PushButton Download status
        self.pushButton_Download = QtWidgets.QPushButton(self.groupBox_Filter)
        self.pushButton_Download.setEnabled(False)
        self.pushButton_Download.setGeometry(QtCore.QRect(225, 93, 130, 25))
        self.pushButton_Download.setFont(font)
        self.pushButton_Download.setObjectName("pushButton_Download")
        self.pushButton_Download.setText("Download current status")         
###Label Separator
        self.label_Separator = QtWidgets.QLabel(self.groupBox_Filter)
        self.label_Separator.setGeometry(QtCore.QRect(5, 97, 105, 15))
        self.label_Separator.setFont(font)
        self.label_Separator.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Separator.setObjectName("label_Separator")
        self.label_Separator.setText("Symbol(s)-Separator:")
###LineEdit Separator        
        self.lineEdit_Separator = QtWidgets.QLineEdit(self.groupBox_Filter)
        self.lineEdit_Separator.setEnabled(True)
        self.lineEdit_Separator.setGeometry(QtCore.QRect(110, 95, 30, 20))
        self.lineEdit_Separator.setFont(font)
        self.lineEdit_Separator.setInputMethodHints(QtCore.Qt.ImhFormattedNumbersOnly)
        self.lineEdit_Separator.setMaxLength(4)
        self.lineEdit_Separator.setObjectName("lineEdit_Separator")
        self.lineEdit_Separator.setText("\\t")
###Label Separator2
        self.label_Separator2 = QtWidgets.QLabel(self.groupBox_Filter)
        self.label_Separator2.setGeometry(QtCore.QRect(130, 97, 95, 15))
        self.label_Separator2.setFont(font)
        self.label_Separator2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Separator2.setObjectName("label_Separator2")
        self.label_Separator2.setText("(type \\t for tab)")
###End Groupbox for filters=============================================

###Groupbox for Campaign List===========================================
        self.groupBox_Campaigns_List = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Campaigns_List.setGeometry(QtCore.QRect(10, 125, 360, 505))
        self.groupBox_Campaigns_List.setObjectName("groupBox_Campaigns_List")
        self.groupBox_Campaigns_List.setTitle("Campaigns List")
###ListWidget Campaigns_List  
        self.listWidget_Campaigns_List = QtWidgets.QListWidget(self.groupBox_Campaigns_List)
        self.listWidget_Campaigns_List.setGeometry(QtCore.QRect(0, 20, 360, 485))
        self.listWidget_Campaigns_List.setFont(font)
        self.listWidget_Campaigns_List.setObjectName("listWidget_Campaigns_List")
###End Groupbox for Campaign List=======================================

###Groupbox for Import Detail=========================================
        self.groupBox_Import_Detail = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_Import_Detail.setGeometry(QtCore.QRect(380, 0, 710, 630))
        self.groupBox_Import_Detail.setObjectName("groupBox_Import_Detail")
        self.groupBox_Import_Detail.setTitle("Import")
###PushButton LoadFile
        self.pushButton_LoadFile = QtWidgets.QPushButton(self.groupBox_Import_Detail)
        self.pushButton_LoadFile.setEnabled(False)
        self.pushButton_LoadFile.setGeometry(QtCore.QRect(5, 15, 75, 25))
        self.pushButton_LoadFile.setFont(font)
        self.pushButton_LoadFile.setObjectName("pushButton_LoadFile")
        self.pushButton_LoadFile.setText("&Load File")
###PushButton Validate
        self.pushButton_Validate = QtWidgets.QPushButton(self.groupBox_Import_Detail)
        self.pushButton_Validate.setEnabled(False)
        self.pushButton_Validate.setGeometry(QtCore.QRect(85, 15, 75, 25))
        self.pushButton_Validate.setFont(font)
        self.pushButton_Validate.setObjectName("pushButton_Validate")
        self.pushButton_Validate.setText("&Validate")
###PushButton DeleteRow
        self.pushButton_DelRow = QtWidgets.QPushButton(self.groupBox_Import_Detail)
        self.pushButton_DelRow.setEnabled(False)
        self.pushButton_DelRow.setGeometry(QtCore.QRect(165, 15, 75, 25))
        self.pushButton_DelRow.setFont(font)
        self.pushButton_DelRow.setObjectName("pushButton_DelRow")
        self.pushButton_DelRow.setText("Delete row(s)")
###PushButton Clear
        self.pushButton_Clear = QtWidgets.QPushButton(self.groupBox_Import_Detail)
        self.pushButton_Clear.setEnabled(False)
        self.pushButton_Clear.setGeometry(QtCore.QRect(245, 15, 75, 25))
        self.pushButton_Clear.setFont(font)
        self.pushButton_Clear.setObjectName("pushButton_Clear")
        self.pushButton_Clear.setText("Clear")
###PushButton AddRow
        self.pushButton_AddRow = QtWidgets.QPushButton(self.groupBox_Import_Detail)
        self.pushButton_AddRow.setEnabled(False)
        self.pushButton_AddRow.setGeometry(QtCore.QRect(325, 15, 75, 25))
        self.pushButton_AddRow.setFont(font)
        self.pushButton_AddRow.setObjectName("pushButton_AddRow")
        self.pushButton_AddRow.setText("Add row")        
###tableWidget_Import
        self.tableWidget_Import = QtWidgets.QTableWidget(self.groupBox_Import_Detail)
        self.tableWidget_Import.setGeometry(QtCore.QRect(0, 45, 710, 585))
        self.tableWidget_Import.setSortingEnabled(False)
        self.tableWidget_Import.setFont(font)
        self.tableWidget_Import.setObjectName("tableWidget_Import")
        self.tableWidget_Import.setColumnCount(0)
        self.tableWidget_Import.setRowCount(0)
        self.tableWidget_Import.horizontalHeader().hide()
        self.tableWidget_Import.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
      
###End Groupbox for Campaign Detail=====================================
        
###Main Menu============================================================
        self.menufile = QtWidgets.QMenuBar(MainWindow)
        self.menufile.setFont(font)
        self.menufile.setObjectName("menufile")

        self.action_Exit = QtWidgets.QAction(MainWindow)
        self.action_Exit.setFont(font)
        self.action_Exit.setObjectName("action_Exit")
        self.action_Exit.setText("&Exit (Ctrl+Q)")
        self.action_Exit.setShortcut('Ctrl+Q')
        self.action_Exit.setStatusTip('Exit')
        self.action_Exit.triggered.connect(QtWidgets.qApp.quit)

        self.menu_File = QtWidgets.QMenu(self.menufile)
        self.menu_File.setObjectName("menu_File")
        self.menu_File.setTitle("&File")
        self.menu_File.addAction(self.action_Exit)        

        self.action_Settings = QtWidgets.QAction(MainWindow)
        self.action_Settings.setFont(font)
        self.action_Settings.setObjectName("action_Settings")
        self.action_Settings.setText("&Settings")

        self.menu_Connection = QtWidgets.QMenu(self.menufile)
        self.menu_Connection.setObjectName("menu_Connection")
        self.menu_Connection.setTitle("&Connection")
        self.menu_Connection.addAction(self.action_Settings)
        
        self.action_About = QtWidgets.QAction(MainWindow)
        self.action_About.setFont(font)
        self.action_About.setObjectName("action_About")
        self.action_About.setText("&About")

        self.menu_Help = QtWidgets.QMenu(self.menufile)
        self.menu_Help.setObjectName("menu_Help")
        self.menu_Help.setTitle("&Help")
        self.menu_Help.addAction(self.action_About)
        
        self.menufile.addAction(self.menu_File.menuAction())
        self.menufile.addAction(self.menu_Connection.menuAction())
        self.menufile.addAction(self.menu_Help.menuAction())

###Statusbar============================================================
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

#Apply Bold to groupBoxes only==========================================
        font.setBold(True)
        self.groupBox_Filter.setFont(font)
        self.groupBox_Campaigns_List.setFont(font)
        self.groupBox_Import_Detail.setFont(font)
#Apply Larger font to CampaignList=====================================
        font.setBold(False)
        font.setPointSize(font.pointSize()+2)
        self.listWidget_Campaigns_List.setFont(font)
###=====================================================================
        MainWindow.setCentralWidget(self.centralwidget)        
        MainWindow.setMenuBar(self.menufile)
        MainWindow.setStatusBar(self.statusbar)        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

class Connection_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog_Connection")
        Dialog.resize(310, 140)
        Dialog.setWindowTitle("Connection settings")
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(310, 130))
        Dialog.setMaximumSize(QtCore.QSize(310, 130))
        self.label_username = QtWidgets.QLabel(Dialog)
        self.label_username.setGeometry(QtCore.QRect(10, 10, 70, 30))
        self.label_username.setObjectName("label_username")
        self.label_username.setText("User name\n(FQDN):")        
        self.lineEdit_username = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_username.setGeometry(QtCore.QRect(80, 10, 110, 20))
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.label_atsign = QtWidgets.QLabel(Dialog)
        self.label_atsign.setGeometry(QtCore.QRect(190, 10, 15, 20))
        self.label_atsign.setObjectName("label_atsign") 
        self.label_atsign.setText("@")        
        self.lineEdit_domain = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_domain.setGeometry(QtCore.QRect(200, 10, 100, 20))
        self.lineEdit_domain.setObjectName("lineEdit_domain")
        self.label_pass = QtWidgets.QLabel(Dialog)
        self.label_pass.setGeometry(QtCore.QRect(10, 40, 70, 20))
        self.label_pass.setObjectName("label_pass")
        self.label_pass.setText("Password:")
        self.lineEdit_pass = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_pass.setGeometry(QtCore.QRect(80, 40, 220, 20))
        self.lineEdit_pass.setObjectName("lineEdit_pass")
        self.lineEdit_pass.setInputMethodHints(QtCore.Qt.ImhHiddenText)
        self.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)        
        self.label_server = QtWidgets.QLabel(Dialog)
        self.label_server.setGeometry(QtCore.QRect(10, 65, 70, 30))
        self.label_server.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_server.setObjectName("label_server")
        self.label_server.setText("Server\n(IP or FQDN):")        
        self.lineEdit_server = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_server.setGeometry(QtCore.QRect(80, 70, 220, 20))
        self.lineEdit_server.setObjectName("lineEdit_server")
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 95, 90, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox_Save")
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox2 = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox2.setGeometry(QtCore.QRect(200, 95, 90, 32))
        self.buttonBox2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox2.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox2.setObjectName("buttonBox_Cancel")
        self.buttonBox2.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

class About_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog_About")
        Dialog.resize(400, 300)
        Dialog.setWindowTitle("About")
        Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(400, 300))
        Dialog.setMaximumSize(QtCore.QSize(400, 300))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 350, 220))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.label2 = QtWidgets.QLabel(Dialog)
        self.label2.setGeometry(QtCore.QRect(20, 230, 350, 20))
        self.label2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label2.setObjectName("label2")        
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 260, 340, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox_Ok")
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
