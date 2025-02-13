import os
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QFileDialog,
    QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import QtMsgType
from PyQt6.QtGui import QPixmap
from PySide6.QtCore import QUrl, QTime

import pygame
from random import randint
import time
from blueberry_ui2 import Ui_Blueberry
pygame.init()
pygame.mixer.init()

playlist = []
current_song = ""
is_paused = False

app = QtWidgets.QApplication(sys.argv)
class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Blueberry()
        self.ui.setupUi(self)
        self.setWindowTitle('Blueberry')

        self.ui.files.triggered.connect(self.OpenFiles)
        self.ui.playlists.triggered.connect(self.Playlists)
        self.ui.Silder.sliderMoved.connect(self.ChangeVolume)
        self.ui.stop.clicked.connect(self.Stop)
        self.ui.play.clicked.connect(self.Play)
        self.ui.shuffle.clicked.connect(self.Shuffle)
        self.ui.repeat.clicked.connect(self.Repeat)
        self.ui.arrow_right.clicked.connect(self.Next)
        self.ui.arrow_left.clicked.connect(self.Previous)
        self.ui.music_list.clicked.connect(self.ShowList)
        self.ui.progressBar.clicked.connect(self.Progression)

    def OpenFiles(self): 
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Music")
        if fileName != '':
            self.player.setSource(QUrl.fromLocalFile(fileName))
            self.ui.toolButtonPlay.setEnabled(True)
    def ShowList(self):
        pass
    def Playlists(self):
        pass
    def ChangeVolume(self):
        pass
    def Play(self):

        pygame.mixer.music.load()
        pygame.mixer.music.play()
    def Previous(self):
        pass
    def Next(self):
        pass
    def Stop(self):
        pygame.mixer.music.pause()
    def Repeat(self):
        pass
    def Shuffle(self):
        pass
    def Progression(self):
        pass

Blueberry = QtWidgets.QMainWindow()
Blueberry.setWindowTitle("Blueberry")
ex = QWidget()
ex.show()
app.exec()
ui = Ui_Blueberry()
ui.setupUi(Blueberry)
Blueberry.show()
sys.exit(app.exec())

