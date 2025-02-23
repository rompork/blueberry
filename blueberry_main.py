import os
import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QFileDialog, QMainWindow,
    QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout)
from PyQt6.QtCore import QtMsgType
from PyQt6.QtGui import QPixmap
from PySide6.QtCore import QUrl, QTime
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudio

from random import randint
import time
from blueberry_ui import *


playlist = []
current_song = ""
is_paused = False


class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Blueberry()
        self.ui.setupUi(self)
        self.setWindowTitle('Blueberry')
        self.file = ''

        self.player = QMediaPlayer
        self.audio = QAudioOutput

        self.ui.files.clicked.connect(self.OpenFiles)
        self.ui.Slider.sliderMoved.connect(self.ChangeVolume)
        self.ui.stop.clicked.connect(self.Stop)
        self.ui.play.clicked.connect(self.Play)
        self.ui.repeat.clicked.connect(self.Repeat)
        self.ui.arrow_right.clicked.connect(self.Next)
        self.ui.arrow_left.clicked.connect(self.Previous)
        #self.ui.progressBar.positionChanged.connect(self.Progression)



    def filter(self, files, extensions):
        result = []
        for filename in files:
            for ext in extensions:
                if filename.endswith(ext):
                    result.append(filename)
        return result
    def choosefile(self):
        print("choosedir")
        self.file = QFileDialog.getOpenFileName(self)
    def OpenFiles(self): 
        print("openfiles")
        self.choosefile()
        extensions = ['.mp3', '.aac', '.wav', '.flac']
        if self.file:
           filenames = self.filter(self.file, extensions)
    def ChangeVolume(self):
        print("changed the volume")
    def Play(self):
        print("play")
        #pygame.mixer.music.load(self.file)
        #pygame.mixer.music.play(self.file)
    def Previous(self):
        print("arrow left")
    def Next(self):
        print("arrow right")
    def Stop(self):
        print("stop")
        self.player.stop()
    def Repeat(self):
        print("repeat")
    def Progression(self):
        print("progress")


app = QApplication([])
ex = Widget()
ex.show()
app.exec()