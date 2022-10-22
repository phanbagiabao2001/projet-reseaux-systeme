"""the main Menu screen"""
import pygame.mixer

from .button_class import ButtonM
from .menu_class import Menu
from pygame import mixer
from .settings_for_menu import *
import pygame as pg
import sys
from queue import Queue
from connection import wrapper
import atexit
import time
from share_data import getRXQueue,getTXQueue, getRBQueue
from multiprocessing import Process

def callbackTest(x,y,z,t,h) :
    getRXQueue().put([x,y,z,t,h])
    getRBQueue().put([x,y,z,t,h])
    print('x : {}, y : {}, id : {}, t : {}, h : {}'.format(x,y,z,t,h))

def process_connection(local_port,remote_port,remote_ip,q : Queue) :
    if wrapper.init_peer(local_port,remote_port,remote_ip) == False :
        exit()
    wrapper.register_callback(wrapper.callbackType()(callbackTest))
    while(True) :
        if q.empty() :
            time.sleep(1.0)
        else :
            coor = q.get()
            wrapper.send_peer(coor[0],coor[1],coor[2],coor[3],coor[4])

class All_menus(Menu):
    pg.init()

    def __init__(self):

        Menu.__init__(self)
        self.connection = None
        self.running = False

    def get_connection(self) :
        return self.connection

    def display_main(self):
        if self.displayed:

            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            New_Game = ButtonM(self.screen, self.mid_width, self.mid_height - GAP, 'New Game')
            Multiplayer = ButtonM(self.screen, self.mid_width, self.mid_height + (2 * GAP), 'Multiplayer')
            loaded_Games = ButtonM(self.screen, self.mid_width, self.mid_height, 'Load Game')
            Settings = ButtonM(self.screen, self.mid_width, self.mid_height + GAP, 'Settings')
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3 * GAP), 'Quit')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Age of Cheap Empires", True, (249, 231, 159)),
                                 (self.mid_width - (3.5*GAP), self.mid_height - (2.5 * GAP)))
                if New_Game.check_button():
                    self.start = True
                    run = False

                if loaded_Games.check_button():
                    self.load = True
                    run = False

                if Quit.check_button():
                    run = False
                    sys.exit()

                if Settings.check_button():
                    self.current = "Settings"
                    self.display_settings()
                    run = False

                if Multiplayer.check_button():
                    self.current = "Multiplayer"
                    self.display_multiplayer()
                    run = False
                

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        sys.exit()

                pg.display.update()
                clock.tick(30)

    def display_pause(self):
        if self.displayed:

            self.current = "Pause"
            self.pause = True
            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3*GAP), 'Quit')
            Resume = ButtonM(self.screen, self.mid_width, self.mid_height - GAP*2, 'Resume')
            Settings = ButtonM(self.screen, self.mid_width, self.mid_height + GAP, 'Settings')
            Save = ButtonM(self.screen, self.mid_width, self.mid_height + 2*GAP, 'Save Game')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Pause", True, (249, 231, 159)), (self.mid_width*0.98, self.mid_height - GAP*3.25))

                if Settings.check_button():
                    self.current = "Settings"
                    self.display_settings()
                    run = False

                if Resume.check_button():
                    self.pause = False
                    run = False

                if Quit.check_button():
                    self.pause = False
                    run = False
                    sys.exit()

                if Save.check_button():
                    self.save = True
                    self.pause = False
                    run = False

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()

                pg.display.update()
                clock.tick(30)

    def display_settings(self):
        if self.displayed:

            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            Vol_up = ButtonM(self.screen, self.mid_width + (3.5*GAP), self.mid_height + GAP, '+')
            Vol_down = ButtonM(self.screen, self.mid_width - (3.5*GAP), self.mid_height + GAP, '-')
            Return = ButtonM(self.screen, self.mid_width, self.mid_height - GAP * 1.5, 'Return')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Settings", True, (249, 231, 159)), (self.mid_width*0.97, self.mid_height - GAP*3.25))
                self.screen.blit(self.font2.render("Volume", True, (249, 231, 159)), (self.mid_width * 0.98 + (0.6 * GAP), self.mid_height + GAP))

                if Vol_up.check_button():
                    if self.volume > 0.0 :
                        self.volume -= 0.1
                        mixer.music.set_volume(self.volume)

                if Vol_down.check_button():
                    if self.volume < 1.0:
                        self.volume += 0.1
                        mixer.music.set_volume(self.volume)

                if Return.check_button():
                    run = False
                    if not self.pause:
                        self.current = "Main"
                        self.display_main()
                    else:
                        self.current = "Pause"
                        self.display_pause()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()

                pg.display.update()
                clock.tick(30)
    
    def display_multiplayer(self):
        if self.displayed:

            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            Create_room = ButtonM(self.screen, self.mid_width + (2.5*GAP), self.mid_height + GAP, 'Create Room')
            Join_room = ButtonM(self.screen, self.mid_width - (2.5*GAP), self.mid_height + GAP, 'Join Room')
            Return = ButtonM(self.screen, self.mid_width, self.mid_height + (3.75*GAP), 'Return')
            
            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Multiplayer", True, (249, 231, 159)), (self.mid_width*0.97, self.mid_height - GAP*3.25))
                
                if Create_room.check_button():
                    self.current = "Join_room"
                    self.display_join_room()
                    run = False

                if Join_room.check_button():
                    self.current = "Join_room"
                    self.display_join_room()
                    run = False
                
                if Return.check_button():
                    run = False
                    if not self.pause:
                        self.current = "Main"
                        self.display_main()
                    else:
                        self.current = "Pause"
                        self.display_pause()
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()

                pg.display.update()
                clock.tick(30)
            
    def display_join_room(self):
        if self.displayed:
            clock = pygame.time.Clock()
            pg.display.set_caption('Age of Cheap Empires')
            # buttons
            Return = ButtonM(self.screen, self.mid_width, self.mid_height + (3.5*GAP), 'Return')
            Join = ButtonM(self.screen, 200,300 , 'Join')
            
            input_localPort_rect = pygame.Rect(250, 150, 200, 32)
            input_PeerIP_rect = pygame.Rect(250, 200, 200, 32)
            input_PeerPort_rect = pygame.Rect(250, 250, 200, 32)
            color_active1 = pygame.Color('lightskyblue3')
            color_passive1 = pygame.Color('chartreuse4')
            color_active2 = pygame.Color('chocolate')
            color_passive2 = pygame.Color('yellow')
            color_active3 = pygame.Color('red4')
            color_passive3 = pygame.Color('red1')
            
            color1 = color_passive1
            color2 = color_passive2
            color3 = color_passive3
            
            base_font = pygame.font.Font(None, 32)
            IP_text = ''
            Port_text = ''
            Local_Port_text = ''

            active1 = False
            active2 = False
            active3 = False
            
            run = True
            
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Multiplayer", True, (249, 231, 159)), (self.mid_width*0.97, self.mid_height - GAP*3.25))
                self.screen.blit(self.font3.render("Local PORT", True, (249, 231, 159)), (100, 150 ))
                self.screen.blit(self.font3.render("Peer IP", True, (249, 231, 159)), (100, 200 ))
                self.screen.blit(self.font3.render("Peer PORT", True, (249, 231, 159)), (100, 255 ))
               
                if Return.check_button():
                    run = False
                    if not self.pause:
                        self.current = "Main"
                        self.display_main()
                    else:
                        self.current = "Pause"
                        self.display_pause()
          
                if Join.check_button():
                    run = False
                    if (self.connection == None) :
                        self.connection = Process(target = process_connection, args=(int(Local_Port_text), int(Port_text), str(IP_text), getTXQueue()))
                        self.connection.start()
                    # conn.join() = True
                    # self.start = True
                    # conn.join() = True
                    # run = False
                  
                    # self.start = True
                    # run = False
                    
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if input_PeerIP_rect.collidepoint(event.pos):
                            active1 = True
                        else:
                            active1 = False
                        if input_PeerPort_rect.collidepoint(event.pos):
                            active2 = True
                        else:
                            active2 = False
                        if input_localPort_rect.collidepoint(event.pos):
                            active3 = True
                        else:
                            active3 = False
                    if active1 and event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            IP_text = IP_text[:-1]
                        else:
                            IP_text += event.unicode
                    if active2 and event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            Port_text = Port_text[:-1]
                        else:
                            Port_text += event.unicode
                    if active3 and event.type == pg.KEYDOWN:
                        if event.key == pg.K_BACKSPACE:
                            Local_Port_text = Local_Port_text[:-1]
                        else:
                            Local_Port_text += event.unicode
                if active1:
                    color1 = color_active1
                else:
                    color1 = color_passive1
                if active2:
                    color2 = color_active2
                else:
                    color2 = color_passive2
                if active3:
                    color3 = color_active3
                else:
                    color3 = color_passive3
                    
                pg.draw.rect(self.screen, color3, input_localPort_rect)
                pg.draw.rect(self.screen, color1, input_PeerIP_rect)
                pg.draw.rect(self.screen, color2, input_PeerPort_rect)
                
                text_surface_localPort = base_font.render(Local_Port_text, True, (255, 255, 255))
                text_surface_IP = base_font.render(IP_text, True, (255, 255, 255))
                text_surface_Port = base_font.render(Port_text, True, (255, 255, 255))
                
                self.screen.blit(text_surface_localPort, (input_localPort_rect.x+5, input_localPort_rect.y+5))
                self.screen.blit(text_surface_IP, (input_PeerIP_rect.x+5, input_PeerIP_rect.y+5))
                self.screen.blit(text_surface_Port, (input_PeerPort_rect.x+5, input_PeerPort_rect.y+5))
                
                input_localPort_rect.w = max(200, text_surface_localPort.get_width()+10)
                input_PeerIP_rect.w = max(200, text_surface_IP.get_width()+10)
                input_PeerPort_rect.w = max(200, text_surface_Port.get_width()+10)
                
                pg.display.update()
                clock.tick(30)
    
if __name__ == '__main__':
    pg.init()
    All_menus().display_main()