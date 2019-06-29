import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget, QPushButton, QVBoxLayout, QHBoxLayout


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Only Otters"
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.createUI()
        self.addButtons()
        self.openFile() #select audio file to play
        self.openFile() #select second audio file to play (stored in playlist)

    def createUI(self):
        menubar = self.menuBar()
        self.setWindowTitle(self.title)
        self.setGeometry(250, 250, 250, 200)
        self.show()

    def addButtons(self):
        widget = QWidget(self)
        
        self.setCentralWidget(widget)
        #song controls
        playButton = QPushButton("Play")
        pauseButton = QPushButton("Pause")
        stopButton = QPushButton("Stop")
        #playlist controls
        shuffleButton = QPushButton("Shuffle")
        prevButton = QPushButton("Prev")
        nextButton = QPushButton("Next")
        #button layouts
        centralWidget = QVBoxLayout()
        controls = QHBoxLayout()
        playlistCtrlLayout = QHBoxLayout()
        #layout of buttons for song control
        controls.addWidget(playButton)
        controls.addWidget(pauseButton)
        controls.addWidget(stopButton)
        #layout of buttons for playlist control
        playlistCtrlLayout.addWidget(shuffleButton)
        playlistCtrlLayout.addWidget(prevButton)
        playlistCtrlLayout.addWidget(nextButton)
        #vertical layout
        centralWidget.addLayout(controls)
        centralWidget.addLayout(playlistCtrlLayout)
        widget.setLayout(centralWidget)
        #assign button to corresponding function
        playButton.clicked.connect(self.play)
        pauseButton.clicked.connect(self.pause)
        stopButton.clicked.connect(self.stop)

        shuffleButton.clicked.connect(self.shuffle)
        prevButton.clicked.connect(self.prevSong)
        nextButton.clicked.connect(self.nextSong)
        
        self.statusBar()
        self.playlist.currentMediaChanged.connect(self.songChanged)

    def play(self):
        #if no songs in queue select a file else play 1st song from playlist
        if not self.playlist.mediaCount():
            self.openFile()
        else:
            self.player.play()
    
    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()
        self.playlist.clear()
        self.statusBar().showMessage("Stopped and emptied playlist")

    def shuffle(self):
        self.playlist.shuffle()

    def prevSong(self):
        if not self.playlist.mediaCount():
            self.openFile()
        else:
            self.player.playlist().previous()

    def nextSong(self):
        if not self.playlist.mediaCount():
            self.openFile()
        else:
            self.player.playlist().next()

    def songChanged(self, media):
        if not media.isNull():
            url = media.canonicalUrl()
            self.statusBar().showMessage(f"Playing: {url.fileName().split('.')[0]}")

    def openFile(self):
        song = QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3)")

        if song[0] != '':
            url = QUrl.fromLocalFile(song[0])
            print(song)
            
            #if playlist is empty then play song, otherwise add to playlist
            if not self.playlist.mediaCount():
                self.playlist.addMedia(QMediaContent(url))
                self.player.setPlaylist(self.playlist)
                self.player.play()
            else:
                self.playlist.addMedia(QMediaContent(url))
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MusicPlayer()
    sys.exit(app.exec_())
    
