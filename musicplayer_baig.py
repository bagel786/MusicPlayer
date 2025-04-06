import sys, random
from PySide6.QtWidgets import QLabel, QPushButton, QToolButton, QFrame, QApplication, QMainWindow, QLineEdit, QProgressBar
from PySide6.QtCore import Qt, QTimer
from PySide6 import QtCore
from PySide6.QtGui import QFont, QFontDatabase, QScreen, QPixmap, QIcon
import time
import os

import pygame
pygame.init()
pygame.mixer.init()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.setWindowTitle("Music Player")
        self.setFixedSize(1280,720)
        self.setStyleSheet('background-color:#364044;')
        self.setCentralWidget(MusicPlayer(self))
       
class Song():
    def __init__(self, album_pic, artist, name, file):
        self.album_pic = album_pic
        self.artist = artist
        self.name = name
        self.file = file    


class MusicPlayer(QFrame):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.load_components()
        running = True
        self.pause = False
        self.skip = False

        # while running:
        #     for event in pygame.event.get():
        #         if event.type == pygame.USEREVENT:
        #             if pygame.mixer.music.get_busy() == 0:
        #                 # If music ends, play the next song
        #                 print('hello')
        #                 self.next()
       


    def load_components(self):
        self.song_info = []
        
        self.header = QLabel('Saf\'s Music Player', self)
        self.header.setGeometry(600, 25, 150,20)
        self.header.setStyleSheet('font-size:20px;color:white;font-style:italic;') 
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.song = QLabel( self)
        self.song.setGeometry(475, 75, 400,500)
        self.song.setStyleSheet('background-color:#8b9ba2;border-radius:10px;')
        self.songs = [['assets/no_idea.png', 'Don Toliver', 'No Idea', 'assets/noidea.mp3'], ['assets/just_wanna_rock.png', 'Lil Uzi Vert', 'Just Wanna Rock', 'assets/rock.mp3'], ['assets/snooze.png', 'SZA', 'Snooze', 'assets/snooze.mp3'], 
                     ['assets/realer.png', 'Future, Juice WRLD','Realer n realer' , 'assets/future.mp3'], ['assets/for_the_night.png', 'Pop Smoke', 'For The Night', 'assets/pop.mp3'], 
                     ['assets/saturn.png', 'SZA', 'Saturn', 'assets/saturn.mp3'], ['assets/you.png', 'Don Toliver', 'You', 'assets/you.mp3'],['assets/lovesick.png', 'Don Toliver', 'Private Landing', 'assets/private_landing.mp3'], ['assets/for_the_night.png', 'Pop Smoke', 'Welcome To The Party', 'assets/welcome.mp3'],
                       ['assets/america.png', '21 Savage','Nee-Nah', 'assets/neenah.mp3'], ['assets/utopia.png', 'Travis Scott', 'My Eyes', 'assets/myeyes.mp3'], ['assets/america.png', '21 Savage','Redrum', 'assets/redrum.mp3'], ['assets/utopia.png', 'Travis Scott', 'K-Pop', 'assets/kpop.mp3'], 
                       ['assets/utopia.png', 'Travis Scott', 'Skitzo', 'assets/skitzo.mp3'], ['assets/astro.png', 'Travis Scott', 'Stargazing', 'assets/stargazing.mp3'], ['assets/rodeo.png', 'Travis Scott', 'Nightcrawler', 'assets/night.mp3'],['assets/birds.png', 'Travis Scott', 'Sdp Interlude', 'assets/sdp.mp3']
                       , ['assets/astro.png', 'Travis Scott', 'Sicko Mode', 'assets/sicko.mp3'], ['assets/utopia.png', 'Travis Scott', 'Telekenesis', 'assets/telekenesis.mp3'], ['assets/utopia.png', 'Travis Scott', 'Meltdown', 'assets/meltdown.mp3'], ['assets/astro.png', 'Travis Scott', 'Skeletons', 'assets/skeletons.mp3']]
        for song in self.songs:
            self.song_info.append(Song(song[0], song[1], song[2], song[3]))

        self.stopped = False
        self.toolbar = QLabel(self)
        self.toolbar.setGeometry(475, 595, 400,80)
        self.toolbar.setStyleSheet('border-radius:10px;background-color:black;')
        self.play_button = QToolButton(self)
        self.play_button.setGeometry(640, 600, 60,65)
        self.play_button.setStyleSheet('background-image:url(assets/playbutton.png);border-radius:10px;background-color:transparent;')
        self.play_button.hide()
        self.play_button.clicked.connect(self.play_music)
        self.shuffle = QToolButton(self)
        self.next_song = QToolButton(self)
        self.next_song.setGeometry(700, 620, 40,40)
        self.next_song.setStyleSheet('background-image:url(assets/next_song.png);border-radius:10px;background-color:transparent;')
        self.last_song = QToolButton(self)
        self.last_song.setGeometry(600, 620, 40,35)
        self.last_song.setStyleSheet('background-image:url(assets/last_song.png);border-radius:10px;background-color:transparent;')
        
        self.shuffle_button = QToolButton(self)
        self.shuffle_button.setGeometry(490, 600, 65,65)
        self.shuffle_button.setStyleSheet('background-color:transparent;')
        shuffle_image = QPixmap('assets/shuffle.png')
        scaled_image = shuffle_image.scaled(120,120)
        icon = QIcon(scaled_image)
        self.shuffle_button.setIcon(icon)
        self.shuffle_button.setIconSize(scaled_image.size())

        self.load_music(random.randint(0,19))
        print(self.index)
        self.next_song.clicked.connect(self.next)
        self.last_song.clicked.connect(self.back)
        self.shuffle_button.clicked.connect(self.shuffle_songs)

       
        self.pause_button = QToolButton(self)
        self.pause_button.setGeometry(640, 600, 60,60)  # Adjusted geometry for scaled image
        self.pause_button.setStyleSheet('background-color:transparent;')

        pause_image = QPixmap('assets/pause.png')
        scaled_image = pause_image.scaled(120,120)
        icon = QIcon(scaled_image)
        self.pause_button.setIcon(icon)
        self.pause_button.setIconSize(scaled_image.size())
        self.pause_button.clicked.connect(self.pause_music)

        self.stop_button = QToolButton(self)
        self.stop_button.setGeometry(800, 600, 60,60)  
        self.stop_button.setStyleSheet('background-color:transparent;')
        stop_image = QPixmap('assets/stop.png')
        scaled_image = stop_image.scaled(120,120)
        icon = QIcon(scaled_image)
        self.stop_button.setIcon(icon)
        self.stop_button.setIconSize(scaled_image.size())
        self.stop_button.clicked.connect(self.stop_music)

        self.fast_forward = QToolButton(self)
        self.fast_forward.setGeometry(740, 600, 60,60)
        self.fast_forward.setStyleSheet('background-color:transparent;')
        fast_image = QPixmap('assets/forward.png')
        scaled_image = fast_image.scaled(30,30)
        icon = QIcon(scaled_image)
        self.fast_forward.setIcon(icon)
        self.fast_forward.setIconSize(scaled_image.size())
        self.fast_forward.clicked.connect(self.fast)
        

        self.backward = QToolButton(self)
        self.backward.setGeometry(550, 600, 60,60)
        self.backward.setStyleSheet('background-color:transparent;')
        back_image = QPixmap('assets/backward.png')
        scaled_image = back_image.scaled(30,30)
        icon = QIcon(scaled_image)
        self.backward.setIcon(icon)
        self.backward.setIconSize(scaled_image.size())
        self.backward.clicked.connect(self.rewind)

     
   

    def shuffle_songs(self):
        random.shuffle(self.song_info)
    def stop_music(self):
        pygame.mixer.music.stop()
        self.play_button.show()
        self.pause_button.hide()
        self.stopped = True

    def next(self):
        playing = True
        self.song_image.hide()
        self.song_title.hide()
        self.timestamp.hide()
        self.play_time.hide()
        self.clock_time.hide()
        self.pause_button.show()
        self.play_button.hide()

        if self.index == 19:
            self.index = 0
        else:
            self.index+=1
        self.current_song = self.song_info[self.index]
        self.current_song = self.song_info[self.index]
        self.song_image = QLabel(self)
        self.song_image.setGeometry(510, 80, 395,445)
        self.image = QPixmap(self.current_song.album_pic)
        self.song_image.setPixmap(self.image)
        self.song_image.setStyleSheet('background-color:transparent;')
        scaled_image = self.image.scaled(315,400)
        self.song_image.setPixmap(scaled_image)
        self.song_title = QLabel(f'{self.current_song.artist} - {self.current_song.name}',self)
        self.song_title.setGeometry(550, 530, 395, 30)
        self.song_title.setStyleSheet('background-color:transparent;color:white;font-size:20px;')
        pygame.mixer.music.load(self.current_song.file)
        pygame.mixer.music.play()
        self.played_time=0
        self.timestamp = QLabel('0:00',self)
        self.timestamp.setGeometry(500, 510, 395, 30)
        self.timestamp.setStyleSheet('background-color:transparent;color:white;font-size:10px;')
        self.clock_time = QProgressBar(self)
        self.clock_time.setGeometry(515, 510, 300, 10)
        self.clock_time.setMinimum(0)
        self.song_length = pygame.mixer.Sound(self.current_song.file).get_length()
        self.clock_time.setMaximum(pygame.mixer.Sound(self.current_song.file).get_length())
        self.minutes = self.song_length//60
        self.seconds = (self.song_length%60)//1
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_timer)
        # self.timer.start(1000)
        self.play_time = QLabel(f"{int(self.minutes):01}:{int(self.seconds):02}", self)
        self.play_time.setGeometry(800, 520, 50, 10)
        self.play_time.setStyleSheet('color:white;font-size:10px;background-color:transparent;')
       
        self.song_title.show()
        self.song_image.show()
        self.timestamp.show()
        self.clock_time.show()
        self.play_time.show()


    def back(self):

        self.song_image.hide()
        self.song_title.hide()
        self.timestamp.hide()
        self.clock_time.hide()
        self.play_time.hide()
        self.pause_button.show()
        self.play_button.hide()

        if self.index == 0:
            self.index = 19
        else:
            self.index-=1
        self.current_song = self.song_info[self.index]
        self.song_image = QLabel(self)
        self.song_image.setGeometry(510, 80, 395,445)
        self.image = QPixmap(self.current_song.album_pic)
        self.song_image.setPixmap(self.image)
        self.song_image.setStyleSheet('background-color:transparent;')
        scaled_image = self.image.scaled(315,400)
        self.song_image.setPixmap(scaled_image)
        self.song_title = QLabel(f'{self.current_song.artist} - {self.current_song.name}',self)
        self.song_title.setGeometry(550, 530, 395, 30)
        self.song_title.setStyleSheet('background-color:transparent;color:white;font-size:20px;')
        pygame.mixer.music.load(self.current_song.file)
        pygame.mixer.music.play()
        self.played_time=0
        self.timestamp = QLabel('0:00',self)
        self.timestamp.setGeometry(500, 510, 395, 30)
        self.timestamp.setStyleSheet('background-color:transparent;color:white;font-size:10px;')
        self.clock_time = QProgressBar(self)
        self.clock_time.setGeometry(515, 510, 300, 10)
        self.clock_time.setMinimum(0)
        self.song_length = pygame.mixer.Sound(self.current_song.file).get_length()
        self.clock_time.setMaximum(pygame.mixer.Sound(self.current_song.file).get_length())
        self.minutes = self.song_length//60
        self.seconds = (self.song_length%60)//1
        self.play_time = QLabel(f"{int(self.minutes):01}:{int(self.seconds):02}", self)
        self.play_time.setGeometry(800, 520, 50, 10)
        self.play_time.setStyleSheet('color:white;font-size:10px;background-color:transparent;')
       
        self.song_title.show()
        self.song_image.show()
        self.timestamp.show()
        self.clock_time.show()
        self.play_time.show()
    def pause_music(self):
        pygame.mixer.music.pause()
        self.play_button.show()
        self.pause_button.hide()
        self.pause = True

    def play_music(self):
        if self.stopped == True:
            pygame.mixer.music.play()
            self.play_button.hide()
            self.pause_button.show()
            self.clock_time.setValue(0)
            self.timestamp.setText('0:00')
            self.played_time = 0
            self.stopped = False
        else:
            pygame.mixer.music.unpause()
            self.pause = False
        self.play_button.hide()
        self.pause_button.show()
    def load_music(self, x):
        self.current_song = self.song_info[x]
        playing = True
        self.song_image = QLabel(self)
        self.song_image.setGeometry(510, 80, 395,445)
        self.index = x
        self.image = QPixmap(self.current_song.album_pic)
        self.song_image.setPixmap(self.image)
        self.song_image.setStyleSheet('background-color:transparent;')
        scaled_image = self.image.scaled(315,400)
        self.song_image.setPixmap(scaled_image)
        self.song_title = QLabel(f'{self.current_song.artist} - {self.current_song.name}',self)
        self.song_title.setGeometry(550, 530, 395, 30)
        self.song_title.setStyleSheet('background-color:transparent;color:white;font-size:20px;')
        pygame.mixer.music.load(self.current_song.file)
        pygame.mixer.music.play()
        self.played_time=0
        self.timestamp = QLabel('0:00',self)
        self.timestamp.setGeometry(500, 510, 395, 30)
        self.timestamp.setStyleSheet('background-color:transparent;color:white;font-size:10px;')
        self.clock_time = QProgressBar(self)
        self.clock_time.setGeometry(515, 510, 300, 10)
        self.clock_time.setMinimum(0)
        self.song_length = pygame.mixer.Sound(self.current_song.file).get_length()
        self.clock_time.setMaximum(pygame.mixer.Sound(self.current_song.file).get_length())
        self.minutes = self.song_length//60
        self.seconds = (self.song_length%60)//1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.play_time = QLabel(f"{int(self.minutes):01}:{int(self.seconds):02}", self)
        self.play_time.setGeometry(800, 520, 50, 10)
        self.play_time.setStyleSheet('color:white;font-size:10px;background-color:transparent;')

        
       

        
    def update_timer(self):
        if pygame.mixer.music.get_busy()==1:
            self.current_time = pygame.mixer.music.get_pos()//1000
            self.played_time+=1
            self.minutes = self.played_time//60
            self.seconds = self.played_time%60
            print(self.minutes, self.seconds)
            if self.played_time > 60:
                self.minutes = self.played_time//60
                self.seconds = self.played_time%60
                self.time = f'{self.minutes}:{self.seconds}'
                self.timestamp.setText(self.time)
            if self.seconds<10:
                self.timestamp.setText(f'{self.minutes}:{0}{self.seconds}')
            else:
                self.timestamp.setText(f'{self.minutes}:{self.seconds}')
            self.clock_time.setValue(self.played_time)
        while pygame.mixer.music.get_busy()==0 and self.pause == False and self.skip == False and self.stopped == False:
            self.next()
     
    def rewind(self):
        if self.played_time-10 >=0 and pygame.mixer.music.get_busy()==1:
            self.skip = True
            self.played_time-=10
            self.minutes = self.played_time//60
            self.seconds = self.played_time%60
            pygame.mixer.music.play(loops=0, start=self.played_time, fade_ms = 0)
            pygame.mixer.music.unpause()
            if self.minutes>0 and self.seconds>10:
                print('grr')
                self.timestamp.setText(f'{self.minutes}:{self.seconds}')
            if self.seconds<10:
                self.timestamp.setText(f'{self.minutes}:{0}{self.seconds}')
            else:
                self.timestamp.setText(f'{self.minutes}:{self.seconds}')
            self.clock_time.setValue(self.played_time)
            self.skip = False



    def fast(self):
        if self.played_time+10 <=self.clock_time.maximum() and pygame.mixer.music.get_busy()==1:
            self.skip = True

            self.played_time+=10
            self.minutes = self.played_time//60
            self.seconds = self.played_time%60
            pygame.mixer.music.play(loops=0, start=self.played_time, fade_ms = 0)
            pygame.mixer.music.unpause()
            
            print(self.minutes, self.seconds, f'{self.minutes}:{self.seconds}')
            if self.minutes>0 and self.seconds>10:
                self.timestamp.setText(f'{self.minutes}:{self.seconds}')
            if self.seconds<10:
                self.timestamp.setText(f'{self.minutes}:{0}{self.seconds}')
            else:
                self.timestamp.setText(f'{self.minutes}:{self.seconds}')
            self.clock_time.setValue(self.played_time)
            self.skip = False

        
        
if __name__ == '__main__':
    app = QApplication(sys.argv) 
    window = Window()
    center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
    geo = window.frameGeometry()
    geo.moveCenter(center)
    window.move(geo.topLeft())
    window.show()
    sys.exit(app.exec())
