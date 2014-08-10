'''
Created on 1 mars 2014

@author: efarhan
'''
import math
from engine import level_manager
from engine.const import CONST, log
from engine.stat import get_value
from engine.vector import Vector2


from render_engine.img_manager import img_manager
from render_engine.input import input_manager

from event.physics_event import get_physics_event
from engine.init import engine
from animation.animation_main import Animation
from physics_engine.physics_manager import physics_manager
from render_engine.snd_manager import snd_manager


class PlayerAnimation(Animation):
    def __init__(self,player):
        Animation.__init__(self, player)
        self.foot = 0
        self.player = self.obj
        self.speed = 3
        self.life = 3
        self.gravity = 30.0/60
        self.direction = True #True for right
        self.jump_step = CONST.jump_step
        self.wall = 0 #None=0, Left=1, Right=2
        self.wall_speed = 2.5
        self.wall_jump_step = 0
        self.not_sliding_wall = 0

        self.touched = False
        self.cat_touched = False

        self.invincibility = 0
        self.show_frequency = 10
        self.dialog = 0
        self.attacking = 0
        self.attack_time = 4*7

        self.transition = 1.0

        self.jump_sound = snd_manager.load_sound("data/sound/Jump2.wav")
        self.deal_with_it = img_manager.load_image("data/sprites/dealwithit.png")
        self.heart = img_manager.load_image("data/sprites/heart.png")
        self.deal_pos = Vector2(23,-7)
        self.deal_delta = Vector2(0,-160)
        self.move_deal = False

        self.slash = Animation(None)
        self.slash.root_path = "data/sprites/"
        self.slash.path_list = ["slash/"]
        self.slash.state_range = { "slash": [0,5]}
        self.slash.load_images()


    def load_images(self, size=None, tmp=False):
        Animation.load_images(self, size=size, tmp=tmp)
    
    def update_animation(self, state="", invert=False):
        self.update_state()
        return Animation.update_animation(self, state=state, invert=invert)

    def update_state(self):
        lock = level_manager.level.lock
        RIGHT = input_manager.get_button('RIGHT')
        LEFT = input_manager.get_button('LEFT')
        UP = input_manager.get_button('UP')
        DOWN = input_manager.get_button('DOWN')
        A_BUTTON = input_manager.get_button('A')
        B_BUTTON = input_manager.get_button('B')
        if lock or self.life == 0:
            RIGHT = False
            LEFT = False
            UP = False
            DOWN = False
            A_BUTTON = False
            B_BUTTON = False


        
        horizontal = RIGHT-LEFT
        vertical = UP-DOWN
        
        physics_events = get_physics_event()
        
        for event in physics_events:
            #log("Physics collision: "+str(event.a.userData)+" "+str(event.b.userData)+" "+str(event.begin) +" "+str(physics_manager.get_body_position(self.obj.body).get_tuple()))
            if (event.a.userData == 2 and 15 >= event.b.userData >= 11 ) or \
                    ( event.b.userData == 2 and 15 >= event.a.userData >= 11):
                if event.begin:
                    self.foot += 1
                else:
                    self.foot -= 1
            elif (event.a.userData == 3 and event.b.userData == 11 ) or \
                    ( event.b.userData == 3  and event.a.userData == 11):
                if event.begin:
                    self.wall = 1
                else:
                    self.wall = 0

            elif (event.a.userData == 4 and event.b.userData == 11 ) or \
                    ( event.b.userData == 4  and event.a.userData == 11):
                if event.begin:
                    self.wall = 2
                else:
                    self.wall = 0
            elif (event.a.userData == 3 and 15 >= event.b.userData > 11 ) or \
                    ( event.b.userData == 3  and 15 >= event.a.userData > 11):
                log("Physics: "+str(event.a.userData)+" "+str(event.b.userData))
                if event.begin:
                    self.not_sliding_wall = 1
                else:
                    self.not_sliding_wall = 0

            elif (event.a.userData == 4 and 15 >= event.b.userData > 11 ) or \
                    ( event.b.userData == 4  and 15 >= event.a.userData > 11):
                log("Physics: "+str(event.a.userData)+" "+str(event.b.userData))
                if event.begin:
                    self.not_sliding_wall = 2
                else:
                    self.not_sliding_wall = 0
            elif (event.a.userData == 1 and event.b.userData >= 20 and event.b.userData % 10 == 0) or \
                    ( event.b.userData == 1 and event.a.userData >= 20 and event.a.userData % 10 == 0):
                log("Touched by cat")
                if event.begin:
                    self.touched = True
                    self.cat_touched = True
                else:
                    self.touched = False
            elif (event.a.userData == 1 and event.b.userData >= 20 and event.b.userData %10 != 0) or \
                    ( event.b.userData == 1 and event.a.userData >= 20 and event.a.userData %10 != 0):
                log("Touched by bullet")
                if event.begin:
                    self.touched = True
                else:
                    self.touched = False
            if (event.a.userData == 1 and event.b.userData == 13 ) or \
                    ( event.b.userData == 1 and event.a.userData == 13):
                log("Touched by spike")
                if event.begin:
                    self.touched = True
                else:
                    self.touched = False





        if self.invincibility:
            self.invincibility -= 1

        if A_BUTTON and ((self.foot and self.jump_step) or (not self.foot and self.jump_step and self.wall)):
            if self.wall == 1:
                #going RIGHT because LEFT wall
                physics_manager.move(self.player.body, vx=self.speed)
                self.wall_jump_step = CONST.wall_jump

            elif self.wall == 2:
                physics_manager.move(self.player.body, vx=-self.speed)
                self.wall_jump_step = CONST.wall_jump
            physics_manager.jump(self.player.body)
            snd_manager.play_sound(self.jump_sound)
            self.jump_step -= 1
        elif not self.foot and not self.wall :
            self.jump_step = 0
        elif (self.foot or (not self.foot and self.wall)) and not A_BUTTON:
            self.jump_step = CONST.jump_step



        if horizontal == -1:
            #LEFT
            self.direction = False
            if self.foot:
                self.state = 'move'
            self.player.flip = True

            move_condition = self.wall != 1 and self.wall_jump_step == 0 and self.not_sliding_wall != 1
            if get_value('boss_limit') is not None:
                move_condition = move_condition and (self.player.pos + \
                                                    self.player.screen_relative_pos * \
                                                    engine.screen_size).x > get_value('boss_limit')[0]
            if move_condition:
                physics_manager.move(self.player.body, -self.speed)
        elif horizontal == 1:
            #RIGHT
            self.direction = True
            if self.foot:
                self.state = 'move'
            self.player.flip = False

            move_condition = self.wall != 2 and self.wall_jump_step == 0 and self.not_sliding_wall != 2
            if get_value('boss_limit') is not None:
                move_condition = move_condition and (self.player.pos + \
                                                    self.player.screen_relative_pos * \
                                                    engine.screen_size ).x < get_value('boss_limit')[1]
            if move_condition:
                physics_manager.move(self.player.body, self.speed)
        else:
            if self.foot:
                if self.direction:
                    self.state = 'still'
                    self.player.flip = False
                else:
                    self.state = 'still'
                    self.player.flip = True
            if self.wall_jump_step == 0:
                physics_manager.move(self.player.body, 0)

        if not self.foot:
            if self.direction:
                self.state = 'jump'
                self.player.flip = False
            else:
                self.state = 'jump'
                self.player.flip = True



        #"gravity" effect like nes game
        velocity = physics_manager.get_body_velocity(self.player.body)
        delta = self.gravity
        if self.wall and self.wall_jump_step == 0:
            velocity.y = self.wall_speed
            self.state = 'slide'
            if self.direction:
                self.player.flip = False
            else:
                self.player.flip = True
        elif self.foot:
            pass
        else:
            velocity.y += delta
        physics_manager.set_body_velocity(self.player.body, velocity)

        physics_pos = physics_manager.get_body_position(self.player.body)
        
        if physics_pos:
            pos = physics_pos-self.player.size/2
        else:
            pos = self.player.pos
        if self.player.screen_relative_pos:
            pos = pos-self.player.screen_relative_pos*engine.get_screen_size()
        self.player.pos = pos

        self.set_screen_pos()

        if self.wall_jump_step != 0:
            self.wall_jump_step -= 1

        for i in range(self.life):
            img_manager.show_image(self.heart,img_manager.buffer,pos=Vector2(i*18,0),new_size=Vector2(16,16))

        if self.move_deal:
            if self.deal_delta.y < 0:
                self.deal_delta = Vector2(0,self.deal_delta.y+1)
            elif self.dialog == 0:
                self.deal_delta = Vector2()
                if engine.textbox.finished:
                    if input_manager.get_button('A') or input_manager.get_button('B'):
                        snd_manager.set_playlist(["data/music/menu_gbjam.ogg"])
                        self.dialog = -1
                        engine.textbox.set_text("Furbrawl", "A game by Team KwaKwa")

            if not self.direction:
                self.deal_delta = Vector2(-20,self.deal_delta.y)
            else:
                self.deal_delta = Vector2(0, self.deal_delta.y)

        if self.dialog == -1 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 1
                engine.textbox.set_text("Lead designer", "Elias Farhan")
        if self.dialog == 1 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 2
                engine.textbox.set_text("Programmer", """Hamza "Tenchi" Haiken""")
        if self.dialog == 2 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 3
                engine.textbox.set_text("Artist", """Josh Grilli""")
        if self.dialog == 3 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 4
                engine.textbox.set_text("Artist", """Austin Lewis""")
        if self.dialog == 4 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 5
                engine.textbox.set_text("Music", """Dorian SRed""")
        if self.dialog == 5 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                self.dialog = 6
                engine.textbox.set_text("THANKS", """For playing the game""")
        if self.dialog == 6 and engine.textbox.finished:
            if input_manager.get_button('A') or input_manager.get_button('B'):
                engine.show_dialog = False
                from levels.logo_kwakwa import Kwakwa
                level_manager.switch_level(Kwakwa())
        if self.touched and not self.invincibility and self.life > 0:
            self.life -= 1
            self.invincibility = CONST.invincibility
            self.anim_counter = self.anim_freq-1

            if self.life == 0:
                level_manager.level.game_over = True
                self.invincibility = 1000
            if self.cat_touched:
                self.touched = False
                self.cat_touched = False
        if self.invincibility > CONST.invincibility - 20 or level_manager.level.game_over:
            self.state = 'hit'

        if self.invincibility %20 > 10:
            self.player.show = False
        else:
            self.player.show = True

        if B_BUTTON and self.attacking == 0:
            self.state = 'attack'
            self.attacking = self.attack_time
        if self.attacking > 1:
            self.state = 'attack'
            self.attacking -= 1
            self.slash.update_animation(state='slash')
            slash_pos = Vector2()
            if self.direction:
                slash_pos = self.player.pos + engine.screen_size * self.player.screen_relative_pos + Vector2(self.player.size.x/1.5,0)
            else:
                slash_pos = self.player.pos + engine.screen_size * self.player.screen_relative_pos - Vector2(self.player.size.x/1.5,0)
            img_manager.show_image(self.slash.img, engine.screen, pos=slash_pos-level_manager.level.screen_pos,new_size=Vector2(36,36),flip=not self.direction)
        elif not B_BUTTON:
            self.attacking = 0
        if ( self.player.pos + engine.screen_size * self.player.screen_relative_pos ).x > 2500:
            from levels.dialog import Dialog
            boss_level = Dialog()
            boss_level.last_checkpoint = level_manager.level.last_checkpoint
            level_manager.switch_level(boss_level)
    def set_screen_pos(self):
        player_pos = self.player.pos + self.player.screen_relative_pos*engine.screen_size
        pos_ratio = player_pos/engine.screen_size
        pos_size_ratio = (player_pos+self.player.size)/engine.screen_size
        size_ratio = pos_size_ratio-pos_ratio
        """
        Transition



        x_delta = 0

        if math.floor(pos_size_ratio.x)-math.floor(pos_ratio.x) == 1:
            x_delta = (int(pos_size_ratio.x)-pos_ratio.x)/size_ratio.x
        y_delta = 0

        if math.floor(pos_size_ratio.y)-math.floor(pos_ratio.y) == 1:
            y_delta = (int(pos_size_ratio.y)-pos_ratio.y)/size_ratio.y

        level_manager.level.screen_pos = Vector2(160*(math.floor(pos_size_ratio.x)-x_delta), )
        """
        y_pos = 0
        if (1000 > player_pos.x > 800) or (2257 > player_pos.x > 2057):
            y_delta = 0

            if math.floor(pos_size_ratio.y)-math.floor(pos_ratio.y) == 1:
                y_delta = (int(pos_size_ratio.y)-pos_ratio.y)/size_ratio.y
            y_pos = 144*(math.floor(pos_size_ratio.y)-y_delta)
        elif (1100 > player_pos.x >= 1000) or (2357 > player_pos.x >= 2257):
            y_pos = self.player.pos.y

        level_manager.level.screen_pos = Vector2(self.player.pos.x, y_pos)
    @staticmethod
    def parse_animation(anim_data):
        Animation.parse_animation(anim_data)