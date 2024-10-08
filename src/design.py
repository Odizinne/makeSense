# Form implementation generated from reading ui file '.\ui\design.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(532, 514)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.controllerFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.controllerFrame.setObjectName("controllerFrame")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.controllerFrame)
        self.gridLayout_7.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.lightbarFrame = QtWidgets.QFrame(parent=self.controllerFrame)
        self.lightbarFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.lightbarFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.lightbarFrame.setObjectName("lightbarFrame")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.lightbarFrame)
        self.gridLayout_5.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_5.setVerticalSpacing(9)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.bSlider = QtWidgets.QSlider(parent=self.lightbarFrame)
        self.bSlider.setMinimumSize(QtCore.QSize(0, 25))
        self.bSlider.setMaximum(255)
        self.bSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.bSlider.setObjectName("bSlider")
        self.gridLayout_5.addWidget(self.bSlider, 2, 1, 1, 1)
        self.rLabel = QtWidgets.QLabel(parent=self.lightbarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rLabel.sizePolicy().hasHeightForWidth())
        self.rLabel.setSizePolicy(sizePolicy)
        self.rLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.rLabel.setObjectName("rLabel")
        self.gridLayout_5.addWidget(self.rLabel, 0, 0, 1, 1)
        self.b = QtWidgets.QSpinBox(parent=self.lightbarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.b.sizePolicy().hasHeightForWidth())
        self.b.setSizePolicy(sizePolicy)
        self.b.setMinimumSize(QtCore.QSize(80, 25))
        self.b.setWrapping(False)
        self.b.setFrame(False)
        self.b.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.b.setProperty("showGroupSeparator", False)
        self.b.setMaximum(255)
        self.b.setObjectName("b")
        self.gridLayout_5.addWidget(self.b, 2, 2, 1, 1)
        self.rSlider = QtWidgets.QSlider(parent=self.lightbarFrame)
        self.rSlider.setMinimumSize(QtCore.QSize(0, 25))
        self.rSlider.setMaximum(255)
        self.rSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.rSlider.setObjectName("rSlider")
        self.gridLayout_5.addWidget(self.rSlider, 0, 1, 1, 1)
        self.gSlider = QtWidgets.QSlider(parent=self.lightbarFrame)
        self.gSlider.setMinimumSize(QtCore.QSize(0, 25))
        self.gSlider.setMaximum(255)
        self.gSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.gSlider.setObjectName("gSlider")
        self.gridLayout_5.addWidget(self.gSlider, 1, 1, 1, 1)
        self.bLabel = QtWidgets.QLabel(parent=self.lightbarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bLabel.sizePolicy().hasHeightForWidth())
        self.bLabel.setSizePolicy(sizePolicy)
        self.bLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.bLabel.setObjectName("bLabel")
        self.gridLayout_5.addWidget(self.bLabel, 2, 0, 1, 1)
        self.gLabel = QtWidgets.QLabel(parent=self.lightbarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gLabel.sizePolicy().hasHeightForWidth())
        self.gLabel.setSizePolicy(sizePolicy)
        self.gLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.gLabel.setObjectName("gLabel")
        self.gridLayout_5.addWidget(self.gLabel, 1, 0, 1, 1)
        self.g = QtWidgets.QSpinBox(parent=self.lightbarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.g.sizePolicy().hasHeightForWidth())
        self.g.setSizePolicy(sizePolicy)
        self.g.setMinimumSize(QtCore.QSize(80, 25))
        self.g.setWrapping(False)
        self.g.setFrame(False)
        self.g.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.g.setProperty("showGroupSeparator", False)
        self.g.setMaximum(255)
        self.g.setObjectName("g")
        self.gridLayout_5.addWidget(self.g, 1, 2, 1, 1)
        self.r = QtWidgets.QSpinBox(parent=self.lightbarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.r.sizePolicy().hasHeightForWidth())
        self.r.setSizePolicy(sizePolicy)
        self.r.setMinimumSize(QtCore.QSize(80, 25))
        self.r.setWrapping(False)
        self.r.setFrame(False)
        self.r.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.r.setProperty("showGroupSeparator", False)
        self.r.setMaximum(255)
        self.r.setObjectName("r")
        self.gridLayout_5.addWidget(self.r, 0, 2, 1, 1)
        self.gridLayout_7.addWidget(self.lightbarFrame, 5, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.controllerFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setIndent(3)
        self.label_2.setObjectName("label_2")
        self.gridLayout_7.addWidget(self.label_2, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.controllerFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setIndent(3)
        self.label_4.setObjectName("label_4")
        self.gridLayout_7.addWidget(self.label_4, 4, 0, 1, 1)
        self.gridFrame = QtWidgets.QFrame(parent=self.controllerFrame)
        self.gridFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.gridFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout_2.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_2.setVerticalSpacing(12)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.emulateXboxBox = QtWidgets.QCheckBox(parent=self.gridFrame)
        self.emulateXboxBox.setMinimumSize(QtCore.QSize(0, 25))
        self.emulateXboxBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.emulateXboxBox.setText("")
        self.emulateXboxBox.setObjectName("emulateXboxBox")
        self.gridLayout_2.addWidget(self.emulateXboxBox, 0, 1, 1, 1)
        self.hideDualsenseLabel = QtWidgets.QLabel(parent=self.gridFrame)
        self.hideDualsenseLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.hideDualsenseLabel.setBaseSize(QtCore.QSize(0, 0))
        self.hideDualsenseLabel.setObjectName("hideDualsenseLabel")
        self.gridLayout_2.addWidget(self.hideDualsenseLabel, 1, 0, 1, 1)
        self.hideDualsenseBox = QtWidgets.QCheckBox(parent=self.gridFrame)
        self.hideDualsenseBox.setMinimumSize(QtCore.QSize(0, 25))
        self.hideDualsenseBox.setBaseSize(QtCore.QSize(0, 0))
        self.hideDualsenseBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.hideDualsenseBox.setText("")
        self.hideDualsenseBox.setObjectName("hideDualsenseBox")
        self.gridLayout_2.addWidget(self.hideDualsenseBox, 1, 1, 1, 1)
        self.emulateXboxLabel = QtWidgets.QLabel(parent=self.gridFrame)
        self.emulateXboxLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.emulateXboxLabel.setObjectName("emulateXboxLabel")
        self.gridLayout_2.addWidget(self.emulateXboxLabel, 0, 0, 1, 1)
        self.rumbleSlider = QtWidgets.QSlider(parent=self.gridFrame)
        self.rumbleSlider.setMinimumSize(QtCore.QSize(0, 25))
        self.rumbleSlider.setMaximum(100)
        self.rumbleSlider.setSliderPosition(50)
        self.rumbleSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.rumbleSlider.setObjectName("rumbleSlider")
        self.gridLayout_2.addWidget(self.rumbleSlider, 2, 1, 1, 1)
        self.rumbleLabel = QtWidgets.QLabel(parent=self.gridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rumbleLabel.sizePolicy().hasHeightForWidth())
        self.rumbleLabel.setSizePolicy(sizePolicy)
        self.rumbleLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.rumbleLabel.setObjectName("rumbleLabel")
        self.gridLayout_2.addWidget(self.rumbleLabel, 2, 0, 1, 1)
        self.gridLayout_7.addWidget(self.gridFrame, 5, 0, 1, 1)
        self.settingsFrame = QtWidgets.QFrame(parent=self.controllerFrame)
        self.settingsFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.settingsFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.settingsFrame.setObjectName("settingsFrame")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.settingsFrame)
        self.gridLayout_4.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_4.setVerticalSpacing(12)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.startupBox = QtWidgets.QCheckBox(parent=self.settingsFrame)
        self.startupBox.setMinimumSize(QtCore.QSize(0, 25))
        self.startupBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.startupBox.setText("")
        self.startupBox.setObjectName("startupBox")
        self.gridLayout_4.addWidget(self.startupBox, 0, 2, 1, 1)
        self.startupLabel = QtWidgets.QLabel(parent=self.settingsFrame)
        self.startupLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.startupLabel.setObjectName("startupLabel")
        self.gridLayout_4.addWidget(self.startupLabel, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.settingsFrame)
        self.label_3.setMinimumSize(QtCore.QSize(0, 25))
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 4, 0, 1, 1)
        self.triggerComboBox = QtWidgets.QComboBox(parent=self.settingsFrame)
        self.triggerComboBox.setMinimumSize(QtCore.QSize(100, 25))
        self.triggerComboBox.setObjectName("triggerComboBox")
        self.gridLayout_4.addWidget(self.triggerComboBox, 5, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.settingsFrame)
        self.label_5.setMinimumSize(QtCore.QSize(0, 25))
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 5, 0, 1, 1)
        self.touchpadLabel = QtWidgets.QLabel(parent=self.settingsFrame)
        self.touchpadLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.touchpadLabel.setObjectName("touchpadLabel")
        self.gridLayout_4.addWidget(self.touchpadLabel, 1, 0, 1, 1)
        self.touchpadBox = QtWidgets.QCheckBox(parent=self.settingsFrame)
        self.touchpadBox.setMinimumSize(QtCore.QSize(0, 25))
        self.touchpadBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.touchpadBox.setText("")
        self.touchpadBox.setObjectName("touchpadBox")
        self.gridLayout_4.addWidget(self.touchpadBox, 1, 2, 1, 1)
        self.shortcutComboBox = QtWidgets.QComboBox(parent=self.settingsFrame)
        self.shortcutComboBox.setMinimumSize(QtCore.QSize(100, 25))
        self.shortcutComboBox.setObjectName("shortcutComboBox")
        self.gridLayout_4.addWidget(self.shortcutComboBox, 4, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout_4.addItem(spacerItem, 4, 1, 1, 1)
        self.gridLayout_7.addWidget(self.settingsFrame, 3, 0, 1, 2)
        self.label = QtWidgets.QLabel(parent=self.controllerFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setIndent(3)
        self.label.setObjectName("label")
        self.gridLayout_7.addWidget(self.label, 2, 0, 1, 2)
        self.batteryLabel_3 = QtWidgets.QLabel(parent=self.controllerFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.batteryLabel_3.sizePolicy().hasHeightForWidth())
        self.batteryLabel_3.setSizePolicy(sizePolicy)
        self.batteryLabel_3.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setBold(True)
        self.batteryLabel_3.setFont(font)
        self.batteryLabel_3.setIndent(3)
        self.batteryLabel_3.setObjectName("batteryLabel_3")
        self.gridLayout_7.addWidget(self.batteryLabel_3, 0, 0, 1, 2)
        self.batteryFrame = QtWidgets.QFrame(parent=self.controllerFrame)
        self.batteryFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.batteryFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.batteryFrame.setObjectName("batteryFrame")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.batteryFrame)
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.batteryLabel = QtWidgets.QLabel(parent=self.batteryFrame)
        self.batteryLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.batteryLabel.setText("")
        self.batteryLabel.setObjectName("batteryLabel")
        self.gridLayout_3.addWidget(self.batteryLabel, 0, 1, 1, 1)
        self.batteryBar = QtWidgets.QProgressBar(parent=self.batteryFrame)
        self.batteryBar.setMinimumSize(QtCore.QSize(0, 25))
        self.batteryBar.setProperty("value", 24)
        self.batteryBar.setTextVisible(False)
        self.batteryBar.setInvertedAppearance(False)
        self.batteryBar.setTextDirection(QtWidgets.QProgressBar.Direction.TopToBottom)
        self.batteryBar.setObjectName("batteryBar")
        self.gridLayout_3.addWidget(self.batteryBar, 0, 0, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.connectionTypeLabel = QtWidgets.QLabel(parent=self.batteryFrame)
        self.connectionTypeLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.connectionTypeLabel.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.connectionTypeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing|QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.connectionTypeLabel.setObjectName("connectionTypeLabel")
        self.gridLayout_6.addWidget(self.connectionTypeLabel, 0, 1, 1, 1)
        self.batteryStatusLabel = QtWidgets.QLabel(parent=self.batteryFrame)
        self.batteryStatusLabel.setMinimumSize(QtCore.QSize(0, 25))
        self.batteryStatusLabel.setObjectName("batteryStatusLabel")
        self.gridLayout_6.addWidget(self.batteryStatusLabel, 0, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.batteryFrame)
        self.label_6.setMinimumSize(QtCore.QSize(0, 25))
        self.label_6.setObjectName("label_6")
        self.gridLayout_6.addWidget(self.label_6, 1, 0, 1, 1)
        self.batteryNotificationBox = QtWidgets.QCheckBox(parent=self.batteryFrame)
        self.batteryNotificationBox.setMinimumSize(QtCore.QSize(0, 25))
        self.batteryNotificationBox.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.batteryNotificationBox.setText("")
        self.batteryNotificationBox.setObjectName("batteryNotificationBox")
        self.gridLayout_6.addWidget(self.batteryNotificationBox, 1, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_6, 2, 0, 1, 2)
        self.gridLayout_7.addWidget(self.batteryFrame, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.controllerFrame, 1, 0, 1, 1)
        self.notFoundLabel = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.notFoundLabel.sizePolicy().hasHeightForWidth())
        self.notFoundLabel.setSizePolicy(sizePolicy)
        self.notFoundLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.notFoundLabel.setObjectName("notFoundLabel")
        self.gridLayout.addWidget(self.notFoundLabel, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.rLabel.setText(_translate("MainWindow", "R"))
        self.bLabel.setText(_translate("MainWindow", "B"))
        self.gLabel.setText(_translate("MainWindow", "G"))
        self.label_2.setText(_translate("MainWindow", "Lightbar"))
        self.label_4.setText(_translate("MainWindow", "Virtual gamepad"))
        self.hideDualsenseLabel.setText(_translate("MainWindow", "Hide Dualsense"))
        self.emulateXboxLabel.setText(_translate("MainWindow", "Virtual XBOX Controller"))
        self.rumbleLabel.setText(_translate("MainWindow", "Rumble intensity    "))
        self.startupLabel.setText(_translate("MainWindow", "Run at startup"))
        self.label_3.setText(_translate("MainWindow", "Mic button shortcut"))
        self.label_5.setText(_translate("MainWindow", "Trigger effect"))
        self.touchpadLabel.setText(_translate("MainWindow", "Touchpad"))
        self.label.setText(_translate("MainWindow", "Settings"))
        self.batteryLabel_3.setText(_translate("MainWindow", "Battery"))
        self.connectionTypeLabel.setText(_translate("MainWindow", "Connection type"))
        self.batteryStatusLabel.setText(_translate("MainWindow", "Status"))
        self.label_6.setText(_translate("MainWindow", "Notify on low battery"))
        self.notFoundLabel.setText(_translate("MainWindow", "No Dualsense found."))
