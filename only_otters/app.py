import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class MusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "Only Otters"
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.createUI()
        self.openFile() #select audio file to play
        self.openFile() #select second audio file to play (stored in playlist)

    def createUI(self):
        menubar = self.menuBar()
        self.setWindowTitle(self.title)
        self.setGeometry(250, 250, 250, 200)
        self.show()

    def openFile(self):
        song = QFileDialog.getOpenFileName(self, "Open Song", "", "Sound Files (*.mp3)")

        if song[0] != '':
            url = QUrl.fromLocalFile(song[0])
            
            #if playlist is empty then play song, otherwise add to playlist
            if self.playlist.mediaCount() == 0:
                self.playlist.addMedia(QMediaContent(url))
                self.player.setPlaylist(self.playlist)
                self.player.play()
            else:
                self.playlist.addMedia(QMediaContent(url))
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MusicPlayer()
    sys.exit(app.exec_())
    
