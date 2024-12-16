from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
    QSlider, QStyle, QSizePolicy, QFileDialog
import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette
from PyQt5.QtCore import Qt, QUrl
 
# Create a QWidget-based class to represent the application window
class Window(QWidget):
    def __init__(self):
        super().__init__()
 
        # Set window properties such as title, size, and icon
        self.setWindowTitle("TH Watch")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))
 
        # Set window background color
        p =self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)
 
        # Initialize the user interface
        self.init_ui()
 
        # Display the window
        self.show()
 
    # Initialize the user interface components
    def init_ui(self):
 
        # Create a QMediaPlayer object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
 
        # Create a QVideoWidget object to display video
        videowidget = QVideoWidget()
 
        # Create a QPushButton to open video files
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)
 
        # Create a QPushButton to play or pause the video
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)
 
        # Create a QSlider for seeking within the video
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.slider.sliderMoved.connect(self.set_position)
 
        # Create a QLabel to display video information or errors
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
 
        # Create a QHBoxLayout for arranging widgets horizontally
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0,0,0,0)
 
        # Add widgets to the QHBoxLayout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
 
        # Create a QVBoxLayout for arranging widgets vertically
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)
 
        # Set the layout of the window
        self.setLayout(vboxLayout)
 
        # Set the video output for the media player
        self.mediaPlayer.setVideoOutput(videowidget)
 
        # Connect media player signals to their respective slots
        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)
 
    # Method to open a video file
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
 
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
 
    # Method to play or pause the video
    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
 
    # Method to handle changes in media player state (playing or paused)
    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)
            )
        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)
            )
 
    # Method to handle changes in video position
    def position_changed(self, position):
        self.slider.setValue(position)
 
    # Method to handle changes in video duration
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
    # Method to set the video position
    def set_position(self, position):
        self.mediaPlayer.setPosition(position)
 
    # Method to handle errors in media playback
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
 
# Create the application instance
app = QApplication(sys.argv)
 
# Create the main window instance
window = Window()
 
# Run the application event loop
sys.exit(app.exec_())
