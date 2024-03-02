import pygame, sys, time, random, menu
from pygame.locals import *

pygame.font.init()
pygame.mixer.init()

pygame.mixer.music.load("space.mp3")
pygame.mixer.music.play(-1, 0.0)  # Loop the music indefinitely
pygame.mixer.music.set_volume(0.1)


ship_hit = pygame.mixer.Sound("ship_hit.mp3")
star_hit = pygame.mixer.Sound("star_hit.mp3")
blaster = pygame.mixer.Sound("blaster.mp3")

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 800
player_speed = 5
player_health = 3

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
        self.last_shot = pygame.time.get_ticks()
    
    
    
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
        
        time_now = pygame.time.get_ticks()
        cooldown = 500
        #shoot
        if keys[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            blaster.set_volume(0.05)
            blaster.play() 
            bullet = Bullets(self.rect.centerx, self.rect.top)
            #bullet2 = Bullets(self.rect.centerx , self.rect.top)
            #bullet3 = Bullets(self.rect.centerx + 18, self.rect.top)
            bullet_group.add(bullet)  #, bullet2, bullet3)
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
            #self.kill()
            game_state = -1
        return game_state

    def reset(self):
        self.health_rem= self.health_start
        self.rect.center = [screen_width / 2, screen_height - 100]  # Reset position

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
        
        if pygame.sprite.spritecollide(self, star_group, True, pygame.sprite.collide_mask):
            self.kill()
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

#stars
class Stars(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Star.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, -10]

    def update(self):
        self.rect.y += star_speed
        if self.rect.bottom > screen_height + 80:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceship_group, False, pygame.sprite.collide_mask):
            spaceship.health_rem -=1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosion_group.add(explosion)
            ship_hit.set_volume(0.2)
            ship_hit.play()
            self.kill()
        
        

# create sprite groups
spaceship_group = pygame.sprite.Group() 
bullet_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()



def spawn_stars():
    for _ in range(3):
        x = random.randint(0, screen_width)
        new_star = Stars(x)  # Assuming the star image is not larger than 20px in height
        star_group.add(new_star)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x - img.get_width()/2, y - img.get_height()/2)) 


    
#Create player
spaceship = Spaceship(int(screen_width/2), screen_height - 150, player_health)
spaceship_group.add(spaceship)

def game():
    run = True
    
    game_state = 0
    end_time = 0

    elapsed_time = 0
    start_time = time.time()

    star_add_increment = 2000 # first star
    start_count = 0 #when we get the next star

    prepare_time = 3
    last_second = pygame.time.get_ticks()

    while run:  #gameloop

        start_count += clock.tick(fps)
        
        
        draw_bg()
        if prepare_time == 0:
            
            if game_state == 0:

                if start_count > star_add_increment:
                    spawn_stars()
                    star_add_increment = max(200, star_add_increment - 20)
                    start_count = 0
                
                
                #time
                elapsed_time = time.time() - start_time - 3
                time_text = FONT30.render(f"Time: {round(elapsed_time)}s", 1, "white")
                screen.blit(time_text, (10, 10))
                
                #update spaceship
                game_state = spaceship.update()

                #update sprite groups
                bullet_group.update()
                star_group.update()

            else:
                if game_state == -1:
                    draw_text("Game Over", FONT50, "white", screen_width / 2, screen_height / 2)
                    if end_time == 0:
                        end_time = round(elapsed_time, 2)
                    draw_text(f"Time: {end_time}s", FONT30, "white", screen_width / 2, screen_height / 2 + 50)
                    draw_text("Press R to restart or M for menu", FONT30, "white", screen_width / 2, screen_height / 2 + 100)
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_r]:
                        star_group.empty()
                        bullet_group.empty()
                        spaceship.reset()
                        game_state = 0
                        prepare_time = 4
                        start_time = time.time()
                        pygame.mixer.music.play(-1)
                        end_time = 0
                        

        #update animations
        explosion_group.update()

        if prepare_time > 0:
            draw_text("Get Ready!", FONT50, "white", screen_width / 2, screen_height / 2)
            draw_text(str(prepare_time), FONT30, "white", screen_width / 2, screen_height / 2 + 50)
            count_timer = pygame.time.get_ticks()
            if count_timer - last_second > 1000:
                prepare_time -= 1
                last_second = count_timer
        
        #draw sprite groups
        spaceship_group.draw(screen)
        bullet_group.draw(screen)
        star_group.draw(screen)
        explosion_group.draw(screen)

        #events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False 
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m and game_state == -1:
                        star_group.empty()
                        bullet_group.empty()
                        spaceship.reset()
                        game_state = 0
                        prepare_time = 4
                        start_time = time.time()
                        end_time = 0
                        pygame.mixer.music.play(-1)
                        menu.main_menu()
                        break

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    menu.main_menu()
    game()
    