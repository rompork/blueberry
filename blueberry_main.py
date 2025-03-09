import os
import sys
import random
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (
    QApplication, QWidget, QFileDialog, QMainWindow,
    QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QSlider)
from PyQt6.QtCore import QtMsgType, Qt, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontMetrics
from PySide6.QtCore import QUrl, QTime
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudio, QAudioFormat
from plyer import notification

from random import randint
from blueberry_ui import *

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Blueberry()
        self.ui.setupUi(self)
        self.setWindowTitle('Blueberry')
        self.file = ''
        self.dir = ''
        self.repeat_m = False
        self.shuffle_m = False
        self.current_index = -1
        self.audio_files = []

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.audioVolumeLevel = 70

        self.ui.files.clicked.connect(self.OpenFiles)
        self.ui.Slider.sliderMoved.connect(self.ChangeVolume)
        self.ui.stop.clicked.connect(self.Stop)
        self.ui.play.clicked.connect(self.Play)
        self.ui.pause.clicked.connect(self.Pause)
        self.ui.repeat.clicked.connect(self.Repeat)
        self.ui.arrow_right.clicked.connect(self.Next)
        self.ui.arrow_left.clicked.connect(self.Previous)
        self.ui.playlists.clicked.connect(self.OpenDirectory)
        self.ui.progressSlider.sliderMoved.connect(self.ChangeMusicPosition)
        self.ui.progressSlider.sliderReleased.connect(self.FinalizeMusicPosition)
        self.ui.listWidget.itemDoubleClicked.connect(self.PlaySelectedFile)
        self.ui.shuffle.clicked.connect(self.Shuffle)

        self.player.mediaStatusChanged.connect(self.handleMediaStatusChanged)
        self.player.positionChanged.connect(self.updateSliderPosition)
        self.player.durationChanged.connect(self.updateSliderRange)
        self.ui.label.setText("No file selected")
        self.ui.music_live_time.setText("00:00 / 00:00")
        
    def filter(self, files, extensions):
         result = []
         for filename in files:
             for ext in extensions:
                 if filename.endswith(ext):
                     result.append(filename)
         return result

    def choosefile(self):
        print("choosefile")
        self.file, _ = QFileDialog.getOpenFileName(self, "open file", "", "Audio Files (*.mp3 *.aac *.wav *.flac)")
        print(f"Selected file: {self.file}")

    def choosedir(self):
        print("choosedir")
        self.dir = QFileDialog.getExistingDirectory(self, "open directory", "")

    def OpenFiles(self): 
        print("openfiles")
        self.choosefile()
        if self.file:
            print(f"Setting source to: {self.file}")
            self.player.setSource(QUrl.fromLocalFile(self.file))
            self.ui.label.setText(os.path.basename(self.file))
            self.adjustLabelFontSize(self.ui.label)
            self.Play()
            self.sendNotification(os.path.basename(self.file))

    def OpenDirectory(self):
        print("opendirectory")
        self.choosedir()
        if self.dir:
            print(f"setting source to directory: {self.dir}")
            extensions = ['.mp3', '.aac', '.wav', '.flac']
            files = os.listdir(self.dir)
            self.audio_files = self.filter(files, extensions)
            self.audio_files.sort()
            self.ui.listWidget.clear()
            for audio_file in self.audio_files:
                self.ui.listWidget.addItem(audio_file)
            if self.audio_files:
                self.current_index = 0
                first_file = os.path.join(self.dir, self.audio_files[0])
                print(f"Setting source to: {first_file}")
                self.player.setSource(QUrl.fromLocalFile(first_file))
                self.ui.label.setText(os.path.basename(first_file)) 
                self.adjustLabelFontSize(self.ui.label)
                self.Play()
                self.sendNotification(os.path.basename(first_file))

    def PlaySelectedFile(self, item):
        selected_file = os.path.join(self.dir, item.text())
        print(f"Playing selected file: {selected_file}")
        self.current_index = self.audio_files.index(item.text())
        self.player.setSource(QUrl.fromLocalFile(selected_file))
        self.ui.label.setText(item.text())
        self.adjustLabelFontSize(self.ui.label)
        self.Play()
        self.sendNotification(item.text())

    def ChangeVolume(self):
        print("changed the volume")
        volume = self.ui.Slider.value()
        self.audio.setVolume(volume / 100)

    def Play(self):
        print("play")
        if self.player.source().isValid():
            print("playing the file")
            self.player.play()
        else:
            print("source invalid")
            print(f"media status: {self.player.mediaStatus()}")

    def Pause(self):
        print("paused")
        self.player.pause()

    def Stop(self):
        print("stop")
        self.player.stop()
        self.ui.label.setText("No file selected")
        self.adjustLabelFontSize(self.ui.label)
        self.ui.music_live_time.setText("00:00 / 00:00")

    def Repeat(self):
        print("repeat")
        self.repeat_m = not self.repeat_m
        print(f"repeat mode: {'on' if self.repeat_m else 'off'}")

    def Shuffle(self):
        print("shuffle")
        if self.audio_files:
            self.current_index = randint(0, len(self.audio_files) - 1)
            random_file = os.path.join(self.dir, self.audio_files[self.current_index])
            print(f"Setting source to: {random_file}")
            self.player.setSource(QUrl.fromLocalFile(random_file))
            self.ui.label.setText(os.path.basename(random_file))
            self.adjustLabelFontSize(self.ui.label)
            self.Play()
            self.sendNotification(os.path.basename(random_file))
        else:
            print("No audio files to shuffle")

    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            if self.repeat_m:
                print("repeating the file")
                self.player.setPosition(0)
                self.player.play()
            else:
                self.Next()

    def ChangeMusicPosition(self):
        print("music position changed")
        position = self.ui.progressSlider.value()
        self.player.setPosition(position)
    
    def FinalizeMusicPosition(self):
        print("finalizing music position")
        position = self.ui.progressSlider.value()
        self.player.setPosition(position)

    def updateSliderPosition(self, position):
        self.ui.progressSlider.setValue(position)
        self.updateMusicTime(position)

    def updateSliderRange(self, duration):
        self.ui.progressSlider.setRange(0, duration)
        self.updateMusicTime(self.player.position())

    def updateMusicTime(self, position):
        duration = self.player.duration()
        current_time = QTime(0, 0, 0).addMSecs(position)
        total_time = QTime(0, 0, 0).addMSecs(duration)
        self.ui.music_live_time.setText(f"{current_time.toString('mm:ss')} / {total_time.toString('mm:ss')}")

    def Next(self):
        print("arrow right")
        if not self.audio_files:
            print("No audio files loaded")
            return
        if self.current_index < len(self.audio_files) - 1:
            self.current_index += 1
            next_file = os.path.join(self.dir, self.audio_files[self.current_index])
            print(f"Setting source to: {next_file}")
            self.player.setSource(QUrl.fromLocalFile(next_file))
            self.ui.label.setText(os.path.basename(next_file))
            self.adjustLabelFontSize(self.ui.label)
            self.Play()
            self.sendNotification(os.path.basename(next_file))
        else:
            print("No next file available")

    def Previous(self):
        print("arrow left")
        if not self.audio_files:
            print("No audio files loaded")
            return
        if self.current_index > 0:
            self.current_index -= 1
            prev_file = os.path.join(self.dir, self.audio_files[self.current_index])
            print(f"Setting source to: {prev_file}")
            self.player.setSource(QUrl.fromLocalFile(prev_file))
            self.ui.label.setText(os.path.basename(prev_file))
            self.adjustLabelFontSize(self.ui.label)
            self.Play()
            self.sendNotification(os.path.basename(prev_file))
        else:
            print("No previous file available")

    def adjustLabelFontSize(self, label):
        font = label.font()
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(label.text())
        label_width = label.width()

        while text_width > label_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            font_metrics = QFontMetrics(font)
            text_width = font_metrics.horizontalAdvance(label.text())

        label.setFont(font)

    def sendNotification(self, song_name):
        notification.notify(
            title='Now Playing',
            message=song_name,
            app_name='Blueberry',
            timeout=5
        )

app = QApplication([])
bl = Widget()
bl.show()
app.exec()