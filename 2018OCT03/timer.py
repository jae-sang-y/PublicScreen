import pygame, time, datetime
from pygame.locals import *
import re, random
import urllib.request
import get_food
from firebase import firebase
import moviepy.editor
from pygame.locals import *
import threading, time, pytube, os, shutil
import numpy as np
from moviepy.decorators import requires_duration

class timer:
    font = 0
    draw_string = 0
    FONT_SIZE =  100
    times = []
    dates = []
    back_color = (5,5,0)
    text_color = (255,255,255)
    tick = 0
    SPACE = 1
    change = 0
    last_t = -1
    data = None
    fb = None
    clip = None
    W = 0
    H = 0

    movie_start = 0
    movie_run = False
    movie_buf = None
    movie_title = ''
    
    right_text = ''
    rt_life = 0
    rt_cursor = 0
    
    tube_list = ''
    tube_key = ''
    tube_csr = 0
    tube_busy = False
    tube_queue = False
    tube_title = ''
    
    def get_youtube(self, link):
        self.tube_busy = True

        try:
            yt = pytube.YouTube(link)
            self.tube_title = yt.title[0:min(60,len(yt.title))]
            print('start download ' + self.tube_title)

            flt = yt.streams.filter(mime_type='video/mp4', audio_codec='mp4a.40.2')
            print('i have item as ',(flt.fmt_streams))
            flt.first().download('',filename='queue')
            print('end download ' + self.tube_title)
        except:
            self.tube_busy = False
            print('error cant download movie')
            return
        self.tube_queue = True
        print('end tube_queue=== ' + str(self.tube_queue))
        self.tube_busy = False
        
        
    def add_time(self,hour, min, sub,tag=''):
        obj = {}
        obj['h'] = hour
        obj['m'] = min
        obj['sub'] = sub
        obj['tag'] = tag
        self.times.append(obj)
    def add_tag_t(self, str):
        self.times[-1]['tag'] += str
    def __init__(self, draw_string,w,h):
        self.W = w
        self.H = h
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
        #self.clip = moviepy.editor.VideoFileClip('play.mp4')
        random.seed(int(time.time() * 10000000 % 100000))
        self.fb = firebase.FirebaseApplication('https://public-screen.firebaseio.com', None)
        
        delay = 0
        self.font3 = pygame.font.Font('unifont-11.0.02.ttf',self.FONT_SIZE//2)
        self.font4 = pygame.font.Font('unifont-11.0.02.ttf',self.FONT_SIZE//4)
        self.font = pygame.font.Font('unifont-11.0.02.ttf',self.FONT_SIZE)
        self.font5 = pygame.font.Font('unifont-11.0.02.ttf',self.FONT_SIZE * 4 // 5)
        self.font2 = pygame.font.Font('unifont-11.0.02.ttf',int(self.FONT_SIZE * 1.5))
        self.draw_string = draw_string

        self.add_time(6,20,'기상',tag='{평일}{아침}')
        self.add_time(6,30,"아침점호",tag='{평일}{아침}')
        self.add_time(7,20,'아침 식사',tag='{평일}{아침}')
        self.add_time(7,50,'등교',tag='{평일}{자율}')
        self.add_time(8,30,'조례',tag='{평일}')
        #self.add_time(8,30,'쉬는 시간',tag='{평일}{자율}')
        self.add_time(8,40,'1교시',tag='{평일}')
        self.add_time(9,30,'쉬는시간',tag='{평일}{자율}')
        self.add_time(9,40,'2교시',tag='{평일}')
        self.add_time(10,30,'쉬는시간',tag='{평일}{자율}')
        self.add_time(10,40,'3교시',tag='{평일}{점심}')
        self.add_time(11,30,'쉬는시간',tag='{평일}{점심}{자율}')
        self.add_time(11,40,'4교시',tag='{평일}{점심}')
        self.add_time(12,30,'점심시간',tag='{평일}{점심}{자율}')
        
        
        self.add_time(13,20,'5교시',tag='{평일}')
        self.add_time(14,10,'쉬는시간',tag='{평일}{자율}')
        self.add_time(14,20,'6교시',tag='{평일}')
        self.add_time(15,10,'쉬는시간',tag='{평일}{자율}')
        self.add_time(15,20,'7교시',tag='{평일}')
        
        self.add_time(16,10,'종례 및 청소',tag='{평일}')
        
        self.add_time(16,30,'8교시',tag='{평일}')
        self.add_time(17,20,'쉬는시간',tag='{평일}{저녁}{자율}')
        self.add_time(17,30,'9교시',tag='{평일}{저녁}')
        
        self.add_time(18,20,'저녁시간',tag='{평일}{저녁}{자율}')
        self.add_time(19,10,'자율1교시',tag='{평일}')
        self.add_time(20,00,'쉬는시간',tag='{평일}{자율}')
        self.add_time(20,10,'자율2교시',tag='{평일}')

        self.add_time(21,00,'기숙사 이동',tag='{평일}{자율}')
        self.add_time(21,20,'개인시간',tag='{평일}{자율}')
        self.add_time(22,20,'저녁점호',tag='{평일}')
        self.add_time(22,30,'',tag='{평일}')

        self.add_time(8,10,'아침점호',tag='{휴일}{아침}')
        self.add_time(8,30,'오전일과',tag='{휴일}{자율}{점심}')
        self.add_time(12,40,'점심시간',tag='{휴일}{자율}{점심}')
        self.add_time(13,20,'오후일과',tag='{휴일}{자율}{저녁}')
        self.add_time(18,00,'저녁시간',tag='{휴일}{자율}{저녁}')
        self.add_time(19,10,'야간일과',tag='{휴일}{자율}')
        self.add_time(21,20,'개인시간',tag='{휴일}{자율}')
        self.add_time(21,40,'저녁점호',tag='{휴일}')
        #self.add_time(23,20,'테스트',tag='{휴일}')
        self.add_time(21,50,'',tag='{휴일}')

        #pygame.mixer.music.load('track 01.mp3')

    def tag_cond(self, t, dt):
        r = False
        if t['tag'].find('{평일}')>=0 and dt.weekday() < 5:
            r = True
        if t['tag'].find('{휴일}')>=0 and dt.weekday() >= 5:
            r = True
        return r
    def env_set(self, t_i):
        #if (t_i['tag'].find('{아침}') >= 0 or t_i['tag'].find('{점심}') >= 0  or t_i['tag'].find('{저녁}') >= 0) and t_i['tag'].find('{자율}')>=0:
        #    if not pygame.mixer.music.get_busy():
        #            pygame.mixer.music.play(1)
        #elif pygame.mixer.music.get_busy():
        #    pygame.mixer.music.stop()
        if 6 < t_i['h'] <= 18:
            r,g,b = self.text_color
            if r > 0:
                r -= 1
            if g > 0:
                g -= 1
            if b > 0:
                b -= 1
            self.text_color = (r,g,b)
            r,g,b = self.back_color
            if r < 250:
                r += 1
            if g < 250:
                g += 1
            if b < 250:
                b += 1
            self.back_color = (r,g,b)
        else:
            r,g,b = self.text_color
            if r < 250:
                r += 1
            if g < 250:
                g += 1
            if b < 250:
                b += 1
            self.text_color = (r,g,b)
            r,g,b = self.back_color
            if r > 0:
                r -= 1
            if g > 0:
                g -= 1
            if b > 0:
                b -= 1
            self.back_color = (r,g,b)


    def step(self, surf):
        for event in pygame.event.get(): # event handling loop
            #if event.type == QUIT:
            #    return False
            #    break
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    #self.swit0 = not self.swit0
                    break
                elif event.key == K_q:
                    return False
                    break
        
        surf.fill(self.back_color)
        
        dt = datetime.datetime.now() + datetime.timedelta(seconds=29)        
        string = None
        next_time = None

        t_t = 0
        t_i = -1
        for t in self.times:
            if t['h'] * 60 + t['m'] <= dt.hour * 60 + dt.minute:
                if t_t < t['h'] * 60 + t['m']:
                    if self.tag_cond(t, dt):
                        string = t['sub']
                        t_i = t
                        t_t = t['h'] * 60 + t['m']
        
        t_tt = 24 * 60
        for t in self.times:
            if t_t < t['h'] * 60 + t['m'] < t_tt:
                if self.tag_cond(t, dt):
                    t_tt = t['h'] * 60 + t['m']

        if self.SPACE != 1:
            self.SPACE += (1 - self.SPACE) * 0.2

        if t_i != -1:
            self.env_set(t_i)
            if t_i['tag'].find('{아침}') >= 0 or t_i['tag'].find('{점심}') >= 0 or t_i['tag'].find('{저녁}') >= 0:
                if self.change > 290:
                    if t_i['tag'].find('{아침}') >= 0:
                        self.data = get_food.get_food(0)
                        self.change = 0
                    elif t_i['tag'].find('{점심}') >= 0:
                        self.data = get_food.get_food(1)
                        self.change = 0
                    elif t_i['tag'].find('{저녁}') >= 0:
                        self.data = get_food.get_food(2)
                        self.change = 0
                if self.change == 0 and self.data != None:
                    i = 0
                    for s in self.data:
                        self.draw_string(self.font3,surf, s,x=-self.FONT_SIZE*3.5, y = (self.SPACE - 1)*0.5*self.FONT_SIZE*(-len(self.data)/2 + 0.5 + i),  color = self.text_color)
                        #self.draw_string(self.font3,surf, s,x=self.FONT_SIZE*3.5, y = (self.SPACE - 1)*0.5*self.FONT_SIZE*(-len(self.data)/2 + 0.5 + i),  color = self.text_color)
                        i += 1
                    if self.SPACE != 2.85:
                        self.SPACE += (2.85 - self.SPACE) * 0.4

            if string != '' and string != None:
                self.draw_string(self.font5,surf,string,x=-self.FONT_SIZE*3.5,y=-self.FONT_SIZE*self.SPACE,  color = self.text_color)
                #self.draw_string(self.font,surf,string,x=self.FONT_SIZE*3.5,y=-self.FONT_SIZE*self.SPACE,  color = self.text_color)
                ddt = datetime.datetime(year = dt.year, month = dt.month, day = dt.day,hour = t_tt // 60, minute = t_tt % 60) - dt
                if ddt.seconds // 60 >= 60:
                    string = "%s:%s:%s"%("{:02d}".format(ddt.seconds // 3600),"{:02d}".format((ddt.seconds // 60) % 60), "{:02d}".format(ddt.seconds % 60))
                else:
                    string = "%s:%s"%("{:02d}".format((ddt.seconds // 60)), "{:02d}".format(ddt.seconds % 60))
                self.draw_string(self.font,surf,string,x=-self.FONT_SIZE*3.5,y=self.FONT_SIZE*self.SPACE,  color = self.text_color)
                temp_y = -self.H // 4
                if self.rt_life < 200:
                    temp_y+=self.FONT_SIZE*(((200 - self.rt_life) / (200)) ** 2 * 6)
                elif self.rt_life > 1000 - 200:
                    temp_y-=self.FONT_SIZE*(((1000 - 200 - self.rt_life) / (200)) ** 2 * 6)

                if self.right_text != None:
                    j = 0
                    for _ in self.right_text:
                        if j == self.rt_cursor:
                            i = 0
                            lines = self.right_text[_].split('\\n')
                            for s in lines:
                                #print(i)
                                self.draw_string(self.font3,surf, s,x=self.W // 4, y = temp_y+(self.SPACE)*0.5*self.FONT_SIZE*(i - (len(lines) - 1) / 2),  color = self.text_color)
                                i += 1
                            break
                        j += 1
                self.draw_string(self.font4,surf,'http://대소고.oa.to/',x=-self.W * 0.25,y = self.H / 2 - self.FONT_SIZE / 4, color = self.text_color)
                #if self.movie_av:
                if self.clip == None:
                    if self.tube_queue:
                        if t_i['tag'].find('{자율}') >= 0 or True:
                            shutil.copy2('queue.mp4','play.mp4')
                            self.clip = moviepy.editor.VideoFileClip('play.mp4')
                            print('NOne Movie Start---')
                            self.movie_title = self.tube_title
                            self.tube_quere = False
                            self.movie_run = True
                            self.movie_start = time.time()
                            if self.clip.audio != None:
                                videoFlag = threading.Event()
                                audioFlag = threading.Event()
                                audiothread = threading.Thread(target=self.clip.audio.preview, args=(22050, 3000, 2, audioFlag, videoFlag))
                                audiothread.start()
                                videoFlag.set()
                                audioFlag.wait()
                        else:
                            pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                            self.draw_string(self.font4,surf,'Sleep',x=self.W * 0.25,y = self.H *0.25, color = self.back_color)
                        
                    else:
                        pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                        self.draw_string(self.font4,surf,'영상 로드 중',x=self.W * 0.25,y = self.H *0.25, color = self.back_color)
                        if not self.tube_busy:
                            self.tube_csr += 1
                            if self.tube_csr >= len(self.tube_key):
                                self.tube_list = self.fb.get('tube', None)
                                self.tube_key = list(self.tube_list.keys())
                                random.shuffle(self.tube_key, random.random)
                                self.tube_csr = 0
                            j = 0

                            print('get new movie1')
                            for _ in self.tube_key:
                                if j == self.tube_csr:
                                    threading.Thread(target=self.get_youtube,args=(self.tube_list[_],)).start()
                                    break
                                j += 1
                            
                elif t_i['tag'].find('{자율}') >= 0 or True:
                    
                    if self.movie_run:
                        #print(2222 + str(time.time() - self.movie_start < self.clip.duration-.001))
                        if time.time() - self.movie_start < self.clip.duration-.001:
                            pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                            if self.tick % 2 == 0:
                                self.movie_buf = pygame.transform.scale(pygame.surfarray.make_surface(self.clip.get_frame(time.time() - self.movie_start).swapaxes(0, 1)), (640 * (360 - self.FONT_SIZE // 2) // 360,360 - self.FONT_SIZE // 2))
                            if self.movie_buf != None:
                                surf.blit(self.movie_buf, (640 + 640 * self.FONT_SIZE // 4 // 360, 360))
                            leftov_time= int(self.clip.duration-.001 - (time.time() - self.movie_start))
                            
                            pygame.draw.rect(surf, self.back_color, (640,720-self.FONT_SIZE // 4- self.FONT_SIZE / 4,640,self.FONT_SIZE // 4 + self.FONT_SIZE / 4))
                            if leftov_time >= 60:
                                self.draw_string(self.font4,surf,self.movie_title + ' : %d분 %d초'%(leftov_time//60,leftov_time % 60),x=self.W * 0.25,y = self.H / 2 - self.FONT_SIZE / 4, color = self.text_color)
                            else:
                                self.draw_string(self.font4,surf,self.movie_title + ' : %d초'%(leftov_time),x=self.W * 0.25,y = self.H / 2 - self.FONT_SIZE / 4, color = self.text_color)
                            
                        else: #Video End
                            print('End Please')
                            if self.tube_queue:
                                print('Not Azik')
                                self.clip.close()
                                try:
                                    os.remove('play.mp4')
                                    print('328')
                                    shutil.copy2('queue.mp4','play.mp4')
                                    print('330')
                                    self.clip = moviepy.editor.VideoFileClip('play.mp4')
                                    print('333')
                                    self.movie_title = self.tube_title
                                    self.tube_queue = False
                                    self.movie_run = False
                                    print('i remove queue', self.tube_queue)
                                    print('movie end!!!')
                                except:
                                    print('failed remove')
                            else:
                                print('End Azik')
                                pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                                self.draw_string(self.font4,surf,'영상 로드 중',x=self.W * 0.25,y = self.H *0.25, color = self.back_color)
                    else:
                        if self.clip.audio != None:
                            videoFlag = threading.Event()
                            audioFlag = threading.Event()
                            audiothread = threading.Thread(target=self.clip.audio.preview, args=(22050, 3000, 2, audioFlag, videoFlag))
                            audiothread.start()
                            videoFlag.set()
                            audioFlag.wait()
                        self.movie_run = True
                        self.movie_start = time.time()
                        print('play movie %s' % self.movie_title)
                        if self.tube_queue:
                            print('queue exist')
                        if self.tube_busy:
                            print('tube busy')

                    if not (self.tube_queue or self.tube_busy):
                        self.tube_csr += 1
                        if self.tube_csr >= len(self.tube_key):
                            self.tube_list = self.fb.get('tube', None)
                            self.tube_key = list(self.tube_list.keys())
                            random.shuffle(self.tube_key, random.random)
                            self.tube_csr = 0
                        print('get new movie2')
                        j = 0
                        for _ in self.tube_key:
                            if j == self.tube_csr:
                                threading.Thread(target=self.get_youtube,args=(self.tube_list[_],)).start()
                                break
                            j += 1
                    #else:
                    #    #True
                    #    pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                    #    self.draw_string(self.font4,surf,'영상 로드 중',x=self.W * 0.25,y = self.H *0.25, color = self.back_color)
                else:
                    pygame.draw.rect(surf, self.text_color, (640,360,640,360))
                    self.draw_string(self.font4,surf,'대구소프트웨어고등학교',x=self.W * 0.25,y = self.H *0.25, color = self.back_color)
                        
            else:
                string = 'Sleep'
                if self.tick % 400 < 100:
                    string += '.'
                elif self.tick % 400 < 200:
                    string += '..'
                elif self.tick % 400 < 300:
                    string += '...'
                self.draw_string(self.font,surf,string, color = self.text_color)
            if self.last_t != t_i:
                self.change = 300
                self.data = None
            self.last_t = t_i

        if self.change > 0:
            self.change -= 1
        if self.rt_life == 0:
            self.rt_life = 1000
            self.rt_cursor += 1
            if self.rt_cursor >= len(self.right_text):
                self.right_text = self.fb.get('notice', None)
                #self.right_text = self.right_text.replace('\\n','\n').split('\r')
                self.rt_cursor = 0
                

        self.rt_life -= 1
        self.tick = (self.tick + 1) % (32768)
        return True     