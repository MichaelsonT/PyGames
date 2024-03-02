#tutorial credits -> Tech With Tim
#https://www.youtube.com/watch?v=waY3LfJhQLY&ab_channel=TechWithTim

import pygame
import time
import random
import menu
#import music
pygame.font.init()
pygame.mixer.init()

#sounds
pygame.mixer.music.load("space.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.1)
boopsound = pygame.mixer.Sound("boop.mp3")

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodge")

PLAYER_WIDHT = 30
PLAYER_HEIGHT = 50
PLAYER_VEL = 5

START_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

BULLET_WIDTH = 10
BULLET_HEIGHT = 10
BULLET_VEL = 5

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (WIDTH, HEIGHT))
Ship_image = pygame.image.load("Ship.png")

FONT = pygame.font.SysFont("comicsans", 30)

#player
class Player():
    def __init__(self, x, y):
        self.image = Ship_image
        self.widht = PLAYER_WIDHT
        self.height = PLAYER_HEIGHT
        self.rect = pygame.Rect(0, 0, self.widht, self.height)
        self.rect.center = (x, y)
    
    def moves(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x - PLAYER_VEL >= 0:
            self.rect.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and self.rect.x + self.widht <= WIDTH:
            self.rect.x += PLAYER_VEL
        if keys[pygame.K_UP] and self.rect.y + PLAYER_VEL > 0:
            self.rect.y -= PLAYER_VEL
        if keys[pygame.K_DOWN] and self.rect.y + self.height < HEIGHT:
            self.rect.y += PLAYER_VEL
        
    def shoot(self):
        # The bullet will be spawned at the top-center of the ship
        new_bullet = Bullet(self.rect.centerx, self.rect.top)
        bullets.append(new_bullet)  # Add the new bullet to the bullets list

        
    
    def draw(self):
        WIN.blit(self.image, (self.rect.x - 10, self.rect.y - 10)) # center the rectangle
        pygame.draw.rect(WIN, "red", self.rect, 2)


class Bullet:
    def __init__(self, x, y, width=BULLET_WIDTH, height=BULLET_HEIGHT, velocity=BULLET_VEL):
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = velocity

    def move(self):
        self.rect.y -= self.vel

    def draw(self):
        pygame.draw.rect(WIN, "red", self.rect)  # Draw the bullet as a white rectangle


def draw(elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    
    WIN.blit(time_text, (10, 10))

    ship.draw()
 
    for bullet in bullets:  # Draw each bullet
        bullet.draw()

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

ship = Player(WIDTH/2 , 650)

bullets = []

def game():
    run = True
    
    
    #player = Player(WIDTH/2 , HEIGHT - PLAYER_HEIGHT/2)
    #player = pygame.Rect(WIDTH/2 - PLAYER_WIDHT/2, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDHT, PLAYER_HEIGHT) #player
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000 # first star
    start_count = 0 #when we get the next star

    stars = []
    hit = False

    while run:

        start_count += clock.tick(60)
        
        #clock
        elapsed_time = time.time() - start_time

        #generating stars
        if start_count > star_add_increment:
            for _ in range(5):
                star_x = random.randint(0, WIDTH - START_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, START_WIDTH, STAR_HEIGHT) #star starting point
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50) #star aperance increment
            start_count = 0
    
        #Running the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
                break # Exit the function and stop the game
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ship.shoot()  # Call shoot method when spacebar is pressed
   
        #controls
        ship.moves()

        #moving stars
        for star in stars[:]: #copy of the list
            star.y += STAR_VEL
            if star.y > HEIGHT: #gets to the end of the screen
                stars.remove(star)
            elif star.y + star.height >= PLAYER_HEIGHT and star.colliderect(ship): # see if the player got hit while the star is on the bottom
                #colliderect sees if 2 rects collided
                stars.remove(star)
                hit = True
                boopsound.set_volume(0.05)
                boopsound.play()
                break  

        #Losing the game
        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        draw(elapsed_time, stars)


            

        # Move and draw bullets
        for bullet in bullets[:]:  # Iterate over a copy of the bullets list
            bullet.move()
            if bullet.rect.bottom < 0:  # Remove the bullet if it's off-screen
                bullets.remove(bullet)

    
    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    menu.main_menu()
    game()
    

