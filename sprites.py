import pygame as pg
import colors
from settings import *
from random import choice, randrange
vec = pg.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert_alpha()
    
    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image
    
    def get_image_heart(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image
    
    def get_image_heart_ly(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image

    def get_breath_drugs(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image

    def get_walk_drugs(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image
    
class Joseph(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.shoot = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(0,0,64,64),
                        self.game.spritesheet.get_image(64,0,64,64),
                        self.game.spritesheet.get_image(128,0,64,64),
                        self.game.spritesheet.get_image(192,0,64,64)]
        for frame in self.standing_frames:
            frame.set_colorkey(colors.BLACK)

        self.walking_frames_r = [self.game.spritesheet.get_image(64,64,64,64),
                        self.game.spritesheet.get_image(128,64,64,64),
                        self.game.spritesheet.get_image(192,64,64,64),
                        self.game.spritesheet.get_image(0,128,64,64)]
        
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(colors.BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))

        self.jumping_frames = [self.game.spritesheet.get_image(0,128,64,64),
                        self.game.spritesheet.get_image(64,128,64,64),
                        self.game.spritesheet.get_image(128,128,64,64),
                        self.game.spritesheet.get_image(192,128,64,64)]
        
        self.punch_frames = [self.game.spritesheet.get_image(0,256,64,64),
                                self.game.spritesheet.get_image(64,256,64,64),
                                self.game.spritesheet.get_image(128,256,64,64)]

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    


    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()
        if keys[pg.K_m]:
            self.shoot = True
            proyectil = Proyectil()
            # Configuramos el proyectil de forma que esté donde el protagonista
            proyectil.rect.x = self.rect.x + 20
            proyectil.rect.y = self.rect.y + 20
            # Añadimos el proyectil a la lista
            self.game.all_sprites.add(proyectil)

        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Ecuaciones de Motricidad
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Se transporta al otro lado de la pantalla(Es bug, si, lo se)
        #if self.pos.x > self.game.map.width + self.rect.width / 2:
            #self.pos.x = 0 - self.rect.width / 2
        #if self.pos.x < 0 - self.rect.width / 2:
            #self.pos.x = self.game.map.width + self.rect.width / 2

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True

        else:
            self.walking = False

        if self.shoot:
               if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.punch_frames)
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom     
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        # show jump animation
        if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                bottom = self.rect.bottom
                if self.vel.y > 0:
                    self.image = self.jumping_frames[self.current_frame]
                else:
                    self.jumping = False
                self.image.set_colorkey(colors.BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        
class Jon_Snow(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def load_images(self):
        self.standing_frames = [self.game.breath_player.get_breath_drugs(0,0,64,64),
                        self.game.breath_player.get_breath_drugs(64,0,64,64),
                        self.game.breath_player.get_breath_drugs(0,64,64,64),
                        self.game.breath_player.get_breath_drugs(64,64,64,64)]
        for frame in self.standing_frames:
            frame.set_colorkey(colors.BLACK)

        self.walking_frames_r = [self.game.walk_player.get_walk_drugs(0,0,64,64),
                        self.game.walk_player.get_walk_drugs(64,0,64,64),
                        self.game.walk_player.get_walk_drugs(0,64,64,64),
                        self.game.walk_player.get_walk_drugs(64,64,64,64),
                        self.game.walk_player.get_walk_drugs(0,128,64,64),
                        self.game.walk_player.get_walk_drugs(64,128,64,64)]
        
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(colors.BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))

        #self.jumping_frames = [self.game.spritesheet.get_image(0,128,64,64),
         #               self.game.spritesheet.get_image(64,128,64,64),
          #              self.game.spritesheet.get_image(128,128,64,64),
           #             self.game.spritesheet.get_image(192,128,64,64)]

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    


    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Ecuaciones de Motricidad
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Se transporta al otro lado de la pantalla(Es bug, si, lo se)
        #if self.pos.x > self.game.map.width + self.rect.width / 2:
            #self.pos.x = 0 - self.rect.width / 2
        #if self.pos.x < 0 - self.rect.width / 2:
            #self.pos.x = self.game.map.width + self.rect.width / 2

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True

        else:
            self.walking = False
        
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        # show jump animation
        if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                bottom = self.rect.bottom
                if self.vel.y > 0:
                    self.image = self.jumping_frames[self.current_frame]
                else:
                    self.jumping = False
                self.image.set_colorkey(colors.BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        
class Mariana(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet_mariana.get_image(0,0,48,64),
                        self.game.spritesheet_mariana.get_image(48,0,48,64),
                        self.game.spritesheet_mariana.get_image(96,0,48,64),
                        self.game.spritesheet_mariana.get_image(144,0,48,64)]
        for frame in self.standing_frames:
            frame.set_colorkey(colors.BLACK)

        self.walking_frames_r = [self.game.spritesheet_mariana.get_image(192,0,48,64),
                        self.game.spritesheet_mariana.get_image(0,64,48,64),
                        self.game.spritesheet_mariana.get_image(48,64,48,64),
                        self.game.spritesheet_mariana.get_image(96,64,48,64),
                        self.game.spritesheet_mariana.get_image(144,64,48,64),
                        self.game.spritesheet_mariana.get_image(192,64,48,64)]
        
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(colors.BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))

        #self.jumping_frames = [self.game.spritesheet.get_image(0,128,64,64),
         #               self.game.spritesheet.get_image(64,128,64,64),
          #              self.game.spritesheet.get_image(128,128,64,64),
           #             self.game.spritesheet.get_image(192,128,64,64)]

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_MAR_JUMP
    


    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()

        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Ecuaciones de Motricidad
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Se transporta al otro lado de la pantalla(Es bug, si, lo se)
        #if self.pos.x > self.game.map.width + self.rect.width / 2:
            #self.pos.x = 0 - self.rect.width / 2
        #if self.pos.x < 0 - self.rect.width / 2:
            #self.pos.x = self.game.map.width + self.rect.width / 2

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True

        else:
            self.walking = False
        
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        # show jump animation
        if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                bottom = self.rect.bottom
                if self.vel.y > 0:
                    self.image = self.jumping_frames[self.current_frame]
                else:
                    self.jumping = False
                self.image.set_colorkey(colors.BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Minion_Depression(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet_minion.get_image(0,0,64,64),
                        self.game.spritesheet_minion.get_image(64,0,64,64),
                        self.game.spritesheet_minion.get_image(128,0,64,64),
                        self.game.spritesheet_minion.get_image(192,0,64,64)]
        for frame in self.standing_frames:
            frame.set_colorkey(colors.BLACK)

        self.walking_frames_r = [self.game.spritesheet_minion.get_image(0,0,64,64),
                        self.game.spritesheet_minion.get_image(64,0,64,64),
                        self.game.spritesheet_minion.get_image(0,64,64,64),
                        self.game.spritesheet_minion.get_image(64,64,64,64),
                        self.game.spritesheet_minion.get_image(0,128,64,64),
                        self.game.spritesheet_minion.get_image(64,128,64,64)]
        
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(colors.BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))

        self.jumping_frames = [self.game.spritesheet_minion.get_image(0,128,64,64),
                        self.game.spritesheet_minion.get_image(64,128,64,64),
                        self.game.spritesheet_minion.get_image(128,128,64,64),
                        self.game.spritesheet_minion.get_image(192,128,64,64)]

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP

    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()
        
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -ENEMY_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = -ENEMY_ACC
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.acc.x = -ENEMY_ACC
        #if self.pos.x < 0:
         #   self.acc.x = -PLAYER_ACC
        #if self.pos.x > 0:
         #   self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Ecuaciones de Motricidad
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Se transporta al otro lado de la pantalla(Es bug, si, lo se)
        #if self.pos.x > self.game.map.width + self.rect.width / 2:
            #self.pos.x = 0 - self.rect.width / 2
        #if self.pos.x < 0 - self.rect.width / 2:
            #self.pos.x = self.game.map.width + self.rect.width / 2

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True

        else:
            self.walking = False
        
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        # show jump animation
        if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                bottom = self.rect.bottom
                if self.vel.y > 0:
                    self.image = self.jumping_frames[self.current_frame]
                else:
                    self.jumping = False
                self.image.set_colorkey(colors.BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Don_Juan(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet_don_juan.get_image(0,0,64,64),
                        self.game.spritesheet_don_juan.get_image(64,0,64,64),
                        self.game.spritesheet_don_juan.get_image(128,0,64,64),
                        self.game.spritesheet_don_juan.get_image(192,0,64,64)]
        for frame in self.standing_frames:
            frame.set_colorkey(colors.BLACK)

        self.walking_frames_r = [self.game.spritesheet_don_juan.get_image(0,64,64,64),
                        self.game.spritesheet_don_juan.get_image(64,64,64,64),
                        self.game.spritesheet_don_juan.get_image(128,64,64,64),
                        self.game.spritesheet_don_juan.get_image(192,64,64,64)]
        
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(colors.BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))

        self.jumping_frames = [self.game.spritesheet_don_juan.get_image(0,128,64,64),
                        self.game.spritesheet_don_juan.get_image(64,128,64,64),
                        self.game.spritesheet_don_juan.get_image(128,128,64,64),
                        self.game.spritesheet_don_juan.get_image(192,128,64,64)]

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    


    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()

        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Ecuaciones de Motricidad
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Se transporta al otro lado de la pantalla(Es bug, si, lo se)
        #if self.pos.x > self.game.map.width + self.rect.width / 2:
            #self.pos.x = 0 - self.rect.width / 2
        #if self.pos.x < 0 - self.rect.width / 2:
            #self.pos.x = self.game.map.width + self.rect.width / 2

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True

        else:
            self.walking = False
        
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        # show jump animation
        if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                bottom = self.rect.bottom
                if self.vel.y > 0:
                    self.image = self.jumping_frames[self.current_frame]
                else:
                    self.jumping = False
                self.image.set_colorkey(colors.BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class El_Macho(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rot = 0

    def load_images(self):
        self.standing_frames = [self.game.spritesheet_macho.get_image(0,0,64,64),
                        self.game.spritesheet_macho.get_image(64,0,64,64),
                        self.game.spritesheet_macho.get_image(128,0,64,64),
                        self.game.spritesheet_macho.get_image(192,0,64,64)]
        for frame in self.standing_frames:
            frame.set_colorkey(colors.BLACK)

        self.walking_frames_r = [self.game.spritesheet_macho.get_image(64,64,64,64),
                        self.game.spritesheet_macho.get_image(128,64,64,64),
                        self.game.spritesheet_macho.get_image(192,64,64,64),
                        self.game.spritesheet_macho.get_image(0,128,64,64)]
        
        self.walking_frames_l = []
        for frame in self.walking_frames_r:
            frame.set_colorkey(colors.BLACK)
            self.walking_frames_l.append(pg.transform.flip(frame,True,False))

        self.jumping_frames = [self.game.spritesheet_macho.get_image(0,128,64,64),
                        self.game.spritesheet_macho.get_image(64,128,64,64),
                        self.game.spritesheet_macho.get_image(128,128,64,64),
                        self.game.spritesheet_macho.get_image(192,128,64,64)]

    def jump(self):
        self.rect.y += 1
        hits = pg.sprite.spritecollide(self,self.game.walls,False)
        self.rect.y -= 1
        if hits:
            self.vel.y = -PLAYER_JUMP
    


    def update(self):
        self.animate()
        self.acc = vec(0,PLAYER_GRAV)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            self.jump()

        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Ecuaciones de Motricidad
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # Se transporta al otro lado de la pantalla(Es bug, si, lo se)
        #if self.pos.x > self.game.map.width + self.rect.width / 2:
            #self.pos.x = 0 - self.rect.width / 2
        #if self.pos.x < 0 - self.rect.width / 2:
            #self.pos.x = self.game.map.width + self.rect.width / 2

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True

        else:
            self.walking = False
        
        # show walk animation
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walking_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walking_frames_r[self.current_frame]
                else:
                    self.image = self.walking_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
            
        # show jump animation
        if self.jumping:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
                bottom = self.rect.bottom
                if self.vel.y > 0:
                    self.image = self.jumping_frames[self.current_frame]
                else:
                    self.jumping = False
                self.image.set_colorkey(colors.BLACK)
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.image.fill(colors.RUBY_RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Camara:
    def __init__(self,width,height):
        self.camera = pg.Rect(0,0,width,height)
        self.width = width
        self.height = height

    def apply(self,entity):
        return entity.rect.move(self.camera.topleft)

    def update(self,target):
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)
        x = min(0,x)
        y = min(0,y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pg.Rect(x,y,self.width,self.height) 

class Map:
    def __init__(self,filename):
        self.data = []
        with open(filename,'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Floor_Depression(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("img/Depression/platform.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        #if randrange(5) < POW_SPAWN_PCT:
            #Pow_Pizza(self.game, self)
        #if randrange(20) < POW_SPAWN_PCT:
            #Pow_Life(self.game,self)

class Floor_Depression_1(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("img/Depression/platform2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        #if randrange(5) < POW_SPAWN_PCT:
            #Pow_Pizza(self.game, self)
        #if randrange(20) < POW_SPAWN_PCT:
            #Pow_Life(self.game,self)

class Floor_Depression_2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("img/Depression/platform3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        #if randrange(5) < POW_SPAWN_PCT:
            #Pow_Pizza(self.game, self)
        #if randrange(20) < POW_SPAWN_PCT:
            #Pow_Life(self.game,self)

class Floor_Drugs(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("img/ladrillo.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Floor(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load("img/transparent_wall.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

class Proyectil(pg.sprite.Sprite):
    def __init__(self):
        #  Llama al constructor de la clase padre (Sprite)
        super().__init__() 
 
        ball = pg.image.load("img/Depression/Energy_Ball.png")
        self.image = ball
        self.image.blit(ball,(0,0))
 
        self.rect = self.image.get_rect()
         
    def update(self):
        """ Desplaza al proyectil. """
        self.rect.x += 3

class Pow_Coin(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(['coin'])
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.heart_ly_animation[0]
        self.image.set_colorkey(colors.BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image
    
    def load_images(self):
        self.heart_ly_animation = [self.game.heart_ly_anim.get_image_heart_ly(0,0,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(64,0,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(128,0,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(0,64,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(64,64,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(128,64,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(0,128,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(64,128,64,64),
                                self.game.heart_ly_anim.get_image_heart_ly(128,128,64,64)]
        for frame in self.heart_ly_animation:
            frame.set_colorkey(colors.BLACK)

    def update(self):
        self.animate()

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 160:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.heart_ly_animation)
            self.image = self.heart_ly_animation[self.current_frame]

class Pow_Coin_Drugs(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(['coin'])
        self.current_frame = 0
        self.last_update = 0
        #self.load_images()
        self.image = pg.image.load("img/marijuana.png").convert_alpha()
        self.image.set_colorkey(colors.BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
class Pow_Pizza(pg.sprite.Sprite):
    def __init__(self, game, wall):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.wall = wall
        self.type = choice(['coin'])
        self.image = pg.image.load("img/Pizza.png").convert_alpha()
        self.image.set_colorkey(colors.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.wall.rect.centerx
        self.rect.bottom = self.wall.rect.top - 5

class Pow_Life(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(['life'])
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.heart_animation[0]
        self.image.set_colorkey(colors.BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        return image
    
    def load_images(self):
        self.heart_animation = [self.game.heart_anim.get_image_heart(0,0,64,64),
                                self.game.heart_anim.get_image_heart(64,0,64,64),
                                self.game.heart_anim.get_image_heart(128,0,64,64),
                                self.game.heart_anim.get_image_heart(0,64,64,64),
                                self.game.heart_anim.get_image_heart(64,64,64,64),
                                self.game.heart_anim.get_image_heart(128,64,64,64),
                                self.game.heart_anim.get_image_heart(0,128,64,64),
                                self.game.heart_anim.get_image_heart(64,128,64,64),
                                self.game.heart_anim.get_image_heart(128,128,64,64)]
        for frame in self.heart_animation:
            frame.set_colorkey(colors.BLACK)

    def update(self):
        self.animate()

     
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 160:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.heart_animation)
            self.image = self.heart_animation[self.current_frame]
        
class Minus_Life(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(['minus_life'])
        self.image = pg.image.load("img/bad_heart.png").convert_alpha()
        self.image.set_colorkey(colors.BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
    
class Door(pg.sprite.Sprite):
    def __init__(self, game, x,y):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.type = choice(['door'])
        self.image = pg.image.load("img/door.png").convert_alpha()
        self.image.set_colorkey(colors.BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
