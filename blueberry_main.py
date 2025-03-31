import os
import sys
import random
import mutagen
import res_rc
from settings import Settings
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog, QMainWindow, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QSlider, QSystemTrayIcon
from PyQt6.QtCore import QtMsgType, Qt, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QFont, QFontMetrics, QImage, QShortcut, QKeySequence
from PyQt6.QtCore import QUrl, QTime, QByteArray
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QAudioFormat
from random import randint

from blueberry_ui import *
from themes import light_theme, dark_theme ,classic_theme, lavander_theme_dark, lavander_theme_light, orange_theme_dark, orange_theme_light, green_theme_dark, green_theme_light, red_theme_dark, red_theme_light, blue_theme_dark, blue_theme_light, cyan_theme_dark, cyan_theme_light, lime_theme_dark, lime_theme_light

FONTS = {
    'Default': 'Arial',
    'Modern': 'Roboto',
    'Classic': 'Times New Roman',
    'Elegant': 'Georgia',
    'Monospace': 'Courier New',
    'Clean': 'Helvetica',
    'Professional': 'Calibri'}

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
        self.shuffle_history = [] 
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
        self.ui.fonts.clicked.connect(self.changeFonts)
        self.ui.help.clicked.connect(self.showHelp)

        self.player.mediaStatusChanged.connect(self.handleMediaStatusChanged)
        self.player.positionChanged.connect(self.updateSliderPosition)
        self.player.durationChanged.connect(self.updateSliderRange)
        self.ui.label.setText("No file selected")
        self.ui.music_live_time.setText("00:00 / 00:00")

        self.shortcut_next = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Right"), self)
        self.shortcut_next.activated.connect(self.Next)
    
        self.shortcut_prev = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Left"), self)
        self.shortcut_prev.activated.connect(self.Previous)
    
        self.shortcut_play = QtGui.QShortcut(QtGui.QKeySequence("Space"), self)
        self.shortcut_play.activated.connect(self.PlayPause)
    
        self.shortcut_stop = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        self.shortcut_stop.activated.connect(self.Stop)
    
        self.shortcut_vol_up = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Up"), self)
        self.shortcut_vol_up.activated.connect(self.VolumeUp)
    
        self.shortcut_vol_down = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+Down"), self)
        self.shortcut_vol_down.activated.connect(self.VolumeDown)
    
        self.shortcut_mute = QtGui.QShortcut(QtGui.QKeySequence("Ctrl+M"), self)
        self.shortcut_mute.activated.connect(self.ToggleMute)

        self.settings = Settings()
        self.current_theme = self.settings.settings['last_theme']
        self.setStyleSheet(self.get_theme_stylesheet(self.current_theme))
        if self.settings.settings['last_directory']:
            self.dir = self.settings.settings['last_directory']
            self.audio_files = self.settings.settings['playlist']
            self.current_index = self.settings.settings['current_index']
            self.ui.listWidget.clear()
            for audio_file in self.audio_files:
                self.ui.listWidget.addItem(audio_file)
            if self.current_index >= 0 and self.audio_files:
                current_file = os.path.join(self.dir, self.audio_files[self.current_index])
                self.highlightCurrentSong() 
                if os.path.exists(current_file):
                    self.player.setSource(QUrl.fromLocalFile(current_file))
                    self.ui.label.setText(os.path.basename(current_file))
                    self.adjustLabelFontSize(self.ui.label)
                    self.updateSongIcon(current_file)

        saved_font = self.settings.settings.get('current_font', 'Default')
        if saved_font in FONTS:
            font_obj = QFont(FONTS[saved_font], 12)
            self.ui.label.setFont(font_obj)
            self.ui.music_live_time.setFont(font_obj)
            self.ui.version_label.setFont(font_obj)
            self.ui.listWidget.setFont(font_obj)


    def filter(self, files, extensions):
        result = []
        for filename in files:
            for ext in extensions:
                if filename.endswith(ext):
                    result.append(filename)
        return result

    def choosefile(self):
        print("choosefile")
        self.file, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Audio Files (*.mp3 *.aac *.wav *.flac)")
        print(f"Selected file: {self.file}")

    def choosedir(self):
        print("choosedir")
        self.dir = QFileDialog.getExistingDirectory(self, "Open directory", "")

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
            self.settings.settings['last_directory'] = self.dir
            self.settings.settings['playlist'] = self.audio_files
            self.settings.settings['current_index'] = self.current_index
            self.settings.save_settings()
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
        self.settings.settings['current_index'] = self.current_index
        self.settings.save_settings()
        self.Play()
        self.highlightCurrentSong()
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
        self.highlightCurrentSong()

    def Repeat(self):
        print("repeat")
        self.repeat_m = not self.repeat_m
        print(f"repeat mode: {'on' if self.repeat_m else 'off'}")
        if self.repeat_m:
            self.ui.repeat.setIcon(QIcon(":/icons/repeat_on.png"))
        else:
            self.ui.repeat.setIcon(QIcon(":/icons/repeat_off.png"))

    def Shuffle(self):
        print("shuffle")
        self.shuffle_m = not self.shuffle_m
        print(f"shuffle mode: {'on' if self.shuffle_m else 'off'}")
        if self.shuffle_m:
            self.ui.shuffle.setIcon(QIcon(":/icons/shuffle_on.png"))
        else:
            self.ui.shuffle.setIcon(QIcon(":/icons/shuffle_off.png"))

    def ShuffleToNextSong(self):
        if self.audio_files:
            available_indices = [i for i in range(len(self.audio_files)) if i != self.current_index]
            if available_indices:
                if self.current_index >= 0:
                    self.shuffle_history.append(self.current_index)  # Save current song to history
                self.current_index = random.choice(available_indices)
                random_file = os.path.join(self.dir, self.audio_files[self.current_index])
                print(f"Setting source to: {random_file}")
                self.player.setSource(QUrl.fromLocalFile(random_file))
                self.adjustLabelFontSize(self.ui.label)
                self.updateSongIcon(random_file)
                self.settings.settings['current_index'] = self.current_index
                self.settings.save_settings()
                self.Play()
                self.highlightCurrentSong()
                self.sendNotification(os.path.basename(random_file))
            else:
                print("No songs left to shuffle to")
        else:
            print("No audio files to shuffle")

    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            if self.repeat_m:
                print("repeating the file")
                self.player.setPosition(0)
                self.player.play()
            else:
                if self.shuffle_m:
                    print("shuffling to next song")
                    self.ShuffleToNextSong()
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
        if self.shuffle_m:
            self.ShuffleToNextSong()
            return
        if self.current_index < len(self.audio_files) - 1:
            self.current_index += 1
            next_file = os.path.join(self.dir, self.audio_files[self.current_index])
            print(f"Setting source to: {next_file}")
            self.player.setSource(QUrl.fromLocalFile(next_file))
            self.ui.label.setText(os.path.basename(next_file))
            self.adjustLabelFontSize(self.ui.label)
            self.updateSongIcon(next_file)
            self.settings.settings['current_index'] = self.current_index
            self.settings.save_settings()
            self.Play()
            self.highlightCurrentSong()
            self.sendNotification(os.path.basename(next_file))
        else:
            print("No next file available")

    def Previous(self):
        print("arrow left")
        if not self.audio_files:
            print("No audio files loaded")
            return
        if self.shuffle_m:
            if self.shuffle_history:
                self.current_index = self.shuffle_history.pop()  
                prev_file = os.path.join(self.dir, self.audio_files[self.current_index])
                print(f"Setting source to previous shuffled song: {prev_file}")
                self.player.setSource(QUrl.fromLocalFile(prev_file))
                self.ui.label.setText(os.path.basename(prev_file))
                self.adjustLabelFontSize(self.ui.label)
                self.updateSongIcon(prev_file)
                self.settings.settings['current_index'] = self.current_index
                self.settings.save_settings()
                self.Play()
                self.highlightCurrentSong()
                self.sendNotification(os.path.basename(prev_file))
            else:
                print("No previous shuffled songs available")
            return
        if self.current_index > 0:
            self.current_index -= 1
            prev_file = os.path.join(self.dir, self.audio_files[self.current_index])
            print(f"Setting source to: {prev_file}")
            self.player.setSource(QUrl.fromLocalFile(prev_file))
            self.ui.label.setText(os.path.basename(prev_file))
            self.adjustLabelFontSize(self.ui.label)
            self.updateSongIcon(prev_file)
            self.settings.settings['current_index'] = self.current_index
            self.settings.save_settings()
            self.Play()
            self.highlightCurrentSong()
            self.sendNotification(os.path.basename(prev_file))
        else:
            print("No previous file available")

    def PlayPause(self):
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.Pause()
        else:
            self.Play()

    def VolumeUp(self):
        current = self.ui.Slider.value()
        new_volume = min(current + 5, 100)
        self.ui.Slider.setValue(new_volume)
        self.ChangeVolume()

    def VolumeDown(self):
        current = self.ui.Slider.value()
        new_volume = max(current - 5, 0)
        self.ui.Slider.setValue(new_volume)
        self.ChangeVolume()

    def ToggleMute(self):
        self.audio.setMuted(not self.audio.isMuted())

    def adjustLabelFontSize(self, label):
        font = label.font()
        original_family = font.family()
        font.setPointSize(24)
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance(label.text())
        label_width = label.width()

        while text_width > label_width and font.pointSize() > 1:
            font.setPointSize(font.pointSize() - 1)
            font_metrics = QFontMetrics(font)
            text_width = font_metrics.horizontalAdvance(label.text())

        font.setFamily(original_family)
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
                    theme_lower = theme.lower()
                    if mode == "Dark":
                        theme_lower += "_dark"
                    self.current_theme = theme_lower
                    self.setStyleSheet(self.get_theme_stylesheet(theme_lower))
        self.settings.settings['last_theme'] = self.current_theme
        self.settings.save_settings()
    def get_theme_stylesheet(self, theme_name):
        parts = theme_name.split('_')
        base_theme = parts[0]
        is_dark = len(parts) > 1 and parts[1] == 'dark'
        theme_map = {
            'light': light_theme,
            'dark': dark_theme,
            'classic': classic_theme,
            'lavander': {
                'light': lavander_theme_light,
                'dark': lavander_theme_dark
            },
            'orange': {
                'light': orange_theme_light,
                'dark': orange_theme_dark
            },
            'green': {
                'light': green_theme_light,
                'dark': green_theme_dark
            },
            'blue': {
                'light': blue_theme_light,
                'dark': blue_theme_dark
            },
            'red': {
                'light': red_theme_light,
                'dark': red_theme_dark
            },
            'cyan': {
                'light': cyan_theme_light,
                'dark': cyan_theme_dark
            },
            'lime': {
                'light': lime_theme_light,
                'dark': lime_theme_dark
            }
        }
        if base_theme in ['light', 'dark', 'classic']:
            return theme_map.get(base_theme, classic_theme)
        if base_theme in theme_map:
            theme_variant = theme_map[base_theme]
            return theme_variant['dark' if is_dark else 'light']

        return classic_theme
    def changeFonts(self):
        fonts = list(FONTS.keys())
        font, ok = QtWidgets.QInputDialog.getItem(
            self, "Select Font", "Available Fonts:", fonts, 0, False)
        if ok:
            try:
                selected_font = FONTS[font]
                font_obj = QFont(selected_font, 12)
                self.ui.label.setFont(font_obj)
                self.ui.music_live_time.setFont(font_obj)
                self.ui.version_label.setFont(font_obj)
                self.ui.listWidget.setFont(font_obj)
                self.settings.settings['current_font'] = font
                self.settings.save_settings()
                self.adjustLabelFontSize(self.ui.label)
            except Exception as e:
                print(f"Error setting font: {e}")
    def highlightCurrentSong(self):
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            item.setForeground(Qt.GlobalColor.white)
        if self.current_index >= 0 and self.current_index < self.ui.listWidget.count():
            current_item = self.ui.listWidget.item(self.current_index)
            current_item.setForeground(Qt.GlobalColor.cyan)

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
            print(f"Unable to load the icon, try again: {e}")
            self.ui.graphicsView.hide()
    def showHelp(self):
        text = """
        Keyboard Shortcuts:
    
        • Space - Play/Pause
        • Ctrl + Right - Next Song
        • Ctrl + Left - Previous Song
        • Ctrl + S - Stop
        • Ctrl + Up - Volume Up
        • Ctrl + Down - Volume Down
        • Ctrl + M - Toggle Mute
    
        Other Controls:
        • Double click song in list to play them
        • Use slider in the upper right corner to change the volume (why did i add this)
        • Use the slider on the bottom to change the postion of the song
        """
    
        help_dialog = QtWidgets.QDialog(self)
        help_dialog.setWindowTitle("Help")
        help_dialog.setFixedSize(400, 300)
    
        layout = QtWidgets.QVBoxLayout()
    
        text_browser = QtWidgets.QTextBrowser()
        text_browser.setStyleSheet(self.current_theme)
        text_browser.setText(text)
        text_browser.setOpenExternalLinks(False)
    
        close_button = QtWidgets.QPushButton("Close")
        close_button.setStyleSheet(self.current_theme)
        close_button.clicked.connect(help_dialog.close)
    
        layout.addWidget(text_browser)
        layout.addWidget(close_button)
    
        help_dialog.setLayout(layout)
        help_dialog.exec()

app = QApplication([])
bl = Widget()
bl.show()
app.exec()