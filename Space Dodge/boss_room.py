import pygame, sys, time, random, menu
from pygame.locals import *
import os

pygame.font.init()
pygame.mixer.init()



ship_hit = pygame.mixer.Sound("ship_hit.mp3")
star_hit = pygame.mixer.Sound("star_hit.mp3")
blaster = pygame.mixer.Sound("blaster.mp3")
laser_noise = pygame.mixer.Sound("laser.mp3")
shield_noise = pygame.mixer.Sound("shield_sound.mp3")

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 800
player_speed = 5
player_health = 3
boss_health = 300

bullet_speed = 6
star_speed = 5

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Dodge")


#load image
BG = pygame.transform.scale(pygame.image.load("background.jpg"), (screen_width, screen_height))

FONT30 = pygame.font.SysFont("comicsans", 30)
FONT50 = pygame.font.SysFont("comicsans", 50)

def draw_bg():
     screen.blit(BG, (0,0))

#player
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Ship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_rem = health
        self.is_shielded = False
        self.is_3guns = False
        self.fast_shot = False
        self.laser = False
        self.last_shot = pygame.time.get_ticks()
    
    def activate_shield(self):
        self.is_shielded = True
        # Set a timer to deactivate the shield, 5 seconds
        pygame.time.set_timer(USEREVENT + 1, 5000)  # USEREVENT is a custom event type provided by pygame
    
    def activate_tripleshot(self):
        # Set a timer to deactivate the 3 shot, 5 seconds
        self.is_3guns = True
        pygame.time.set_timer(USEREVENT + 2, 5000)
    
    def activate_fastshot(self):
        # Set a timer to deactivate the fast shot, 5 seconds
        self.fast_shot = True
        pygame.time.set_timer(USEREVENT + 3, 2000)
        
    def activate_lazer(self):
        self.fast_shot = False
        self.is_3guns = False
        self.laser = True

    def update(self):

        game_state = 0
        #moves
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= player_speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += player_speed
        if keys[pygame.K_UP] and self.rect.top >= 0:
            self.rect.y -= player_speed
        if keys[pygame.K_DOWN] and self.rect.bottom < screen_height - 25:
            self.rect.y += player_speed
        
        if self.is_shielded:
            pygame.draw.circle(screen, (0, 0, 255), self.rect.center , self.rect.width, 2)

        time_now = pygame.time.get_ticks()

        if self.fast_shot:
            cooldown = 200
        else:
            cooldown = 500
       
        #shoot
        
        if keys[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            blaster.set_volume(0.05)
            laser_noise.set_volume(0.1)
            if self.is_3guns:
                blaster.play()
                bullet = Bullets(self.rect.centerx - 15, self.rect.top)
                bullet2 = Bullets(self.rect.centerx , self.rect.top)
                bullet3 = Bullets(self.rect.centerx + 15, self.rect.top)
                bullet_group.add(bullet, bullet2, bullet3)
            
            elif self.laser:
                laser_noise.play()
                laser = Laser(self.rect.centerx , self.rect.bottom - 310)
                laser_group.add(laser)
                self.laser = False
                
            else:
                blaster.play()
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet) 
            
            self.last_shot = time_now
            
        #update mask
        self.mask = pygame.mask.from_surface(self.image)
       
        #draw health bar
        pygame.draw.rect(screen, "red", (self.rect.x, (self.rect.bottom + 10), self.rect.width, 10))
        if self.health_rem > 0:
            pygame.draw.rect(screen, "green", (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_rem / self.health_start)), 10))
        elif spaceship.health_rem == 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 4)
            explosion_group.add(explosion)
            self.kill()
            game_state = -1
        
        if pygame.sprite.spritecollide(self, boss_group, False, pygame.sprite.collide_mask):
            if spaceship.is_shielded == False:
                spaceship.health_rem -=1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            ship_hit.set_volume(0.2)
            ship_hit.play()
            
        
        return game_state

    def reset(self):
        self.health_rem= self.health_start
        self.rect.center = [screen_width / 2, screen_height - 100]  # Reset position
        spaceship_group.add(spaceship)
        self.laser = False

#bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= bullet_speed
        if self.rect.bottom < 0:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)    
        
        if pygame.sprite.spritecollide(self, boss_group, False, pygame.sprite.collide_mask):
            boss.health_rem -=1
            self.kill()
            star_hit.set_volume(0.05)
            star_hit.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
        
        if pygame.sprite.spritecollide(self, boss_bullets_group, True, pygame.sprite.collide_mask):
            self.kill()
            star_hit.set_volume(0.05)
            star_hit.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)

#laser
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("power_ups\laser.png"), (200,600))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= bullet_speed * 2
        if -self.rect.bottom > screen_width:
            self.kill()

        self.mask = pygame.mask.from_surface(self.image)    
        
        if pygame.sprite.spritecollide(self, boss_group, False, pygame.sprite.collide_mask):
            boss.health_rem -= 0.50
            star_hit.set_volume(0.05)
            star_hit.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
        
        if pygame.sprite.spritecollide(self, boss_bullets_group, True, pygame.sprite.collide_mask):
            boss.health_rem -= 1
            star_hit.set_volume(0.05)
            star_hit.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosion_group.add(explosion)
            
#explosion
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for item in range(1, 4):
            img = pygame.image.load(f"explosion/frame{item}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            if size == 4:
                img = pygame.transform.scale(img, (300, 300))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 3
        self.counter += 1
        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

#boss
class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("boss.png"), (600, 500))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y - 600]
        self.health_start = health
        self.health_rem = health
        self.spot = y
        self.entry = False
        self.move_direction = 1
        self.shoot_timer = 0
        self.shoot_interval = 100

    def update(self):

        if not self.entry:
            # Move down slowly until reaching the target y position
            if self.rect.centery < self.spot:
                self.rect.centery += 2  # Adjust the speed as needed
            else:
                self.entry = True
        #move
        
        self.rect.x += self.move_direction
        if self.rect.right >= screen_width or self.rect.left <= 0:
            self.move_direction *= -1 

        #shoot
        if self.health_rem < self.health_start / 2:
            self.shoot_interval = 45    
        self.shoot_timer += 1
        if self.shoot_timer > self.shoot_interval:
            bullet = Boss_bullets(self.rect.centerx, self.rect.bottom / 1.5)
            bullet2 = Boss_bullets(self.rect.centerx -200, self.rect.bottom / 1.5)
            bullet3 = Boss_bullets(self.rect.centerx +200, self.rect.bottom / 1.5)
            boss_bullets_group.add(bullet, bullet2, bullet3)
            if self.health_rem < self.health_start / 4:
                bullet4 = Boss_bullets((self.rect.centerx + random.randint(-200, 200)), self.rect.bottom / 1.5)
                boss_bullets_group.add(bullet4)  # Make sure to define this group in your main game loop
            self.shoot_timer = 0  
        
        
        #update mask
        self.mask = pygame.mask.from_surface(self.image)
       
        #draw health bar
        pygame.draw.rect(screen, "red", (self.rect.x, (self.rect.top + 150), self.rect.width, 10))
        if self.health_rem > 0:
            pygame.draw.rect(screen, "green", (self.rect.x, (self.rect.top + 150), int(self.rect.width * (self.health_rem / self.health_start)), 10))
        
        elif self.health_rem == 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 4)
            explosion_group.add(explosion)
            self.kill()

    def reset(self):
        self.health_rem= self.health_start
        self.rect.center = [int(screen_width/2), -400]  
        self.entry = False
        self.shoot_interval = 100
        boss_group.add(boss)


#boss_bullets
class Boss_bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Star.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += star_speed
        if self.rect.bottom > screen_height + 80:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            if spaceship.is_shielded == False:
                spaceship.health_rem -=1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            ship_hit.set_volume(0.2)
            ship_hit.play()
            self.kill()
        
#power-ups
class Power_ups(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        pygame.sprite.Sprite.__init__(self)
        if type == "shield":
            self.image = pygame.transform.scale(pygame.image.load("power_ups\shield.png"), (50,50))
        if type == "tripleshot":
            self.image = pygame.transform.scale(pygame.image.load("power_ups\iplehot.png"), (50,50))
        if type == "fast_shot":
            self.image = pygame.transform.scale(pygame.image.load("power_ups\_fast_shot.png"), (50,50))
        if type == "lazer":
            self.image = pygame.transform.scale(pygame.image.load("power_ups\laser.png"), (50,50))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.type = type

    def update(self):

        self.rect.y += star_speed
        if self.rect.top > screen_height:
            self.kill()
        
        #update mask
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            if self.type == "shield":
                spaceship.activate_shield()
                shield_noise.set_volume(0.1)
                shield_noise.play()
            if self.type == "tripleshot":
                spaceship.activate_tripleshot()
            if self.type == "fast_shot":
                spaceship.activate_fastshot()
            if self.type == "lazer":
                spaceship.activate_lazer()
            self.kill()

# create sprite groups
spaceship_group = pygame.sprite.Group() 
bullet_group = pygame.sprite.Group()
boss_bullets_group = pygame.sprite.Group()
boss_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
power_up_group = pygame.sprite.Group()
laser_group = pygame.sprite.Group()


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x - img.get_width()/2, y - img.get_height()/2)) 

def spawn_power_up():
    if random.randint(0, 1000) <= 1:  
        x = random.randint(20, screen_width - 20)
        power_up = Power_ups(x, -10, "shield")  
        power_up_group.add(power_up)
    if random.randint(0, 1500) <= 1:  
        x = random.randint(20, screen_width - 20) 
        power_up2 = Power_ups(x, -10, "tripleshot")  
        power_up_group.add(power_up2)
    if random.randint(0, 1250) <= 1: 
        x = random.randint(20, screen_width - 20) 
        power_up3 = Power_ups(x, -10, "fast_shot")  
        power_up_group.add(power_up3) 
    if random.randint(0, 1700) <= 1: 
        x = random.randint(20, screen_width - 20) 
        power_up4 = Power_ups(x, -10, "lazer")  
        power_up_group.add(power_up4)  
    
#Create player
spaceship = Spaceship(int(screen_width/2), screen_height - 150, player_health)
spaceship_group.add(spaceship)
#Create boss
boss = Boss(int(screen_width/2), 200, boss_health)
boss_group.add(boss)

def game_boss():
    run = True
    
    game_state = 0
    
    end_time = 0
    elapsed_time = 0
    start_time = time.time()

    start_count = 0 #when we get the next star

    while run:  #gameloop
        start_count += clock.tick(fps)

        draw_bg()
        
        if game_state == 0:

            #time
            elapsed_time = time.time() - start_time
            time_text = FONT30.render(f"Time: {round(elapsed_time)}s", 1, "white")
            screen.blit(time_text, (10, 10))

            if elapsed_time > 20:
                spawn_power_up()
                
            #update spaceship and game state
            game_state = spaceship.update()
            
            #update sprite groups
            bullet_group.update()
            boss_bullets_group.update()
            power_up_group.update()
            laser_group.update()
            boss_group.update()

            #draw sprite groups
            spaceship_group.draw(screen)
            bullet_group.draw(screen)
            boss_group.draw(screen)
            boss_bullets_group.draw(screen)
            power_up_group.draw(screen)
            laser_group.draw(screen)

            #check boss hp and change game state
            if boss.health_rem == 0:
                game_state = 1
                
        else:
            if game_state == -1:    
                draw_text("Game Over", FONT50, "white", screen_width / 2, screen_height / 2)
                draw_text("Press R to restart or M for menu", FONT30, "white", screen_width / 2, screen_height / 2 + 100)
            elif game_state == 1:  
                draw_text("You Win!!", FONT50, "white", screen_width / 2, screen_height / 2)
                draw_text("Press R to restart or M for menu", FONT30, "white", screen_width / 2, screen_height / 2 + 100)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                boss_bullets_group.empty()
                bullet_group.empty()
                power_up_group.empty()
                spaceship.reset()
                boss.reset()
                game_state = 0
                start_time = time.time()
                pygame.mixer.music.play(-1)
                
        #update animations
        explosion_group.update()
        #draw sprite groups
        spaceship_group.draw(screen)
        explosion_group.draw(screen)
        
        #events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m and (game_state == -1 or game_state == 1):
                        boss_bullets_group.empty()
                        bullet_group.empty()
                        power_up_group.empty()
                        spaceship.reset()
                        boss.reset()
                        game_state = 0
                        start_time = time.time()
                        pygame.mixer.music.load("menu_song.mp3")
                        pygame.mixer.music.play(-1, 0.0)
                        menu.main_menu()
                        break

                if event.type == USEREVENT + 1:  # The shield timer expired
                    spaceship.is_shielded = False
                    pygame.time.set_timer(USEREVENT + 1, 0) # stop the timer
                if event.type == USEREVENT + 2:
                    spaceship.is_3guns = False
                    pygame.time.set_timer(USEREVENT + 2, 0) 
                if event.type == USEREVENT + 3:
                    spaceship.fast_shot = False
                    pygame.time.set_timer(USEREVENT + 3, 0)

        pygame.display.update()
    pygame.quit()
  