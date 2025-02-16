import os
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QFileDialog, QMainWindow,
    QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import QtMsgType
from PyQt6.QtGui import QPixmap
from PySide6.QtCore import QUrl, QTime
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput

import pygame
from random import randint
import time
from blueberry_ui2 import *
pygame.init()
pygame.mixer.init()

playlist = []
current_song = ""
is_paused = False

app = QApplication(sys.argv)
class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Blueberry()
        self.ui.setupUi(self)
        self.setWindowTitle('Blueberry')
        self.dir = ''

        self.ui.files.clicked.connect(self.OpenFiles)
        self.ui.playlists.triggered.connect(self.Playlists)
        self.ui.Silder.sliderMoved.connect(self.ChangeVolume)
        self.ui.stop.clicked.connect(self.Stop)
        self.ui.play.clicked.connect(self.Play)
        self.ui.repeat.clicked.connect(self.Repeat)
        self.ui.arrow_right.clicked.connect(self.Next)
        self.ui.arrow_left.clicked.connect(self.Previous)
        self.ui.progressBar.clicked.connect(self.Progression)

        self.player = QMediaPlayer
        self.audio = QAudioOutput

    def filter(self, files, extensions):
        result = []
        for filename in files:
            for ext in extensions:
                if filename.endswith(ext):
                    result.append(filename)
        return result
    def choosedir(self):
        self.dir = QFileDialog.getExistingDirectory()
    def OpenFiles(self): 
        self.choosedir()
        extensions = ['.mp3', '.aac', '.wav', '.flac']
        if self.dir:
            filenames = self.filter(os.listdir(self.dir), extensions)
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
    def Progression(self):
        pass

Blueberry = QtWidgets.QMainWindow()
Blueberry.setWindowTitle("Blueberry")
ui = Ui_Blueberry()
ui.setupUi(Blueberry)
Blueberry.show()
sys.exit(app.exec())

