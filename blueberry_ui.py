# Form implementation generated from reading ui file 'blueberry.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Blueberry(object):
    def setupUi(self, Blueberry):
        Blueberry.setObjectName("Blueberry")
        Blueberry.resize(754, 504)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Blueberry.sizePolicy().hasHeightForWidth())
        Blueberry.setSizePolicy(sizePolicy)
        Blueberry.setMinimumSize(QtCore.QSize(30, 20))
        font = QtGui.QFont()
        font.setItalic(False)
        Blueberry.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/arrow_right.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        Blueberry.setWindowIcon(icon)
#        Blueberry.setStyleSheet("background-color: #000000;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #0000FF;")
        self.centralwidget = QtWidgets.QWidget(parent=Blueberry)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.files = QtWidgets.QToolButton(parent=self.centralwidget)
        self.files.setMinimumSize(QtCore.QSize(30, 40))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setItalic(False)
        self.files.setFont(font)
        self.files.setAutoFillBackground(False)
#        self.files.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.files.setObjectName("files")
        self.horizontalLayout.addWidget(self.files)
        self.playlists = QtWidgets.QPushButton(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.playlists.sizePolicy().hasHeightForWidth())
        self.playlists.setSizePolicy(sizePolicy)
        self.playlists.setMinimumSize(QtCore.QSize(30, 40))
        self.playlists.setMaximumSize(QtCore.QSize(100, 50))
#        self.playlists.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.playlists.setObjectName("playlists")
        self.horizontalLayout.addWidget(self.playlists)
        self.themes = QtWidgets.QToolButton(parent=self.centralwidget)
        self.themes.setMinimumSize(QtCore.QSize(30, 40))
#        self.themes.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.themes.setObjectName("themes")
        self.horizontalLayout.addWidget(self.themes)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.arrow_left = QtWidgets.QPushButton(parent=self.centralwidget)
        self.arrow_left.setMinimumSize(QtCore.QSize(30, 30))
#        self.arrow_left.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.arrow_left.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/arrow_left.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.arrow_left.setIcon(icon1)
        self.arrow_left.setObjectName("arrow_left")
        self.horizontalLayout.addWidget(self.arrow_left)
        self.play = QtWidgets.QPushButton(parent=self.centralwidget)
        self.play.setMinimumSize(QtCore.QSize(30, 30))
#        self.play.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.play.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/play.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.play.setIcon(icon2)
        self.play.setObjectName("play")
        self.horizontalLayout.addWidget(self.play)
        self.pause = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pause.setMinimumSize(QtCore.QSize(30, 30))
#        self.pause.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.pause.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/pause.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pause.setIcon(icon3)
        self.pause.setObjectName("pause")
        self.horizontalLayout.addWidget(self.pause)
        self.arrow_right = QtWidgets.QPushButton(parent=self.centralwidget)
        self.arrow_right.setMinimumSize(QtCore.QSize(30, 30))
#        self.arrow_right.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.arrow_right.setText("")
        self.arrow_right.setIcon(icon)
        self.arrow_right.setObjectName("arrow_right")
        self.horizontalLayout.addWidget(self.arrow_right)
        self.stop = QtWidgets.QPushButton(parent=self.centralwidget)
        self.stop.setMinimumSize(QtCore.QSize(30, 30))
#        self.stop.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.stop.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/stop.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.stop.setIcon(icon4)
        self.stop.setObjectName("stop")
        self.horizontalLayout.addWidget(self.stop)
        self.Slider = QtWidgets.QSlider(parent=self.centralwidget)
#        self.Slider.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.Slider.setSliderPosition(70)
        self.Slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.Slider.setObjectName("Slider")
        self.horizontalLayout.addWidget(self.Slider)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.horizontalLayout)
        self.listWidget = QtWidgets.QListWidget(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(200, 300))
        self.listWidget.setMaximumSize(QtCore.QSize(600, 700))
#        self.listWidget.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #FFFFFF;")
        self.listWidget.setObjectName("listWidget")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.listWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.repeat = QtWidgets.QPushButton(parent=self.centralwidget)
        self.repeat.setMinimumSize(QtCore.QSize(40, 30))
        self.repeat.setMaximumSize(QtCore.QSize(100, 20))
#        self.repeat.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/repeat.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.repeat.setIcon(icon5)
        self.repeat.setCheckable(False)
        self.repeat.setObjectName("repeat")
        self.verticalLayout.addWidget(self.repeat)
        self.shuffle = QtWidgets.QPushButton(parent=self.centralwidget)
        self.shuffle.setMinimumSize(QtCore.QSize(40, 30))
        self.shuffle.setMaximumSize(QtCore.QSize(100, 20))
#        self.shuffle.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/icons/shuffle.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.shuffle.setIcon(icon6)
        self.shuffle.setObjectName("shuffle")
        self.verticalLayout.addWidget(self.shuffle)
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.centralwidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(200, 0))
        self.graphicsView.setMaximumSize(QtCore.QSize(300, 300))
        self.graphicsView.setAlignment(QtCore.Qt.AlignmentFlag.AlignBottom|QtCore.Qt.AlignmentFlag.AlignRight|QtCore.Qt.AlignmentFlag.AlignTrailing)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.verticalLayout)
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(250, 50))
        self.label.setMaximumSize(QtCore.QSize(720, 30))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.label)
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.music_live_time = QtWidgets.QLabel(parent=self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.music_live_time.sizePolicy().hasHeightForWidth())
        self.music_live_time.setSizePolicy(sizePolicy)
        self.music_live_time.setMinimumSize(QtCore.QSize(20, 10))
        self.music_live_time.setMaximumSize(QtCore.QSize(90, 20))
#        self.music_live_time.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.music_live_time.setObjectName("music_live_time")
        self.horizontalLayout_2.addWidget(self.music_live_time)
        self.progressSlider = QtWidgets.QSlider(parent=self.widget)
        self.progressSlider.setMinimumSize(QtCore.QSize(500, 20))
        self.progressSlider.setMaximumSize(QtCore.QSize(600, 30))
#        self.progressSlider.setStyleSheet("background-color: #00008B;\n"
#"border: 1px solid #000000;\n"
#"border-radius: 4px;\n"
#"color: #1E90FF;")
        self.progressSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.progressSlider.setObjectName("progressSlider")
        self.horizontalLayout_2.addWidget(self.progressSlider)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.widget)
        Blueberry.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=Blueberry)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 754, 22))
        self.menubar.setObjectName("menubar")
        Blueberry.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=Blueberry)
        self.statusbar.setObjectName("statusbar")
        Blueberry.setStatusBar(self.statusbar)

        self.retranslateUi(Blueberry)
        QtCore.QMetaObject.connectSlotsByName(Blueberry)

    def retranslateUi(self, Blueberry):
        _translate = QtCore.QCoreApplication.translate
        Blueberry.setWindowTitle(_translate("Blueberry", "Blueberry"))
        self.files.setText(_translate("Blueberry", "Files"))
        self.playlists.setText(_translate("Blueberry", "Playlists"))
        self.themes.setText(_translate("Blueberry", "Themes"))
        self.repeat.setText(_translate("Blueberry", "Repeat"))
        self.shuffle.setText(_translate("Blueberry", "Shuffle"))
        self.label.setText(_translate("Blueberry", "TextLabel"))
        self.music_live_time.setText(_translate("Blueberry", "00:00"))
