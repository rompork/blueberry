import os
import sys
import random
import mutagen
import res_rc
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QSlider, QSystemTrayIcon
from PyQt6.QtCore import QtMsgType, Qt, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontMetrics, QImage
from PyQt6.QtCore import QUrl, QTime, QByteArray
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudioFormat
from random import randint

from blueberry_ui import *
from themes import light_theme, dark_theme ,classic_theme, lavander_theme_dark, lavander_theme_light, orange_theme_dark, orange_theme_light, green_theme_dark, green_theme_light, red_theme_dark, red_theme_light, blue_theme_dark, blue_theme_light, cyan_theme_dark, cyan_theme_light, lime_theme_dark, lime_theme_light

class Widget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Blueberry()
        self.ui.setupUi(self)
        self.setWindowTitle('Blueberry')
        self.setWindowIcon(QIcon(":/icons/blueberry.png"))

        self.file = ''
        self.dir = ''
        self.repeat_m = False
        self.shuffle_m = False
        self.current_index = -1
        self.audio_files = []
        self.current_theme = classic_theme
        self.setStyleSheet(self.current_theme)
        self.scene = QtWidgets.QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.ui.graphicsView.hide() 

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
        self.ui.themes.clicked.connect(self.changeThemes)

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
            self.updateSongIcon(self.file)
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
        self.updateSongIcon(selected_file)
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
        self.ui.graphicsView.hide()

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
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
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
            self.updateSongIcon(next_file)
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
            self.updateSongIcon(prev_file)
            self.Play()
            self.sendNotification(os.path.basename(prev_file))
        else:
            print("No previous file available")

    def adjustLabelFontSize(self, label):
        font = label.font()
        font.setPointSize(24)
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(label.text())
        label_width = label.width()

        while text_width > label_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            font_metrics = QFontMetrics(font)
            text_width = font_metrics.horizontalAdvance(label.text())

        label.setFont(font)
        font_metrics = QFontMetrics(font)
        text = label.text()
        elided_text = font_metrics.elidedText(text, Qt.TextElideMode.ElideRight, label.width())
        label.setText(elided_text)

    def sendNotification(self, song_name):
        try:
            if not hasattr(self, 'tray_icon'):
                self.tray_icon = QSystemTrayIcon(self)
                self.tray_icon.setIcon(QIcon(":/icons/blueberry.png"))
                self.tray_icon.show()
        
            self.tray_icon.showMessage("Now Playing", song_name, QSystemTrayIcon.MessageIcon.Information, 3000)
        except Exception as e:
            print(f"Notification error: {e}")
            pass
    def changeThemes(self):
        themes = ["Light", "Dark", "Classic", "Lavander", "Orange", "Green", "Red", "Blue", "Cyan", "Lime"]
        theme, ok = QtWidgets.QInputDialog.getItem(self, "Select Theme", "Available Themes:", themes, 0, False)
        if ok:
            if theme in ["Light", "Dark", "Classic"]:
                if theme == "Light":
                    self.setStyleSheet(light_theme)
                    self.current_theme = "light"
                elif theme == "Dark":
                    self.setStyleSheet(dark_theme)
                    self.current_theme = "dark"
                elif theme == "Classic":
                    self.setStyleSheet(classic_theme)
                    self.current_theme = "classic"
            else:
                mode, ok_mode = QtWidgets.QInputDialog.getItem(
                    self, "Select Mode", "Choose Mode:", ["Light", "Dark"], 0, False)
                if ok_mode:
                    if theme == "Lavander":
                        self.setStyleSheet(lavander_theme_light if mode == "Light" else lavander_theme_dark)
                        self.current_theme = "lavander"
                    elif theme == "Orange":
                        self.setStyleSheet(orange_theme_light if mode == "Light" else orange_theme_dark)
                        self.current_theme = "orange"
                    elif theme == "Green":
                        self.setStyleSheet(green_theme_light if mode == "Light" else green_theme_dark)
                        self.current_theme = "green"
                    elif theme == "Blue":
                        self.setStyleSheet(blue_theme_light if mode == "Light" else blue_theme_dark)
                        self.current_theme = "blue"
                    elif theme == "Red":
                        self.setStyleSheet(red_theme_light if mode == "Light" else red_theme_dark)
                        self.current_theme = "red"
                    elif theme == "Cyan":
                        self.setStyleSheet(cyan_theme_light if mode == "Light" else cyan_theme_dark)
                        self.current_theme = "cyan"
                    elif theme == "Lime":
                        self.setStyleSheet(lime_theme_light if mode == "Light" else lime_theme_dark)
                        self.current_theme = "lime"
    def updateSongIcon(self, file_path):
        try:
            from mutagen import File
            from mutagen.id3 import ID3
            audio = File(file_path)
            if audio is None:
                self.ui.graphicsView.hide()
                return
            if isinstance(audio, mutagen.mp3.MP3):
                if audio.tags is None:
                    self.ui.graphicsView.hide()
                    return
                for tag in audio.tags.values():
                    if tag.FrameID == 'APIC':
                        img_data = tag.data
                        qimg = QImage.fromData(QByteArray(img_data))
                        pixmap = QPixmap.fromImage(qimg)
                        view_size = self.ui.graphicsView.size()
                        self.scene.setSceneRect(0, 0, view_size.width(), view_size.height())
                        scaled_pixmap = pixmap.scaled(view_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation) 
                        x = (view_size.width() - scaled_pixmap.width()) / 2
                        y = (view_size.height() - scaled_pixmap.height()) / 2 
                        self.scene.clear()
                        self.scene.addPixmap(scaled_pixmap).setPos(x, y)
                        self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                        self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                        self.ui.graphicsView.show()
                        return
            elif isinstance(audio, mutagen.flac.FLAC):
                if audio.pictures:
                    img_data = audio.pictures[0].data
                    qimg = QImage.fromData(QByteArray(img_data))
                    pixmap = QPixmap.fromImage(qimg)
                    view_size = self.ui.graphicsView.size()
                    self.scene.setSceneRect(0, 0, view_size.width(), view_size.height())
                    scaled_pixmap = pixmap.scaled(view_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    x = (view_size.width() - scaled_pixmap.width()) / 2
                    y = (view_size.height() - scaled_pixmap.height()) / 2
                    self.scene.clear()
                    self.scene.addPixmap(scaled_pixmap).setPos(x, y)
                    self.ui.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                    self.ui.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                    self.ui.graphicsView.show()
                    return
            self.ui.graphicsView.hide()
        except Exception as e:
            print(f"Unable to load the icon of the music, try again: {e}")
            self.ui.graphicsView.hide()

app = QApplication([])
bl = Widget()
bl.show()
app.exec()