import sys
from threading import *
from pytube import YouTube
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import * # Don't import all, it will flood the namespace


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Youtube Downloader")
        self.setWindowIcon(QIcon("resources/images/logo.png"))
        width = 1600
        height = 450
        self.setGeometry(415, 225, width , height)
        self.setFixedSize(width, height)
        self.setStyleSheet("background: #EEEEEE;")
        self.Uicomponents()
        self.show()
        
        
    def Uicomponents(self):
        # Header Label
        head = QLabel("YouTube Downloader", self)
        head.setGeometry(0, 20, 600, 60)
        head.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_id = QFontDatabase.addApplicationFont(r"resources/fonts/PermanentMarker-Regular.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[0], 20)
        head.setFont(font)
        head.setStyleSheet("background: #EEEEEE; color: #000;")
    
        # YouTube Link Label
        l_label = QLabel("YouTube Link", self)
        l_label.setGeometry(20, 130, 180, 40)
        l_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font_id = QFontDatabase.addApplicationFont(r"resources/fonts/OpenSans.ttf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        font = QFont(families[0], 10)
        l_label.setFont(font)
        l_label.setStyleSheet("background: #FF3737;"
                              "border-radius: 5px;"
                              "color: #fff;")
        
        # Input field for the link
        self.link = QLineEdit(self)
        self.link.setGeometry(220, 130, 360, 40) 
        font = QFont(families[0], 8)
        self.link.setFont(font)
        self.link.setStyleSheet("""
                                QLineEdit {
                                background: #fff;
                                border: 2px solid black;
                                }
                                """)
        
        # Button 1 (Download Video)
        video = QPushButton("Download Video", self)
        video.setGeometry(110, 210, 180, 50)
        video.clicked.connect(self.threading_video)
        video.setFont(font)
        video.setStyleSheet("""
                            QPushButton {
                                border: 1px solid black;
                                border-radius: 4px;
                                background: #fff;
                            }
                            QPushButton:hover {
                                background: #FF9999;
                            }
                            QPushButton:pressed {
                                background: #FF3737;
                                color: #fff;
                                border: none;
                            }
                            """)
        
        # Button 2 (Download Audio Only)
        audio = QPushButton("Download Audio", self)
        audio.setGeometry(310, 210, 180, 50)
        audio.clicked.connect(self.threading_audio)
        audio.setFont(font)
        audio.setStyleSheet("""
                            QPushButton {
                                border: 1px solid black;
                                border-radius: 4px;
                                background: #fff;
                            }
                            QPushButton:hover {
                                background: #FF9999;
                            }
                            QPushButton:pressed {
                                background: #FF3737;
                                color: #fff;
                                border: none;
                            }                    
                            """)

        # Progress Bar
        self.p_bar = QProgressBar(self)
        self.p_bar.setGeometry(100, 340, 400, 40)
        self.p_bar.setStyleSheet("QProgressBar:chunk { background-color: #FF3737;}")
        self.p_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        # Waiting Label
        self.w_label = QLabel("Waiting...", self)
        self.w_label.setGeometry(100, 300, 400, 40)
        self.w_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.w_label.setFont(font)
        self.w_label.setHidden(True)
        
        
    def on_complete(self, stream, filepath):
        self.link.clear()
        self.p_bar.setFormat("Completed!")
    

    def on_progress(self, stream, chunk, bytes_remaining):        
        self.w_label.setHidden(True)
        self.progress = int((100 - (bytes_remaining / stream.filesize * 100)))
        self.p_bar.setValue(self.progress)

            
            
    def download_video(self):
        self.p_bar.reset()
        self.p_bar.resetFormat()
        
        try:
            self.w_label.setHidden(False)
            video_object = YouTube(self.link.text(), on_complete_callback=self.on_complete, on_progress_callback=self.on_progress)
            video_object.streams.get_highest_resolution().download()
        except:
            self.w_label.setHidden(True)
        

    def threading_video(self):
        t1 = Thread(target = self.download_video)
        t1.start()
    
    
    def download_audio(self):
        self.p_bar.reset()
        self.p_bar.resetFormat()
        
        try:
            self.w_label.setHidden(False)
            audio_object = YouTube(self.link.text(), on_complete_callback=self.on_complete, on_progress_callback=self.on_progress)
            audio_object.streams.get_audio_only().download()
        except:
            self.w_label.setHidden(True)
    
    
    def threading_audio(self):
        t2 = Thread(target = self.download_audio)
        t2.start() 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
